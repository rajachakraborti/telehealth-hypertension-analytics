"""Build the Technology Capstone Showcase poster (36 x 48 in) from the course template.

Every number is read from artifacts/topic6/topic6_metrics.json, so the poster matches the report and deck.
    python build_showcase_poster.py
Outputs Technology_Capstone_Showcase_Poster.pptx and .pdf in the repository root.
"""
import json
import math
import os

import win32com.client
from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.environ.get("POSTER_TEMPLATE", r"C:\Users\rajac\Downloads\DSC-590-RS-T8-Benchmark-TechnologyShowcasePosterTemplate.pptx")
OUT_PPTX = os.path.join(ROOT, "Technology_Capstone_Showcase_Poster.pptx")
OUT_PDF = os.path.join(ROOT, "Technology_Capstone_Showcase_Poster.pdf")
M = json.load(open(os.path.join(ROOT, "artifacts/topic6/topic6_metrics.json"), encoding="utf-8"))
EMAIL = "rajachakraborti@gmail.com"
REPO = "github.com/rajachakraborti/telehealth-hypertension-analytics"

# ---- numbers, all from the notebook's saved metrics ----
R = M["results"]; T = R["xgb_tuned"]; CI = M["ci"]; SUB = M["eda"]["subgroups"]
acc, crisis_recall = T["accuracy"], T["crisis_recall"]
cm = T["cm"]; n_crisis = sum(cm[3]); caught = cm[3][3]
off_by_two = sum(cm[i][j] for i in range(4) for j in range(4) if abs(i - j) >= 2)
latency = T["latency_ms"] + T["shap_latency_ms"]
office_acc, abpm_acc = R["office_rule"]["accuracy"], R["abpm_rule"]["accuracy"]
disagree = M["eda"]["office_vs_true_htn_disagree"]
u45 = SUB["age=<45"]

def rgb(h): return RGBColor.from_string(h)
HEADER, PURPLE, PALE, TEXT, MUTED, ORANGE, BORDER = "280334", "522398", "F3EEF8", "1F2933", "52606D", "EB6834", "D9CCEB"
WHITE = "FFFFFF"
FONT = "Calibri"
PT_BODY, PT_SMALL, PT_HEAD = 30, 25, 46

prs = Presentation(TEMPLATE)
slide = prs.slides[0]
header_box = logo = None
for sh in list(slide.shapes):
    if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
        logo = sh
    elif sh.name == "TextBox 3":
        header_box = sh
    else:
        sh._element.getparent().remove(sh._element)        # template instruction boxes
for p in header_box.text_frame.paragraphs[1:]:
    p._p.getparent().remove(p._p)
header_box.text_frame.paragraphs[0].runs[0].text = ""


# ------------------------------------------------------------------ helpers
def est_lines(text, width_in, size, bold=False):
    per = max(1, int(width_in * 72 / (size * (0.53 if bold else 0.49))))
    total = 0
    for para in text.split("\n"):
        cur, n = 0, 1
        for w in para.split():
            need = len(w) + (1 if cur else 0)
            if cur + need > per:
                n += 1; cur = len(w)
            else:
                cur += need
        total += n
    return total

def est_h(text, width_in, size, bold=False, after=8, spacing=1.2):
    return est_lines(text, width_in, size, bold) * size * spacing / 72 + after / 72

def add_bullet(p, indent_in, color=PURPLE):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(int(Inches(indent_in)))); pPr.set("indent", str(-int(Inches(indent_in))))
    clr = etree.SubElement(pPr, qn("a:buClr")); etree.SubElement(clr, qn("a:srgbClr")).set("val", color)
    etree.SubElement(pPr, qn("a:buChar")).set("char", "\u2022")

def textbox(x, y, w, h, paras, size=PT_BODY, color=TEXT, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, after=8, bullet=False):
    """paras: list of paragraphs; a paragraph is a str or a list of (text, {opts}) runs."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = box.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(after); p.line_spacing = 1.0
        runs = [(para, {})] if isinstance(para, str) else para
        for text, o in runs:
            r = p.add_run(); r.text = text; f = r.font
            f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold); f.italic = o.get("italic", False)
            f.color.rgb = rgb(o.get("color", color))
        if bullet:
            add_bullet(p, 0.55)
    return box

def rect(x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(2.5)
    else: s.line.fill.background()
    s.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s

def picture(path, x, y, w, border=True, col_w=None):
    iw, ih = Image.open(path).size
    h = w * ih / iw
    off = (col_w - w) / 2 if col_w else 0
    pic = slide.shapes.add_picture(path, Inches(x + off), Inches(y), Inches(w), Inches(h))
    if border:
        pic.line.color.rgb = rgb(BORDER); pic.line.width = Pt(2.5)
    return h

def section(x, y, w, number, title):
    bar = rect(x, y, w, 1.35, PURPLE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    tf = bar.text_frame; tf.margin_left = Inches(0.45); tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = f"{number}  {title}"; r.font.name = FONT; r.font.size = Pt(PT_HEAD); r.font.bold = True; r.font.color.rgb = rgb(WHITE)
    return y + 1.35 + 0.45

def body(x, y, w, paras, size=PT_BODY, bullet=False, after=10, color=TEXT):
    """Stack text; paras are str or run lists. Returns new y."""
    plain = [p if isinstance(p, str) else "".join(t for t, _ in p) for p in paras]
    h = sum(est_h(t, w - (0.55 if bullet else 0), size, after=after) for t in plain)
    textbox(x, y, w, h, paras, size=size, bullet=bullet, after=after, color=color)
    return y + h + 0.1

def caption(x, y, w, text):
    h = est_h(text, w, PT_SMALL, after=0) + 0.15
    textbox(x, y, w, h, [[(text, {"italic": True})]], size=PT_SMALL, color=MUTED, after=0)
    return y + h + 0.25

def stat_card(x, y, w, h, big, label, big_size=84):
    rect(x, y, w, h, PALE, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    textbox(x + 0.2, y + 0.15, w - 0.4, h * 0.5, [big], size=big_size, color=PURPLE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, after=0)
    textbox(x + 0.25, y + h * 0.55, w - 0.5, h * 0.42, [label], size=PT_SMALL, color=TEXT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP, after=0)

b = lambda t: (t, {"bold": True})
n = lambda t: (t, {})

# ------------------------------------------------------------------ header
header_box.top, header_box.height = 0, Inches(6.82)
textbox(1.0, 0.7, 26.8, 2.1, ["Telehealth Hypertension Analytics"], size=104, color=WHITE, bold=True, after=0)
textbox(1.0, 2.95, 26.8, 1.0, ["Explained, audited blood pressure staging from 24-hour monitoring"], size=50, color="E6D9F5", after=0)
textbox(1.0, 4.35, 26.8, 2.2, [
    [("Raja Chakraborty", {"bold": True}), (", M.S. in Data Science  |  " + EMAIL, {})],
    "Faculty advisor: Jonathan Pollyn  |  DSC-590 Data Science Capstone  |  Grand Canyon University"], size=38, color=WHITE, after=6)
rect(28.7, 0.6, 5.9, 5.9, WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
logo.left, logo.top, logo.width, logo.height = Inches(28.95), Inches(0.85), Inches(5.4), Inches(5.4)
slide.shapes._spTree.remove(logo._element); slide.shapes._spTree.append(logo._element)   # keep logo above its panel

# ------------------------------------------------------------------ geometry
X = [1.0, 12.6, 24.2]; W = 10.8; TOP = 7.7; BOTTOM = 41.3

# ================= column 1: description + justification =================
x, y = X[0], TOP
y = section(x, y, W, "1", "Project Description")
y = body(x, y, W, [
    [b("What it is. "), n("A decision-support tool that reads a patient's full 24-hour blood pressure record, suggests a hypertension stage, shows which measurements drove the result, and flags uncertain cases for a clinician.")],
    [b("Who it helps. "), n("Clinicians who review ambulatory monitoring (ABPM), where a wearable cuff takes about 48 readings across a day and night.")],
])
steps = [("1", "Record in", "48 readings from one 24-hour cuff recording"), ("2", "Stage + explain", "Normal, Elevated, Stage 1 or Stage 2, with reasons"),
         ("3", "Clinician decides", "Low-confidence cases are flagged for review")]
bw, gap, bh = 3.2, 0.6, 3.9
for i, (num, head, desc) in enumerate(steps):
    bx = x + i * (bw + gap)
    rect(bx, y, bw, bh, PALE, line=BORDER, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    circ = rect(bx + bw / 2 - 0.45, y + 0.2, 0.9, 0.9, PURPLE, shape=MSO_SHAPE.OVAL)
    tf = circ.text_frame; tf.margin_left = tf.margin_right = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    r = tf.paragraphs[0].add_run(); r.text = num; r.font.size = Pt(40); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb(WHITE)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    textbox(bx + 0.1, y + 1.25, bw - 0.2, 0.7, [head], size=26, bold=True, color=PURPLE, align=PP_ALIGN.CENTER, after=0)
    textbox(bx + 0.2, y + 2.05, bw - 0.4, 1.8, [desc], size=24, align=PP_ALIGN.CENTER, after=0)
y += bh + 0.45
y = body(x, y, W, [
    [b("What was built. "), n("A machine learning model, a secured web service (API), a dashboard page and 44 automated tests, released together as one tagged version on GitHub.")],
    [b("Data. "), n("Real patient records are protected, so every result here uses 1,800 simulated patients.")],
])
y += 0.35

y = section(x, y, W, "2", "Project Justification")
y = body(x, y, W, [
    "High blood pressure is a leading modifiable risk factor for cardiovascular disease, yet it is usually diagnosed from a few office readings (Whelton et al., 2018).",
    "A single reading can mislead in both directions: white-coat hypertension looks high only in the clinic, and masked hypertension looks normal in the clinic but is high outside it.",
])
cw3 = (W - 0.6) / 3
for i, (big, lab) in enumerate([(f"{disagree * 100:.1f}%", "one office reading disagrees with true status"), (f"{office_acc * 100:.0f}%", "office-rule staging accuracy"),
                                ("48", "readings per patient to review by hand")]):
    stat_card(x + i * (cw3 + 0.3), y, cw3, 3.1, big, lab, big_size=66)
y += 3.1 + 0.4
h = picture(os.path.join(ROOT, "artifacts/topic6/topic6_fig8_office_vs_abpm.png"), x, y, 9.4, col_w=W)
y += h + 0.2
y = caption(x, y, W, "Each dot is a simulated patient. Orange: high in clinic but not hypertensive (white-coat). Green: normal in clinic but hypertensive (masked).")
col1_end = y

# ================= column 2: requirements + design process =================
x, y = X[1], TOP
y = section(x, y, W, "3", "Functional Requirements, Specifications and Standards")
rows = [
    ("Requirement", "Specification as built", "Standard or evidence"),
    ("Stage a patient from a 24-hour record", "One API call takes about 48 readings and returns Normal, Elevated, Stage 1 or Stage 2", "2017 ACC/AHA staging (Whelton et al., 2018)"),
    ("Explain every result", "Top four contributing measurements plus a plain-English summary", "TreeSHAP attributions (Lundberg et al., 2020)"),
    ("Give trustworthy confidence", f"Calibrated probabilities (error {T['ece']:.3f}); results under 65% flagged for review", "Reporting guided by TRIPOD+AI (Collins et al., 2024)"),
    ("Respond within 200 ms", f"Measured {latency:.0f} ms for prediction plus explanation", "Project service-level objective"),
    ("Protect patient data", "Hashed passwords, role-based access tokens, rate limiting, encrypted patient columns", "HIPAA Security Rule safeguards (U.S. Department of Health and Human Services, 2013)"),
    ("Be reproducible and tested", "Fixed random seeds, 44 automated tests, tagged release", "Documented in a model card (Mitchell et al., 2019)"),
]
cols = [3.0, 4.2, 3.6]
row_h = [0.95] + [max(est_h(c, cols[j] - 0.3, 23, after=0) for j, c in enumerate(r)) + 0.25 for r in rows[1:]]
tbl_shape = slide.shapes.add_table(len(rows), 3, Inches(x), Inches(y), Inches(W), Inches(sum(row_h)))
tbl = tbl_shape.table
for j, cwid in enumerate(cols): tbl.columns[j].width = Inches(cwid)
for i, r in enumerate(rows):
    tbl.rows[i].height = Inches(row_h[i])
    for j, text in enumerate(r):
        c = tbl.cell(i, j); c.text = ""; c.fill.solid()
        c.fill.fore_color.rgb = rgb(PURPLE if i == 0 else (PALE if i % 2 else WHITE))
        c.margin_left = c.margin_right = Inches(0.15); c.margin_top = c.margin_bottom = Inches(0.1); c.vertical_anchor = MSO_ANCHOR.MIDDLE
        run = c.text_frame.paragraphs[0].add_run(); run.text = text; f = run.font
        f.name = FONT; f.size = Pt(25 if i == 0 else 23); f.bold = (i == 0 or j == 0)
        f.color.rgb = rgb(WHITE if i == 0 else (PURPLE if j == 0 else TEXT))
y += sum(row_h) + 0.6

y = section(x, y, W, "4", "Design Process")
y = body(x, y, W, ["Six stages, reshaped by two reviews: professor feedback on holdout leakage, then a self-audit."], size=PT_BODY)
stages = [("Define requirements", "Clinical need, staging rules and security needs set first"),
          ("Simulate and prepare data", "1,800 patients, 48 readings each, with noise, artifacts and gaps"),
          ("Select the model fairly", "Choices by cross-validation on training data only; 540 patients held back for one final test"),
          ("Build the service", "Secured API and dashboard page; model, model card and tests released together"),
          ("Audit the whole project", "Claims checked against the code; security and evaluation gaps found and fixed"),
          ("Report honestly", "Limits and open issues published with the results")]
step_h = 1.6
line_x = x + 0.5
rect(line_x - 0.04, y + 0.5, 0.08, step_h * (len(stages) - 1), BORDER)
for i, (head, desc) in enumerate(stages):
    sy = y + i * step_h
    circ = rect(x, sy, 1.0, 1.0, PURPLE, shape=MSO_SHAPE.OVAL)
    tf = circ.text_frame; tf.margin_left = tf.margin_right = 0; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    r = tf.paragraphs[0].add_run(); r.text = str(i + 1); r.font.size = Pt(36); r.font.bold = True; r.font.name = FONT; r.font.color.rgb = rgb(WHITE)
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    textbox(x + 1.4, sy - 0.05, W - 1.4, step_h, [[(head, {"bold": True, "color": PURPLE, "size": 30})], [(desc, {"size": 25})]], size=25, after=2)
y += step_h * len(stages) + 0.1
h = picture(os.path.join(ROOT, "artifacts/topic7/topic7_architecture.png"), x, y, 9.8, col_w=W)
y += h + 0.2
y = caption(x, y, W, "System as built. The dashed box (clinician override logging and retraining) is planned, not implemented.")
col2_end = y

# ================= column 3: data summaries + limits =================
x, y = X[2], TOP
y = section(x, y, W, "5", "Relevant Data Summaries")
cw2 = (W - 0.4) / 2
cards = [(f"{acc * 100:.1f}%", "of 540 unseen patients staged correctly"), (f"{crisis_recall * 100:.0f}%", f"of Stage 2 patients caught ({caught} of {n_crisis})"),
         (f"{off_by_two}", "patients staged more than one step from the true stage"), (f"{latency:.0f} ms", "to predict and explain one patient")]
for i, (big, lab) in enumerate(cards):
    stat_card(x + (i % 2) * (cw2 + 0.4), y + (i // 2) * 3.35, cw2, 3.05, big, lab, big_size=72)
y += 2 * 3.35 + 0.2
h = picture(os.path.join(ROOT, "artifacts/topic7/topic7_benchmarks.png"), x, y, W)
y += h + 0.2
y = caption(x, y, W, f"Accuracy on patients the model never saw. Rules on one office reading or the daytime average are right {office_acc * 100:.0f}% and {abpm_acc * 100:.0f}% of the time. "
                      "The gain over simpler machine learning is small and within the margin of error; the model's edge is better-calibrated confidence and explanations.")
h = picture(os.path.join(ROOT, "artifacts/ui/ui_poster_crop.png"), x, y, W)
y += h + 0.2
y = caption(x, y, W, "The dashboard's ABPM Staging page, captured from the running app: the predicted stage with its confidence, stage probabilities, and the four measurements that drove the result. "
                      "Night-time pressure carries the most weight, a pattern built into the simulated data.")
y = body(x, y, W, [
    [b("Where it errs. "), n(f"Most mistakes fall within 5 mmHg of a stage boundary, where the stage is a judgment call. Accuracy is lowest under age 45 ({u45[0] * 100:.0f}%, {u45[1]} patients), so it needs a larger test.")]], size=27, after=6)
y += 0.3
y = section(x, y, W, "6", "Limits and Next Steps")
y = body(x, y, W, [
    [b("Simulated data only. "), n("Not clinically validated and not for patient care.")],
    [b("Next: "), n("test on real multi-site records, predict real outcomes, and show prediction sets with coverage guarantees near stage boundaries (Angelopoulos & Bates, 2023).")],
    [b("Planned, not built: "), n("clinician override logging and retraining.")]], size=27, bullet=True, after=8)
col3_end = y

# ------------------------------------------------------------------ references strip + footer
ref_y = 41.6
rect(1.0, ref_y - 0.2, 34.0, 0.06, BORDER)
textbox(1.0, ref_y, 6, 0.8, ["References"], size=34, bold=True, color=PURPLE, after=0)
I = lambda t: (t, {"italic": True})
refs = [
    [[n("Angelopoulos, A. N., & Bates, S. (2023). Conformal prediction: A gentle introduction. "), I("Foundations and Trends in Machine Learning, 16"), n("(4), 494\u2013591. https://doi.org/10.1561/2200000101")],
     [n("Collins, G. S., Moons, K. G. M., Dhiman, P., Riley, R. D., Beam, A. L., Van Calster, B., ... Logullo, P. (2024). TRIPOD+AI statement: Updated guidance for reporting clinical prediction models that use regression or machine learning methods. "), I("BMJ, 385"), n(", Article e078378. https://doi.org/10.1136/bmj-2023-078378")]],
    [[n("Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. "), I("Nature Machine Intelligence, 2"), n("(1), 56\u201367. https://doi.org/10.1038/s42256-019-0138-9")],
     [n("Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. In "), I("Proceedings of the Conference on Fairness, Accountability, and Transparency"), n(" (pp. 220\u2013229). ACM. https://doi.org/10.1145/3287560.3287596")]],
    [[n("U.S. Department of Health and Human Services. (2013). Modifications to the HIPAA Privacy, Security, Enforcement, and Breach Notification Rules under the Health Information Technology for Economic and Clinical Health Act and the Genetic Information Nondiscrimination Act; other modifications to the HIPAA rules. "), I("Federal Register, 78"), n("(17), 5566\u20135702.")],
     [n("Whelton, P. K., Carey, R. M., Aronow, W. S., Casey, D. E., Collins, K. J., Himmelfarb, C. D., ... Wright, J. T. (2018). 2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults. "), I("Journal of the American College of Cardiology, 71"), n("(19), e127\u2013e248. https://doi.org/10.1016/j.jacc.2017.11.006")]],
]
for i, col in enumerate(refs):
    tb_ = textbox(X[i], ref_y + 0.85, W, 3.0, col, size=19, color=TEXT, after=6)
    for p in tb_.text_frame.paragraphs:
        pPr = p._p.get_or_add_pPr(); pPr.set("marL", str(int(Inches(0.4)))); pPr.set("indent", str(-int(Inches(0.4))))

rect(0, 45.5, 36, 2.5, HEADER)
textbox(1.0, 45.85, 34.0, 0.7, [[("Code, notebook and tests: ", {"bold": True}), (REPO + "   |   release tag topic7-submission (commit 73adefd)   |   " + EMAIL, {})]],
        size=28, color=WHITE, align=PP_ALIGN.CENTER, after=0)
textbox(1.0, 46.7, 34.0, 0.7, ["Grand Canyon University, College of Engineering and Technology  |  Technology Capstone Showcase  |  Results use simulated data and are not clinically validated."],
        size=24, color="E6D9F5", align=PP_ALIGN.CENTER, after=0)

prs.save(OUT_PPTX)
print(f"saved {OUT_PPTX}\ncolumn ends (in): col1 {col1_end:.1f}, col2 {col2_end:.1f}, col3 {col3_end:.1f} (limit {BOTTOM})")

app = win32com.client.Dispatch("PowerPoint.Application")
try:
    pres = app.Presentations.Open(OUT_PPTX, WithWindow=False)
    pres.SaveAs(OUT_PDF, 32)
    pres.Close()
finally:
    try:
        app.Quit()
    except Exception:
        pass   # PowerPoint sometimes refuses to quit cleanly; the PDF is already written
print("saved", OUT_PDF)
