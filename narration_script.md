# Narration script

One paragraph per slide (the deck's speaker notes). Read aloud, about 6 to 7 minutes in total.

## Slide 1

This is the completion-phase summary of my capstone: a decision-support system that stages hypertension from a patient's 24-hour blood pressure record. In the next few minutes: the problem, what I built, how I chose the model, the results, what a technical audit of the whole project found, and what I would do next. Everything here traces to the repository at tag topic7-submission.

## Slide 2

Hypertension is diagnosed from spot-checks in the clinic, but blood pressure moves through the day. White-coat patients read high only in clinic; masked patients read normal in clinic and high outside it. In my simulated cohort, 25.5% of patients are misjudged by one office reading, and a rule applied to that single reading stages only 54.3% correctly. Ambulatory monitoring records 48 readings over 24 hours and fixes this, but nobody has time to read 48 numbers per patient. The goal: automate the staging and show why.

## Slide 3

This is the system as built, not as originally designed. A clinician signs in through the React dashboard on Vercel; the FastAPI backend on Render checks the JWT role, rate-limits, and serves one endpoint that takes a 24-hour record and returns the stage, probabilities, the top explaining measurements and a manual-review flag. Patient identifiers are stored with column-level encryption in PostgreSQL. The audit corrected two things I had claimed earlier: login previously accepted any password, and the override-to-Jira retraining loop was never built, so it is dashed here.

## Slide 4

Here is what a clinician actually sees. On the left is the ABPM Staging page. The clinician loads a patient's 24-hour record and clicks classify. The page shows the predicted stage with its confidence, the probability for each of the four stages, and the four measurements that pushed the prediction, drawn from the exact Shapley attributions. In this example the model calls Stage 1 with 99 percent confidence, and it explains that night-time pressure dominates and that the nocturnal dip is blunted, only 7 percent. If confidence were below 65 percent, a banner would recommend manual review, and every result carries a disclaimer that the model is trained on simulated data. On the right are two more screens from the same app: summary statistics for an uploaded dataset, and the dashboard with its risk score. Sign-in is role-based, so only clinicians and administrators can classify a record.

## Slide 5

The cohort is simulated: 1,800 patients, 450 per stage, each with 48 half-hourly readings with measurement noise, 3% cuff artifacts and 8% missing readings. From each record I compute day and night averages, mean arterial pressure, pulse pressure and the nocturnal dipping ratio, the way a clinician reads an ambulatory report. One caution I carry through the whole deck: the simulator builds in the dipping and morning-surge differences, so finding them confirms the pipeline works; it is not a clinical discovery.

## Slide 6

My professor pointed out that I had used holdout results to keep or drop refinements. I rebuilt the selection. Rules first: adopt a step only if it lowers cross-validated log loss by at least two standard errors, reject it if it raises it by that much. Result: hyperparameter search is strongly supported (z about 12, and it survives nested cross-validation). Feature engineering shows no reliable accuracy gain, so I keep it as the clinically defined design, not as an improvement. Isotonic calibration is rejected because it makes log loss worse (z -3.1), and the morning-surge features add nothing. Two of my earlier explanations were wrong, and the report now says so.

## Slide 7

On 540 held-out patients the refined model reaches 90.2% accuracy; Stage 2 recall is 0.970 at precision 0.985, macro AUC 0.984, and calibration error 0.014. Inference plus explanation takes about 22 milliseconds. The honest reading of the intervals: the gain over guideline rules is large (24 to 33 points), but the gain over logistic regression (-0.2 to +3.7) and default XGBoost (-0.6 to +3.1) includes zero. What the extra work buys is better-calibrated probabilities and an explanation, not a large accuracy jump.

## Slide 8

I audited the whole project: the notebook, the backend, the frontend and the tests. The most serious findings were in security: login accepted any password for an existing username, and registration stored plaintext passwords and let a caller choose the administrator role. Both are fixed and tested. The model the API served was a different, leakier per-reading model than the one in my report, so I built an endpoint that serves the evaluated model and proved it reproduces the notebook. The earlier selection process used the holdout, now fixed. Two items remain open and are stated plainly: the database encryption key falls back to a default and needs a re-encryption migration, and the committed demo accounts need rotated passwords on any shared deployment.

## Slide 9

Errors are not random. 70% of the mistakes sit within five millimetres of mercury of a stage boundary, where a patient's true stage is genuinely ambiguous. Accuracy is 86.0% for patients under 45 against 94.4% for those 65 and over; with 93 young patients that interval is wide, so this is a flag to investigate, not a conclusion. The biggest limitation is the data: the labels come from the same simulator as the features, so the headline accuracy is an upper bound and says nothing yet about clinical validity.

## Slide 10

My recommendations follow from the audit rather than from a wish list. First, nothing here is clinically validated, so the priority is an external test on real ambulatory data, reported to the TRIPOD+AI standard. Second, because the stage labels are produced by the same guideline thresholds the model learns, the more valuable target is a real outcome, such as confirmed hypertension or cardiovascular events. Third, my 65 percent review threshold is a policy choice, not a validated one; conformal prediction gives sets with a coverage guarantee, which suits boundary cases. Fourth, close the loop I had only drawn: log clinician overrides, monitor drift, and publish a model card per release. Fifth, check performance by age and sex on a larger sample. Deep sequence models only make sense once real raw waveform data exists. Thank you; I am happy to take questions.

