"""Write sample 24-hour records for the dashboard's ABPM Staging page.

Picks one confidently classified simulated patient per stage from the notebook's parity fixture.
Run from the repository root after the notebook has been executed:
    python scripts/make_sample_records.py
"""
import json

fixture = json.load(open("backend/tests/fixtures/abpm_parity.json"))
STAGES = ["Normal", "Elevated", "Stage 1", "Stage 2"]
samples = []
for k, name in enumerate(STAGES):
    cands = [p for p in fixture if p["stage"] == k]
    if not cands:
        continue
    best = max(cands, key=lambda p: max(p["probabilities"]))
    samples.append(dict(
        label=f"Simulated {name}",
        record=dict(age=round(best["age"], 1), bmi=round(best["bmi"], 1),
                    readings=[{k_: (round(v, 1) if isinstance(v, float) else v) for k_, v in r.items()} for r in best["readings"]])))
json.dump(samples, open("frontend/public/sample_abpm_patients.json", "w"))
print("samples:", [s["label"] for s in samples])
