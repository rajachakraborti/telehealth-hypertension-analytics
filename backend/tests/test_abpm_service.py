"""ABPM staging service: parity with the notebook, data-quality gates and the API contract."""
import json
import os
import time

import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.core.security import create_access_token
from app.main import app
from app.services.modeling import abpm_service as svc

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "abpm_parity.json")
client = TestClient(app)


@pytest.fixture(scope="module")
def parity():
    with open(FIXTURE) as fh:
        return json.load(fh)


def _auth(role="clinician"):
    return {"Authorization": f"Bearer {create_access_token({'sub': 'tester', 'role': role})}"}


def _payload(p, drop_awake=False):
    readings = [{k: v for k, v in r.items() if not (drop_awake and k == "awake")} for r in p["readings"]]
    out = dict(age=p["age"], bmi=p["bmi"], readings=readings)
    if drop_awake:
        out.update(bed_hour=p["bed"], wake_hour=p["wake"])
    return out


# ---- parity with the notebook (the reported metrics describe this exact pipeline) ----
def test_features_match_notebook(parity):
    for p in parity:
        feats, _ = svc.extract_features(p["readings"], p["age"], p["bmi"])
        for name, expected in p["features"].items():
            assert feats[name] == pytest.approx(expected, rel=1e-9, abs=1e-9), name


def test_probabilities_match_notebook(parity):
    for p in parity:
        out = svc.classify(_payload(p))
        got = np.array([out["probabilities"][s] for s in svc.STAGES])
        assert np.allclose(got, p["probabilities"], atol=2e-4)
        assert out["stage_index"] == p["stage"]


def test_bed_wake_fallback_agrees_with_diary_flags(parity):
    same = sum(svc.classify(_payload(p))["stage_index"] == svc.classify(_payload(p, drop_awake=True))["stage_index"]
               for p in parity)
    assert same >= len(parity) - 1   # the smooth diary indicator vs a hard threshold may flip one boundary case


# ---- response content ----
def test_response_contract(parity):
    out = svc.classify(_payload(parity[0]))
    assert set(out) >= {"stage", "confidence", "probabilities", "needs_manual_review", "explanation", "model", "disclaimer"}
    assert sum(out["probabilities"].values()) == pytest.approx(1.0, abs=1e-3)
    assert len(out["explanation"]["top_drivers"]) == 4
    assert out["needs_manual_review"] == (out["confidence"] < svc.REVIEW_THRESHOLD)


def test_low_confidence_is_flagged_for_review(parity, monkeypatch):
    monkeypatch.setattr(svc, "REVIEW_THRESHOLD", 1.01)
    out = svc.classify(_payload(parity[0]))
    assert out["needs_manual_review"] and "manual clinician review" in out["explanation"]["narrative"]


def test_model_card_states_limitations():
    card = svc.model_card()
    assert any("not clinically validated" in s for s in card["limitations"])
    assert card["holdout"]["n"] == 540


# ---- data-quality gates ----
def test_too_few_valid_readings_rejected(parity):
    p = parity[0]
    readings = [dict(r, sbp=None, dbp=None) if i % 3 else r for i, r in enumerate(p["readings"])]
    with pytest.raises(svc.InvalidRecord):
        svc.extract_features(readings, p["age"], p["bmi"])


def test_missing_awake_and_no_bed_wake_rejected(parity):
    p = parity[0]
    readings = [{k: v for k, v in r.items() if k != "awake"} for r in p["readings"]]
    with pytest.raises(svc.InvalidRecord):
        svc.extract_features(readings, p["age"], p["bmi"])


# ---- API ----
def test_api_requires_authentication(parity):
    assert client.post("/api/abpm/classify", json=_payload(parity[0])).status_code == 401


def test_api_rejects_unauthorised_role(parity):
    r = client.post("/api/abpm/classify", json=_payload(parity[0]), headers=_auth("data_analyst"))
    assert r.status_code == 403


def test_api_classifies_for_clinician(parity):
    r = client.post("/api/abpm/classify", json=_payload(parity[0]), headers=_auth())
    assert r.status_code == 200 and r.json()["stage"] in svc.STAGES


def test_api_rejects_out_of_range_values(parity):
    bad = _payload(parity[0])
    bad["readings"][0]["sbp"] = 900
    assert client.post("/api/abpm/classify", json=bad, headers=_auth()).status_code == 422


def test_api_reports_unusable_record_as_422(parity):
    bad = _payload(parity[0])
    bad["readings"] = [dict(r, sbp=None, dbp=None) for r in bad["readings"]]
    r = client.post("/api/abpm/classify", json=bad, headers=_auth())
    assert r.status_code == 422 and "Too few valid readings" in r.json()["detail"]


def test_inference_plus_explanation_within_slo(parity):
    svc.classify(_payload(parity[0]))   # warm the cache
    times = []
    for p in parity[:15]:
        t0 = time.perf_counter()
        svc.classify(_payload(p))
        times.append((time.perf_counter() - t0) * 1000)
    assert float(np.median(times)) < 200   # the 200 ms clinical service-level objective
