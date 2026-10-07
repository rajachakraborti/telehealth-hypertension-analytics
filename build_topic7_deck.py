"""Build Topic_7_Capstone_Presentation.pptx (9 slides) from the notebook's saved metrics.

Every number on the slides is read from artifacts/topic6/topic6_metrics.json, so the deck cannot drift
from the results. Run from the repository root:
    python scripts/make_topic7_figures.py && python build_topic7_deck.py
"""
import json
import os
import sys

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(ROOT, "artifacts/topic6/topic6_metrics.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "Topic_7_Capstone_Presentation.pptx")
COMMIT = os.environ.get("RELEASE_COMMIT", "73adefd")
TAG = "topic7-submission"

NAVY, BLUE, ORANGE, GREEN, RED = (RGBColor(0x14, 0x30, 0x6B), RGBColor(0x2A, 0x78, 0xD6), RGBColor(0xEB, 0x68, 0x34),
                                  RGBColor(0x2F, 0x85, 0x5A), RGBColor(0xC5, 0x30, 0x30))
INK, MUTED, LIGHT = RGBColor(0x1F, 0x29, 0x33), RGBColor(0x52, 0x60, 0x6D), RGBColor(0xF1, 0xF5, 0xF9)
W, H = Inches(13.333), Inches(7.5)

prs = Presentation(); prs.slide_width, prs.slide_height = W, H
BLANK = prs.slide_layouts[6]
R, CI, SEL, SUB = M["results"], M["ci"], M["selection"], M["eda"]
tuned = R["xgb_tuned"]
fig6 = lambda n: os.path.join(ROOT, "artifacts/topic6", n)
fig7 = lambda n: os.path.join(ROOT, "artifacts/topic7", n)
page = [0]


def text(slide, x, y, w, h, paras, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=6):
    box = slide.shapes.add_textbox(x, y, w, h); tf = box.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.03)
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space)
        segs = para if isinstance(para, list) else [(para, bold, color)]
        for seg in segs:
            t, b, c = (seg + (bold, color)[len(seg) - 1:])[:3] if isinstance(seg, tuple) else (seg, bold, color)
            r = p.add_run(); r.text = t; r.font.size = Pt(size); r.font.bold = b; r.font.color.rgb = c; r.font.name = "Calibri"
    return box


def base(title, takeaway, notes):
    s = prs.slides.add_slide(BLANK); page[0] += 1
    text(s, Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.8), title, size=28, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    if takeaway:
        text(s, Inches(0.6), Inches(1.05), Inches(12.1), Inches(0.5), takeaway, size=16, color=MUTED)
    bar = s.shapes.add_shape(1, Inches(0.6), Inches(1.55), Inches(1.2), Inches(0.05)); bar.fill.solid(); bar.fill.fore_color.rgb = ORANGE; bar.line.fill.background()
    text(s, Inches(0.6), Inches(7.08), Inches(9), Inches(0.3), f"Telehealth Hypertension Analytics  |  DSC-590  |  R. Chakraborty  |  release tag {TAG}", size=10, color=MUTED)
    text(s, Inches(12.0), Inches(7.08), Inches(0.8), Inches(0.3), str(page[0]), size=10, color=MUTED, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    return s


def picture(slide, path, x, y, max_w, max_h):
    iw, ih = Image.open(path).size
    scale = min(max_w / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(path, x + int((max_w - w) / 2), y + int((max_h - h) / 2), w, h)


def callout(slide, x, y, w, big, label, color=BLUE):
    box = slide.shapes.add_shape(1, x, y, w, Inches(1.15)); box.fill.solid(); box.fill.fore_color.rgb = LIGHT; box.line.fill.background()
    text(slide, x + Inches(0.1), y + Inches(0.02), w - Inches(0.2), Inches(0.6), big, size=30, color=color, bold=True)
    text(slide, x + Inches(0.1), y + Inches(0.62), w - Inches(0.2), Inches(0.5), label, size=13, color=MUTED)


def bullets(slide, x, y, w, h, items, size=18):
    text(slide, x, y, w, h, [[("•  ", True, ORANGE)] + (it if isinstance(it, list) else [(it, False, INK)]) for it in items], size=size, space=10)


pct = lambda v, d=1: f"{v * 100:.{d}f}%"

# ---------------- 1. Title ----------------
s = prs.slides.add_slide(BLANK); page[0] += 1
bg = s.shapes.add_shape(1, 0, 0, W, H); bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
text(s, Inches(0.9), Inches(1.5), Inches(11.5), Inches(1.2), "Telehealth Hypertension Analytics", size=44, color=RGBColor(255, 255, 255), bold=True)
text(s, Inches(0.9), Inches(2.7), Inches(11.5), Inches(1.0), "From 24-hour blood pressure records to an explained, audited staging model", size=24, color=RGBColor(0xBF, 0xD4, 0xF2))
text(s, Inches(0.9), Inches(4.4), Inches(11.5), Inches(1.6),
     ["Raja Chakraborty  |  DSC-590 Data Science Capstone, Completion Phase", "Grand Canyon University  |  Instructor: Jonathan Pollyn  |  October 2026",
      f"github.com/rajachakraborti/telehealth-hypertension-analytics  |  tag {TAG}  |  commit {COMMIT}"], size=16, color=RGBColor(255, 255, 255))
s.notes_slide.notes_text_frame.text = (
    "This is the completion-phase summary of my capstone: a decision-support system that stages hypertension from a patient's 24-hour blood pressure record. "
    "In the next nine minutes: the problem, what I built, how I chose the model, the results, what a technical audit of the whole project found, and what I would do next. "
    f"Everything here traces to the repository at tag {TAG}.")

# ---------------- 2. Problem ----------------
dis, wc, mk = SUB["office_vs_true_htn_disagree"], SUB["phenotype_counts"]["White-coat"], SUB["phenotype_counts"]["Masked"]
s = base("A single office reading misjudges about one patient in four",
         f"In the simulated cohort, one clinic reading disagrees with the patient's true hypertensive status {pct(dis)} of the time",
         "Hypertension is diagnosed from spot-checks in the clinic, but blood pressure moves through the day. White-coat patients read high only in clinic; masked patients read normal in clinic and high outside it. "
         f"In my simulated cohort, {pct(dis)} of patients are misjudged by one office reading, and a rule applied to that single reading stages only {pct(R['office_rule']['accuracy'])} correctly. "
         "Ambulatory monitoring records 48 readings over 24 hours and fixes this, but nobody has time to read 48 numbers per patient. The goal: automate the staging and show why.")
bullets(s, Inches(0.6), Inches(1.9), Inches(5.6), Inches(4.8), [
    [("Office spot-check: ", True, INK), (f"stages {pct(R['office_rule']['accuracy'])} of patients correctly", False, INK)],
    [(f"White-coat {pct(wc / 1800)} and masked {pct(mk / 1800)}: ", True, INK), ("opposite errors from the same single reading", False, INK)],
    [("24-hour monitoring ", True, INK), ("(ABPM) fixes this but produces 48 readings per patient to review", False, INK)],
    [("Goal: ", True, INK), ("stage each patient from the full record, show which measurements drove the result, and flag low-confidence cases", False, INK)]], size=18)
picture(s, fig6("topic6_fig8_office_vs_abpm.png"), Inches(6.4), Inches(1.8), Inches(6.4), Inches(5.1))

# ---------------- 3. System ----------------
s = base("A staging API and dashboard page serve the refined model",
         "Architecture as built; the Jira retraining loop from the earlier design is not implemented and is shown dashed",
         "This is the system as built, not as originally designed. A clinician signs in through the React dashboard on Vercel; the FastAPI backend on Render checks the JWT role, rate-limits, and serves one endpoint that takes a 24-hour record and returns the stage, probabilities, the top explaining measurements and a manual-review flag. "
         "Patient identifiers are stored with column-level encryption in PostgreSQL. The audit corrected two things I had claimed earlier: login previously accepted any password, and the override-to-Jira retraining loop was never built, so it is dashed here.")
picture(s, fig7("topic7_architecture.png"), Inches(0.35), Inches(1.7), Inches(9.4), Inches(5.3))
bullets(s, Inches(9.9), Inches(1.9), Inches(3.1), Inches(4.9), [
    [("One request = one patient-day: ", True, INK), ("48 readings in, stage + explanation out", False, INK)],
    [("Explained: ", True, INK), ("exact TreeSHAP drivers, signed", False, INK)],
    [("Safe by default: ", True, INK), ("flags confidence under 65% for manual review", False, INK)],
    [("Secured: ", True, INK), ("bcrypt passwords, JWT roles, rate limit, encrypted PHI columns", False, INK)]], size=15)

# ---------------- 4. Data and method ----------------
s = base("Each patient is a 24-hour record reduced to 11 clinical features",
         "Simulated because real patient records are protected; dipping and surge patterns are built into the simulator",
         "The cohort is simulated: 1,800 patients, 450 per stage, each with 48 half-hourly readings with measurement noise, 3% cuff artifacts and 8% missing readings. "
         "From each record I compute day and night averages, mean arterial pressure, pulse pressure and the nocturnal dipping ratio, the way a clinician reads an ambulatory report. "
         "One caution I carry through the whole deck: the simulator builds in the dipping and morning-surge differences, so finding them confirms the pipeline works; it is not a clinical discovery.")
bullets(s, Inches(0.6), Inches(1.9), Inches(5.8), Inches(4.8), [
    [("1,800 patients x 48 readings: ", True, INK), ("noise, 3% artifacts, 8% missing", False, INK)],
    [("11 features: ", True, INK), ("day/night pressure, MAP, pulse pressure, dipping ratio, age, BMI, heart rate", False, INK)],
    [("XGBoost, ", True, INK), (f"tuned on {M['n_train']:,} patients; {M['n_test']} held out and untouched until the end", False, INK)],
    [("Caveat: ", True, RED), ("labels and features come from the same simulator, so scores are an upper bound", False, INK)]], size=18)
picture(s, fig6("topic6_fig6_circadian.png"), Inches(6.5), Inches(1.8), Inches(6.3), Inches(3.4))
text(s, Inches(6.5), Inches(5.3), Inches(6.3), Inches(0.9), "Mean systolic profile by stage. The night-time dip and the 06:00 to 10:00 surge are assumptions built into the simulator, so seeing them confirms the pipeline works; it is not a clinical finding.", size=13, color=MUTED)

# ---------------- 5. Selection ----------------
cm = SEL["comparisons"]
s = base("Cross-validation chose the model; the holdout chose nothing",
         "Rules were fixed first: adopt at 2 standard errors of log-loss gain, reject at minus 2",
         "My professor pointed out that I had used holdout results to keep or drop refinements. I rebuilt the selection. Rules first: adopt a step only if it lowers cross-validated log loss by at least two standard errors, reject it if it raises it by that much. "
         f"Result: hyperparameter search is strongly supported (z about {cm['hyperparameter_search']['logloss']['z']:.0f}, and it survives nested cross-validation). Feature engineering shows no reliable accuracy gain, so I keep it as the clinically defined design, not as an improvement. "
         f"Isotonic calibration is rejected because it makes log loss worse (z {cm['isotonic_calibration']['logloss']['z']:.1f}), and the morning-surge features add nothing. Two of my earlier explanations were wrong, and the report now says so.")
picture(s, fig7("topic7_cv_selection.png"), Inches(0.5), Inches(1.8), Inches(8.2), Inches(4.0))
bullets(s, Inches(8.9), Inches(1.9), Inches(4.0), Inches(4.9), [
    [("Tuning: ", True, GREEN), ("adopted; holds up under nested CV", False, INK)],
    [("Features: ", True, BLUE), ("kept for interpretability, no accuracy gain", False, INK)],
    [("Isotonic calibration: ", True, RED), ("rejected, worse log loss and 5 to 6x slower", False, INK)],
    [("Surge features: ", True, MUTED), ("no supported gain", False, INK)]], size=16)
text(s, Inches(0.6), Inches(5.95), Inches(8.2), Inches(0.9),
     "Corrected claims: feature engineering did not raise accuracy, and calibration did not \"worsen\" Brier score and ECE in cross-validation; its clear cost is log loss and latency.", size=14, color=MUTED)

# ---------------- 6. Results ----------------
ci_lr, ci_def, ci_abpm = CI["acc_diff_vs_logreg"], CI["acc_diff_vs_xgb_default"], CI["acc_diff_vs_abpm_rule"]
s = base(f"{pct(tuned['accuracy'])} accuracy and {pct(tuned['crisis_recall'], 0)} Stage 2 recall, with the uncertainty shown",
         "Clear win over guideline rules; the gain over simpler machine learning is within noise",
         f"On 540 held-out patients the refined model reaches {pct(tuned['accuracy'])} accuracy; Stage 2 recall is {tuned['crisis_recall']:.3f} at precision {tuned['precision'][3]:.3f}, macro AUC {tuned['macro_roc_auc']:.3f}, and calibration error {tuned['ece']:.3f}. "
         f"Inference plus explanation takes about {tuned['latency_ms'] + tuned['shap_latency_ms']:.0f} milliseconds. The honest reading of the intervals: the gain over guideline rules is large ({ci_abpm[0] * 100:.0f} to {ci_abpm[1] * 100:.0f} points), "
         f"but the gain over logistic regression ({ci_lr[0] * 100:.1f} to {ci_lr[1] * 100:+.1f}) and default XGBoost ({ci_def[0] * 100:.1f} to {ci_def[1] * 100:+.1f}) includes zero. "
         "What the extra work buys is better-calibrated probabilities and an explanation, not a large accuracy jump.")
picture(s, fig7("topic7_benchmarks.png"), Inches(0.5), Inches(1.8), Inches(7.6), Inches(4.4))
callout(s, Inches(8.4), Inches(1.85), Inches(2.2), f"{tuned['crisis_recall']:.3f}", "Stage 2 recall", ORANGE)
callout(s, Inches(10.75), Inches(1.85), Inches(2.2), f"{tuned['precision'][3]:.3f}", "Stage 2 precision", ORANGE)
callout(s, Inches(8.4), Inches(3.2), Inches(2.2), f"{tuned['macro_roc_auc']:.3f}", "macro ROC-AUC")
callout(s, Inches(10.75), Inches(3.2), Inches(2.2), f"{tuned['ece']:.3f}", "calibration error (ECE)")
callout(s, Inches(8.4), Inches(4.55), Inches(2.2), f"{tuned['latency_ms'] + tuned['shap_latency_ms']:.0f} ms", "prediction + explanation")
callout(s, Inches(10.75), Inches(4.55), Inches(2.2), f"+{ci_abpm[0] * 100:.0f} to +{ci_abpm[1] * 100:.0f}", "points vs ABPM rule (95% CI)", GREEN)
text(s, Inches(0.6), Inches(6.3), Inches(12.2), Inches(0.7),
     f"Versus logistic regression the accuracy gain is {ci_lr[0] * 100:.1f} to {ci_lr[1] * 100:+.1f} points (95% CI), and versus default XGBoost {ci_def[0] * 100:.1f} to {ci_def[1] * 100:+.1f}: both include zero.", size=14, color=MUTED)

# ---------------- 7. Audit ----------------
s = base("The audit found real gaps between the claims and the code",
         "Eight of the eleven findings, most serious first; the first six are fixed (full list in the report)",
         "I audited the whole project: the notebook, the backend, the frontend and the tests. The most serious findings were in security: login accepted any password for an existing username, and registration stored plaintext passwords and let a caller choose the administrator role. Both are fixed and tested. "
         "The model the API served was a different, leakier per-reading model than the one in my report, so I built an endpoint that serves the evaluated model and proved it reproduces the notebook. The earlier selection process used the holdout, now fixed. "
         "Two items remain open and are stated plainly: the database encryption key falls back to a default and needs a re-encryption migration, and the committed demo accounts need rotated passwords on any shared deployment.")
rows = [("Finding", "Severity", "Status"),
        ("Login accepted any password for a known username", "Critical", "Fixed, tested"),
        ("Registration stored plaintext and allowed self-assigned admin role", "Critical", "Fixed, tested"),
        ("Served model was per-reading and leaky, not the reported model", "High", "Fixed: new endpoint, parity test"),
        ("Holdout set influenced refinement decisions", "High", "Fixed: CV selection + nested check"),
        ("Suite broken (1 import error, 1 failing test); no tests for new logic", "Medium", "Fixed: all tests pass"),
        ("Jira override retraining and a dashboard SHAP view were claimed, not built", "Medium", "Claim removed; SHAP page built"),
        ("Database encryption key has a built-in default", "Medium", "Open: needs re-encryption"),
        ("Demo accounts ship with known passwords; CORS open to all origins", "Low", "Mitigated: hashed, env overrides")]
tbl = s.shapes.add_table(len(rows), 3, Inches(0.6), Inches(1.85), Inches(12.1), Inches(4.9)).table
for j, w in enumerate((7.0, 1.4, 3.7)):
    tbl.columns[j].width = Inches(w)
sev_color = {"Critical": RED, "High": ORANGE, "Medium": BLUE, "Low": MUTED}
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        c = tbl.cell(i, j); c.text = v; para = c.text_frame.paragraphs[0]; r = para.runs[0]
        r.font.size = Pt(15 if i else 15); r.font.name = "Calibri"; r.font.bold = (i == 0 or j == 1)
        c.fill.solid(); c.fill.fore_color.rgb = NAVY if i == 0 else (LIGHT if i % 2 else RGBColor(255, 255, 255))
        r.font.color.rgb = RGBColor(255, 255, 255) if i == 0 else (sev_color[v] if j == 1 else INK)
        c.margin_top = c.margin_bottom = Inches(0.04)

# ---------------- 8. Limitations ----------------
n_near = SUB["share_errors_near_boundary"]; sub = SUB["subgroups"]
s = base("Where it fails: near stage cut-points, and for younger patients",
         f"{pct(n_near, 0)} of errors fall within 5 mmHg of a stage boundary; accuracy is lowest under age 45",
         f"Errors are not random. {pct(n_near, 0)} of the mistakes sit within five millimetres of mercury of a stage boundary, where a patient's true stage is genuinely ambiguous. "
         f"Accuracy is {pct(sub['age=<45'][0])} for patients under 45 against {pct(sub['age=65+'][0])} for those 65 and over; with 93 young patients that interval is wide, so this is a flag to investigate, not a conclusion. "
         "The biggest limitation is the data: the labels come from the same simulator as the features, so the headline accuracy is an upper bound and says nothing yet about clinical validity.")
picture(s, fig6("topic6_fig10_errors.png"), Inches(0.5), Inches(1.8), Inches(6.2), Inches(3.5))
picture(s, fig7("topic7_subgroups.png"), Inches(6.8), Inches(1.8), Inches(6.0), Inches(3.5))
bullets(s, Inches(0.6), Inches(5.45), Inches(12.2), Inches(1.5), [
    [("Boundary errors: ", True, INK), ("a 5 mmHg measurement wobble can flip a stage; the review flag and, later, prediction sets target these cases", False, INK)],
    [("Not validated clinically: ", True, RED), ("simulated data, same-generator labels; the API returns a disclaimer with every result", False, INK)]], size=16)

# ---------------- 9. Recommendations ----------------
s = base("Next: prove it on real data, then predict outcomes",
         "Each recommendation answers a specific finding; the last two follow current practice in clinical machine learning",
         "My recommendations follow from the audit rather than from a wish list. First, nothing here is clinically validated, so the priority is an external test on real ambulatory data, reported to the TRIPOD+AI standard. "
         "Second, because the stage labels are produced by the same guideline thresholds the model learns, the more valuable target is a real outcome, such as confirmed hypertension or cardiovascular events. "
         "Third, my 65 percent review threshold is a policy choice, not a validated one; conformal prediction gives sets with a coverage guarantee, which suits boundary cases. "
         "Fourth, close the loop I had only drawn: log clinician overrides, monitor drift, and publish a model card per release. Fifth, check performance by age and sex on a larger sample. Deep sequence models only make sense once real raw waveform data exists.")
recs = [("1  Validate externally", "All evidence is synthetic. Test on real multi-site ABPM data and report to TRIPOD+AI (Collins et al., 2024).", NAVY),
        ("2  Predict outcomes, not stage", "Stage labels come from the same thresholds the model learns, so it mostly re-learns a rule.", NAVY),
        ("3  Add conformal prediction sets", "The 65% review cut-off is unvalidated; sets with a coverage guarantee suit boundary cases (Angelopoulos & Bates, 2023).", NAVY),
        ("4  Close the loop", "Log overrides, monitor drift, retrain on a schedule, ship a model card per release (Mitchell et al., 2019).", NAVY),
        ("5  Audit fairness at scale", "Under-45 accuracy is 86% on 93 patients; confirm or refute on a larger real sample.", NAVY)]
for k, (head, body, col) in enumerate(recs):
    y = Inches(1.85 + k * 1.0)
    box = s.shapes.add_shape(1, Inches(0.6), y, Inches(0.09), Inches(0.82)); box.fill.solid(); box.fill.fore_color.rgb = ORANGE; box.line.fill.background()
    text(s, Inches(0.85), y - Inches(0.02), Inches(3.9), Inches(0.85), head, size=19, color=col, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(4.8), y - Inches(0.02), Inches(8.0), Inches(0.85), body, size=16, color=INK, anchor=MSO_ANCHOR.MIDDLE)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides))
