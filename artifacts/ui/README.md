# UI screenshots

All captured from the running app (admin account, sample dataset `backend/static/hypertension_sample.csv` uploaded first).
Regenerate: start the backend (`:8000`) and `npm run dev` (`:3000`), then `cd frontend && node tests/capture_all_pages.mjs`.

## Best for the poster and slides
| File | Shows |
|---|---|
| `pages/22_clinical-abpm-staging-result.png` | ABPM Staging: predicted stage, probabilities, TreeSHAP drivers (the core product screen) |
| `pages/01_login.png` | Sign-in |
| `pages/04_explore-summary-statistics.png` | Summary statistics for the uploaded data |
| `pages/11_viz-dashboard-risk.png` | Dashboard with risk gauge (60%) and quick stats |
| `pages/06_explore-correlation-matrix.png`, `pages/07_cleaning-outlier-detection.png`, `pages/10_viz-chart-builder.png` | Data exploration, cleaning, charts |
| `tour/` | Three consistent crops used on the poster |
| `ui_poster_crop.png` | ABPM result crop used on the poster |

## Do not use (not working or placeholder)
| File | Why |
|---|---|
| `pages/13_modeling-model-training.png` | "Failed to load model list": the backend has no `/api/modeling/models` route |
| `pages/20_user-role-management.png` | "Not Found": the backend has no `/api/auth/users/roles` route |
| `pages/14_modeling-hyperparameter-tuning.png` | Same missing modeling routes; dropdowns are empty |
| `pages/15_modeling-feature-importance.png` | Placeholder numbers (labelled illustrative) |
