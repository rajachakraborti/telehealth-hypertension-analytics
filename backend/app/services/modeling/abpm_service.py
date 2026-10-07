"""Serve the refined ABPM staging model from the Topic 6/7 notebook (section 9).

One request is one patient's 24-hour ambulatory record (about 48 half-hourly readings),
not a single reading. Feature extraction mirrors the notebook exactly; the parity test in
tests/test_abpm_service.py replays notebook patients through this module and compares.
"""
import json
import logging
import os
import time
from functools import lru_cache
from typing import Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../../models_saved")
MODEL_PATH = os.path.join(MODEL_DIR, "abpm_xgb_refined.json")
CARD_PATH = os.path.join(MODEL_DIR, "abpm_model_card.json")

STAGES = ["Normal", "Elevated", "Stage 1", "Stage 2"]
# Below this top-class probability the result is flagged for manual clinician review.
# A policy setting, not a validated cut-off: tune it against real clinical data.
REVIEW_THRESHOLD = float(os.getenv("ABPM_REVIEW_THRESHOLD", "0.65"))
MIN_VALID_READINGS, MIN_DAY_READINGS, MIN_NIGHT_READINGS = 24, 6, 3

FEATURE_LABELS = {
    "sbp_day": "daytime systolic", "dbp_day": "daytime diastolic", "sbp_night": "night-time systolic",
    "dbp_night": "night-time diastolic", "heart_rate": "heart rate", "age": "age", "bmi": "BMI",
    "map_day": "daytime mean arterial pressure", "map_night": "night-time mean arterial pressure",
    "pulse_pressure": "pulse pressure", "dip_ratio": "nocturnal dipping ratio",
}
DISCLAIMER = ("Decision support only. The model was trained and tested on simulated data and has not been "
              "clinically validated; it must not be used for diagnosis or treatment decisions.")


class InvalidRecord(ValueError):
    """The submitted 24-hour record cannot be turned into model features."""


def _asleep(hour: float, bed: float, wake: float) -> bool:
    return (hour >= bed or hour < wake) if bed > wake else (bed <= hour < wake)


def extract_features(readings: List[dict], age: float, bmi: float,
                     bed_hour: Optional[float] = None, wake_hour: Optional[float] = None):
    """Return (features, quality) for one patient; raises InvalidRecord if the record is unusable."""
    sbp, dbp, hr, awake = [], [], [], []
    for r in readings:
        flag = r.get("awake")
        if flag is None:
            if bed_hour is None or wake_hour is None:
                raise InvalidRecord("Each reading needs an 'awake' flag, or the record needs bed_hour and wake_hour.")
            flag = not _asleep(float(r["hour"]), bed_hour, wake_hour)
        awake.append(bool(flag))
        sbp.append(np.nan if r.get("sbp") is None else float(r["sbp"]))
        dbp.append(np.nan if r.get("dbp") is None else float(r["dbp"]))
        hr.append(np.nan if r.get("hr") is None else float(r["hr"]))
    sbp, dbp, hr, awake = map(np.asarray, (sbp, dbp, hr, awake))

    valid = ~np.isnan(sbp) & ~np.isnan(dbp)
    n_day, n_night = int((valid & awake).sum()), int((valid & ~awake).sum())
    quality = dict(valid_readings=int(valid.sum()), day_readings=n_day, night_readings=n_night, warnings=[])
    if valid.sum() < MIN_VALID_READINGS or n_day < MIN_DAY_READINGS or n_night < MIN_NIGHT_READINGS:
        raise InvalidRecord(
            f"Too few valid readings (need at least {MIN_VALID_READINGS} in total, {MIN_DAY_READINGS} awake "
            f"and {MIN_NIGHT_READINGS} asleep; got {int(valid.sum())}, {n_day}, {n_night}).")
    if valid.sum() < 0.7 * len(valid):
        quality["warnings"].append("More than 30% of readings are missing; interpret with extra caution.")

    f = dict(sbp_day=np.nanmean(sbp[awake]), dbp_day=np.nanmean(dbp[awake]),
             sbp_night=np.nanmean(sbp[~awake]), dbp_night=np.nanmean(dbp[~awake]),
             heart_rate=np.nanmean(hr) if not np.all(np.isnan(hr)) else 74.0,
             age=float(age), bmi=float(bmi))
    f["map_day"] = f["dbp_day"] + (f["sbp_day"] - f["dbp_day"]) / 3
    f["map_night"] = f["dbp_night"] + (f["sbp_night"] - f["dbp_night"]) / 3
    f["pulse_pressure"] = f["sbp_day"] - f["dbp_day"]
    f["dip_ratio"] = (f["sbp_day"] - f["sbp_night"]) / f["sbp_day"]
    if np.all(np.isnan(hr)):
        quality["warnings"].append("No heart-rate data; the training-cohort mean (74 bpm) was used.")
    return {k: float(v) for k, v in f.items()}, quality


@lru_cache(maxsize=1)
def _load():
    import shap
    import xgboost as xgb
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("ABPM model artifact missing; run the notebook export (section 9).")
    card = json.load(open(CARD_PATH, encoding="utf-8"))
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    return model, shap.TreeExplainer(model), card


def model_card() -> dict:
    return _load()[2]


def classify(record: dict) -> dict:
    """Classify one 24-hour ABPM record and explain the result."""
    import pandas as pd
    model, explainer, card = _load()
    feats, quality = extract_features(record["readings"], record["age"], record["bmi"],
                                      record.get("bed_hour"), record.get("wake_hour"))
    X = pd.DataFrame([feats])[card["features"]]

    t0 = time.perf_counter()
    proba = model.predict_proba(X)[0]
    t_infer = (time.perf_counter() - t0) * 1000
    k = int(proba.argmax())

    t0 = time.perf_counter()
    sv = explainer.shap_values(X)
    sv = np.stack(sv, -1) if isinstance(sv, list) else np.asarray(sv)   # (1, features, classes)
    contrib = sv[0, :, k]
    t_explain = (time.perf_counter() - t0) * 1000
    order = np.argsort(-np.abs(contrib))[:4]
    drivers = [dict(feature=card["features"][i], label=FEATURE_LABELS[card["features"][i]],
                    value=round(feats[card["features"][i]], 3), shap=round(float(contrib[i]), 3),
                    effect=f"pushes toward {STAGES[k]}" if contrib[i] > 0 else f"pushes away from {STAGES[k]}")
               for i in order]

    confidence = float(proba[k])
    review = confidence < REVIEW_THRESHOLD
    narrative = (f"Predicted stage: {STAGES[k]} (confidence {confidence:.0%}). "
                 f"Main drivers: {drivers[0]['label']} and {drivers[1]['label']}. ")
    if feats["dip_ratio"] < 0:
        narrative += "Night-time pressure is higher than daytime (reverse dipping). "
    elif feats["dip_ratio"] < 0.10:
        narrative += f"Blunted nocturnal dipping ({feats['dip_ratio']:.0%}; a drop of 10% or more is typical). "
    if review:
        narrative += f"Confidence is below {REVIEW_THRESHOLD:.0%}: manual clinician review recommended."

    logger.info("abpm_classify model=%s stage=%s confidence=%.3f review=%s", card["model_id"], STAGES[k], confidence, review)
    return dict(
        stage_index=k, stage=STAGES[k], confidence=round(confidence, 4),
        probabilities={s: round(float(p), 4) for s, p in zip(STAGES, proba)},
        needs_manual_review=bool(review), review_threshold=REVIEW_THRESHOLD,
        features={k_: round(v, 3) for k_, v in feats.items()}, data_quality=quality,
        explanation=dict(method="TreeSHAP (exact, for the predicted class)", top_drivers=drivers, narrative=narrative),
        model=dict(id=card["model_id"], sha256=card["sha256"][:12]),
        timing_ms=dict(inference=round(t_infer, 2), explanation=round(t_explain, 2)),
        disclaimer=DISCLAIMER)
