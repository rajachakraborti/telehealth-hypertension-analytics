# Project progress across milestones

Telehealth Hypertension Analytics, DSC-590 Data Science Capstone (Grand Canyon University). Author: Raja Chakraborty. Instructor: Jonathan Pollyn.

This page maps each course milestone to its deliverable and to the code or commit that supports it, so a reviewer can follow the project from the first weeks to the final submission.

## How to read this history

- **The system itself** (FastAPI backend, React dashboard, PostgreSQL layer) was first built in the earlier course CST/DSC-580 (May 2026). Those commits are `7de50e3` to `03b438b`, and the documents `MILESTONE_3.md` and `DEPLOYMENT_PLAN.md` belong to that course.
- **DSC-590 work in git** begins on 2026-09-16 with the Topic 4 implementation commit `f5f2a6b`.
- **Earlier DSC-590 deliverables (Topics 1 to 3, 5 and 6) were written in a separate working folder** and were not committed when they were submitted. They were added to this repository afterwards, in the commit that introduced the `milestones/` folder. Their dates below are the original file dates, not commit dates. Git history cannot show them being created, and nothing in it has been backdated.
- Topic numbers 1 and 2 follow the course order; the code refers to the design document as the "Topic 3 Blueprint".

## Milestones

| Milestone | Date | Deliverable | Code and evidence |
|---|---|---|---|
| Foundation (CST/DSC-580) | May 4 to 13 | `MILESTONE_3.md`, `DEPLOYMENT_PLAN.md` | Commits `7de50e3` to `03b438b`: FastAPI backend, React dashboard, data ingestion, cleaning, exploration, deployment on Render and Vercel |
| Topic 1: Planning | Aug 26 | `milestones/topic1_planning/` | Project idea, objectives, needs analysis, timeline |
| Topic 2: Proposal and methodology | Sep 2 | `milestones/topic2_proposal/` | Refined scope after faculty feedback, methodology, security framework |
| Topic 3: Design blueprint | Sep 9 | `milestones/topic3_design/` | Architecture, data strategy, model design, explainability plan |
| Topic 4: Implementation and testing | Sep 16 | `milestones/topic4_implementation/` | Commits `f5f2a6b` to `449a8fe`: synthetic telemetry generator, XGBoost and SHAP pipeline, role-based access control, column encryption, rate limiting, Prometheus metrics. Load-test reports (Locust) in the same folder |
| Topic 5: Model insight and validation | Sep 23 | `milestones/topic5_model_validation/` | Model insight and validation report |
| Topic 6: Advanced analysis and refinement | Sep 30 | `milestones/topic6_advanced_analysis/` | Report and the notebook exactly as submitted |
| Topic 7: Completion phase | Oct 7 | `submissions/topic7/` | Release tag `topic7-submission` (commit `73adefd`); report and deck in `2470311`, `451cc9d` |
| Topic 8: Showcase poster | Oct 14 | `submissions/poster/` | Commit `1acb3af` and later |

## How feedback changed the project

1. **Topic 6 feedback (holdout used to choose refinements; no exact commit cited).** The notebook was rebuilt so every selection decision uses cross-validation on the training set, with rules fixed in advance and a nested cross-validation check. Reports now cite the release tag and commit. The as-submitted notebook is kept in `milestones/topic6_advanced_analysis/` for comparison with the current one at the repository root.
2. **Topic 7 technical audit.** The audit found, and the release commit `73adefd` fixed:
   - login that accepted any password, and registration that stored plaintext passwords and allowed a self-assigned administrator role;
   - a served model that differed from the evaluated model (single readings, a simulator-internal feature, row-level splits), now replaced by an endpoint that serves the evaluated model and is checked against the notebook by a parity test;
   - a broken test suite, now 48 tests;
   - claims in earlier reports with no code behind them, which were removed.
   Open findings are listed in `Topic_7_Final_Capstone_Deliverable.md`.
3. **Later fixes found while capturing screenshots:** a missing `/api/auth/users/me` route (a page refresh logged users out) and a dashboard risk score that silently showed 0% when column names differed in case.

## Where things are

| Path | Contents |
|---|---|
| `backend/` | FastAPI service, models, tests (`pytest`), synthetic data generator |
| `frontend/` | React dashboard, including the ABPM Staging page; `tests/` holds Playwright and screenshot scripts |
| `Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb` | Current notebook with executed outputs: data simulation, benchmarks, cross-validated model selection, export of the served model |
| `backend/models_saved/` | Served model (`abpm_xgb_refined.json`), model card, legacy models |
| `artifacts/` | Metrics (`topic6/topic6_metrics.json`), figures, UI screenshots |
| `Topic_7_*`, `build_topic7_*.py` | Final report, deck and the scripts that build them from the metrics |
| `Technology_Capstone_Showcase_Poster.*`, `build_showcase_poster.py` | Showcase poster and its builder |
| `submissions/` | Copies of the files submitted for Topic 7 and the poster |
| `milestones/` | Earlier deliverables, Topics 1 to 6 |
| `archive/superseded/` | Earlier drafts kept for comparison |

Reproduction steps are in the README ("Reproduce the results").
