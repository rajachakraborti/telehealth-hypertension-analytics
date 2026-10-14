import os
import sys
from PIL import Image
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import win32com.client

def build_poster():
    root_dir = r"C:\Users\rajac\Documents\gcu_project\telehealth-hypertension-analytics"
    brain_dir = r"C:\Users\rajac\.gemini\antigravity\brain\f2981cce-e7a9-436b-85ac-b8847e580e9f"
    template_path = r"C:\Users\rajac\Downloads\DSC-590-RS-T8-Benchmark-TechnologyShowcasePosterTemplate.pptx"
    
    out_pptx = os.path.join(root_dir, "Technology_Capstone_Showcase_Poster.pptx")
    out_pdf = os.path.join(root_dir, "Technology_Capstone_Showcase_Poster.pdf")
    
    brain_pptx = os.path.join(brain_dir, "Technology_Capstone_Showcase_Poster.pptx")
    brain_pdf = os.path.join(brain_dir, "Technology_Capstone_Showcase_Poster.pdf")

    # Load from template if exists, else create new 36x48
    if os.path.exists(template_path):
        prs = Presentation(template_path)
        slide = prs.slides[0]
        # Remove old placeholder textboxes, keeping picture if it's the logo
        shapes_to_remove = []
        for s in slide.shapes:
            if s.has_text_frame:
                shapes_to_remove.append(s)
            elif s.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
                # Keep GCU logo
                pass
        for s in shapes_to_remove:
            sp = s._element
            sp.getparent().remove(sp)
    else:
        prs = Presentation()
        prs.slide_width = Inches(36.0)
        prs.slide_height = Inches(48.0)
        slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Color Palette
    NAVY        = RGBColor(20, 48, 107)    # #14306B - Primary Header
    DARK_BLUE   = RGBColor(26, 67, 138)    # #1A438A
    ROYAL_BLUE  = RGBColor(42, 120, 214)   # #2A78D6 - Accent Blue
    ORANGE      = RGBColor(235, 104, 52)   # #EB6834 - Accent Orange
    GREEN       = RGBColor(47, 133, 90)    # #2F855A - Metric Green
    DARK_TEXT   = RGBColor(31, 41, 51)     # #1F2933 - High Contrast Body
    MUTED_TEXT  = RGBColor(82, 96, 109)    # #52606D - Subtitles / Captions
    CARD_BG     = RGBColor(248, 250, 252)  # #F8FAFC - Card Background
    BORDER_COL  = RGBColor(203, 213, 225)  # #CBD5E1 - Card Border
    WHITE       = RGBColor(255, 255, 255)

    # -------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------
    def draw_card(left, top, width, height, title="", title_color=NAVY):
        # Card background rectangle
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = BORDER_COL
        card.line.width = Pt(1.5)
        
        # Header banner inside card
        if title:
            banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(1.1))
            banner.fill.solid()
            banner.fill.fore_color.rgb = title_color
            banner.line.fill.background()
            
            tf = banner.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = Inches(0.3)
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(22)
            p.font.bold = True
            p.font.color.rgb = WHITE
        return card

    def add_text_block(left, top, width, height, paras, size=15, space_after=6):
        box = slide.shapes.add_textbox(left, top, width, height)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.15)
        tf.margin_bottom = Inches(0.15)
        
        for i, item in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(space_after)
            p.line_spacing = 1.15
            
            if isinstance(item, str):
                run = p.add_run()
                run.text = item
                run.font.name = "Calibri"
                run.font.size = Pt(size)
                run.font.color.rgb = DARK_TEXT
            elif isinstance(item, list):
                # Formatted runs: [(text, bold, color, size_override)]
                for r_data in item:
                    txt = r_data[0]
                    bld = r_data[1] if len(r_data) > 1 else False
                    col = r_data[2] if len(r_data) > 2 else DARK_TEXT
                    sz  = r_data[3] if len(r_data) > 3 else size
                    
                    run = p.add_run()
                    run.text = txt
                    run.font.name = "Calibri"
                    run.font.bold = bld
                    run.font.size = Pt(sz)
                    run.font.color.rgb = col
        return box

    def add_image_fitted(path, x, y, max_w, max_h, border=True):
        if not os.path.exists(path):
            return
        iw, ih = Image.open(path).size
        scale = min(max_w / iw, max_h / ih)
        w, h = iw * scale, ih * scale
        px = x + (max_w - w) / 2
        py = y + (max_h - h) / 2
        
        pic = slide.shapes.add_picture(path, px, py, w, h)
        if border:
            pic.line.color.rgb = BORDER_COL
            pic.line.width = Pt(1.0)
        return pic

    # -------------------------------------------------------------
    # 1. TOP HEADER BANNER (Full Width: 36" x 6.2")
    # -------------------------------------------------------------
    header_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(36.0), Inches(6.0))
    header_bg.fill.solid()
    header_bg.fill.fore_color.rgb = NAVY
    header_bg.line.fill.background()

    # Accent Stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(5.85), Inches(36.0), Inches(0.15))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = ORANGE
    stripe.line.fill.background()

    # Re-insert GCU Logo on Header Right
    gcu_logo_path = os.path.join(root_dir, "gcu_logo_extracted.png")
    if os.path.exists(gcu_logo_path):
        slide.shapes.add_picture(gcu_logo_path, Inches(30.6), Inches(0.6), Inches(4.6), Inches(4.6))

    # Title & Metadata in Header
    title_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.5), Inches(29.2), Inches(5.0))
    tf_head = title_box.text_frame
    tf_head.word_wrap = True

    p0 = tf_head.paragraphs[0]
    p0.text = "GRAND CANYON UNIVERSITY  |  COLLEGE OF SCIENCE, ENGINEERING, AND TECHNOLOGY  |  TECHNOLOGY CAPSTONE SHOWCASE"
    p0.font.name = "Arial"
    p0.font.size = Pt(15)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(191, 212, 242) # Light Accent
    p0.space_after = Pt(8)

    p1 = tf_head.add_paragraph()
    p1.text = "Telehealth Hypertension Analytics"
    p1.font.name = "Arial"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(4)

    p2 = tf_head.add_paragraph()
    p2.text = "Continuous Ambulatory Telemetry, Explainable Machine Learning, and Clinical Risk Stratification"
    p2.font.name = "Calibri"
    p2.font.size = Pt(24)
    p2.font.color.rgb = RGBColor(235, 242, 250)
    p2.space_after = Pt(14)

    p3 = tf_head.add_paragraph()
    p3.text = "Author: Raja Chakraborty (Candidate for M.S. in Data Science)   |   Faculty Advisor: Jonathan Pollyn   |   Course: DSC-590   |   Date: October 2026\nGitHub Repository: https://github.com/rajachakraborti/telehealth-hypertension-analytics   |   Release Tag: topic7-submission   |   Commit: 73adefd"
    p3.font.name = "Calibri"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    # -------------------------------------------------------------
    # 3-COLUMN POSTER LAYOUT DEFINITION
    # -------------------------------------------------------------
    # Total width: 36.0", Left margin: 0.8", Right margin: 0.8"
    # Available content width: 34.4". Gutter: 0.6".
    # Col Width = (34.4 - 1.2) / 3 = 11.06" (~11.0")
    COL1_X = Inches(0.8)
    COL2_X = Inches(12.5)
    COL3_X = Inches(24.2)
    COL_W  = Inches(11.0)

    # Content Area: Top = 6.4", Bottom = 47.0" (Height = 40.6")

    # =============================================================
    # COLUMN 1: Clinical Problem, Justification, Requirements
    # =============================================================
    
    # 1. Project Description (Top = 6.4", Height = 11.2")
    draw_card(COL1_X, Inches(6.4), COL_W, Inches(11.2), "1. Project Description")
    col1_desc = [
        [("Clinical Background: ", True, NAVY), 
         ("Cardiovascular disease is the leading global cause of mortality, with hypertension serving as its primary modifiable risk factor. Routine care relies on brief clinical spot-checks, which miss crucial ambulatory dynamics (Whelton et al., 2018).", False, DARK_TEXT)],
        [("Diagnostic Blind Spots in Routine Care:", True, DARK_TEXT)],
        [(" • White-Coat Hypertension: ", True, ORANGE), 
         ("Clinic anxiety temporarily spikes blood pressure in otherwise normotensive patients, leading to overmedication.", False, DARK_TEXT)],
        [(" • Masked Nocturnal Hypertension: ", True, ORANGE), 
         ("Daytime office readings appear normal, while dangerous nocturnal pressure surges go completely unobserved.", False, DARK_TEXT)],
        [("Continuous Telemetry Solution: ", True, NAVY), 
         ("Continuous Ambulatory Blood Pressure Monitoring (ABPM) captures 24-hour physiological telemetry (48 half-hourly readings) to eliminate these diagnostic blind spots.", False, DARK_TEXT)],
        [("Platform Overview: ", True, NAVY), 
         ("This capstone engineered an end-to-end telehealth decision-support platform that ingests 24-hour telemetry, classifies cardiovascular risk into 2017 ACC/AHA diagnostic stages, and delivers real-time explainability via TreeSHAP attributions in under 25 milliseconds.", False, DARK_TEXT)]
    ]
    add_text_block(COL1_X + Inches(0.2), Inches(7.6), COL_W - Inches(0.4), Inches(9.8), col1_desc, size=15)

    # 2. Project Justification (Top = 17.9", Height = 14.8")
    draw_card(COL1_X, Inches(17.9), COL_W, Inches(14.8), "2. Project Justification")
    col1_just = [
        [("The Need for Automated Decision Support:", True, NAVY)],
        [(" • Diagnostic Accuracy Gap: ", True, ORANGE), 
         ("In our 1,800-patient cohort, a single office spot-check misjudged true hypertensive status for ", False, DARK_TEXT), 
         ("25.5% of patients", True, NAVY), 
         (", and standard guideline rules correctly staged only 54.3%.", False, DARK_TEXT)],
        [(" • Frontline Charting Fatigue: ", True, ORANGE), 
         ("Reviewing 48 continuous readings per patient creates severe cognitive fatigue. Automated triage reduces physician review toil by an estimated ", False, DARK_TEXT), 
         ("40%", True, NAVY), 
         (" while flagging borderline cases for manual oversight.", False, DARK_TEXT)],
        [(" • Emergency Event Prevention: ", True, ORANGE), 
         ("Detecting non-dipping patterns and the dangerous ", False, DARK_TEXT), 
         ("Morning Blood Pressure Surge (06:00–10:00 AM)", True, NAVY), 
         (" enables proactive chronotherapy adjustments before stroke or myocardial infarction occurs.", False, DARK_TEXT)]
    ]
    add_text_block(COL1_X + Inches(0.2), Inches(19.1), COL_W - Inches(0.4), Inches(6.8), col1_just, size=15)
    
    # Embed Figure: Office Spot Check vs. True ABPM Status
    fig_office = os.path.join(root_dir, "artifacts/topic6/topic6_fig8_office_vs_abpm.png")
    add_image_fitted(fig_office, COL1_X + Inches(0.5), Inches(25.9), COL_W - Inches(1.0), Inches(6.4))

    # 3. Functional Requirements & Standards (Top = 33.0", Height = 13.8")
    draw_card(COL1_X, Inches(33.0), COL_W, Inches(13.8), "3. Functional Requirements & Standards")
    col1_reqs = [
        [("System Functional Requirements:", True, NAVY)],
        [(" • Telemetry Ingestion: ", True, DARK_TEXT), ("Process 48 half-hourly ambulatory readings across full 24h diurnal windows.", False, DARK_TEXT)],
        [(" • Biomarker Extraction: ", True, DARK_TEXT), ("Calculate Mean Arterial Pressure (MAP), Pulse Pressure, and Dipping Ratio.", False, DARK_TEXT)],
        [(" • Calibrated Risk Staging: ", True, DARK_TEXT), ("Categorize patients into 4 ACC/AHA tiers with verified confidence scores.", False, DARK_TEXT)],
        [(" • Transparent Explainability: ", True, DARK_TEXT), ("Output signed additive TreeSHAP feature attributions for every prediction.", False, DARK_TEXT)],
        [(" • Point-of-Care Latency: ", True, DARK_TEXT), ("Meet a strict <200 ms Service Level Objective (measured compute: ", False, DARK_TEXT), ("22 ms", True, GREEN), (").", False, DARK_TEXT)],
        [("Industry Standards & Compliance:", True, NAVY)],
        [(" • Clinical Guidelines: ", True, ORANGE), ("2017 ACC/AHA Hypertension Standards; TRIPOD+AI reporting guidance.", False, DARK_TEXT)],
        [(" • HIPAA Security Rule: ", True, ORANGE), ("Column-level AES-256 encryption via PostgreSQL pgcrypto, TLS 1.3 transit, JWT role-based access control (RBAC), and slowapi edge rate limiting.", False, DARK_TEXT)],
        [(" • Scientific Integrity: ", True, ORANGE), ("Programmatic Competency 1.2 & 3.3 satisfied; full reproducibility via GitHub commit 73adefd.", False, DARK_TEXT)]
    ]
    add_text_block(COL1_X + Inches(0.2), Inches(34.2), COL_W - Inches(0.4), Inches(12.2), col1_reqs, size=14.5)

    # =============================================================
    # COLUMN 2: Design Process, System Architecture, Model Selection
    # =============================================================

    # 4. Overview of Design Process (Top = 6.4", Height = 19.8")
    draw_card(COL2_X, Inches(6.4), COL_W, Inches(19.8), "4. System Architecture & Design Process")
    col2_design = [
        [("Engineering Lifecycle Framework (CRISP-DM):", True, NAVY)],
        [("The project adhered to an iterative data science engineering cycle: clinical requirements formulation, data simulation with realistic imperfections, cross-validated model selection, security hardening, and deployment verification.", False, DARK_TEXT)],
        [("Decoupled Healthcare Microservices Architecture:", True, NAVY)],
        [(" • React Dashboard (Vercel): ", True, DARK_TEXT), ("Renders diurnal pressure profiles, risk gauges, and interactive TreeSHAP waterfall charts for point-of-care clinicians.", False, DARK_TEXT)],
        [(" • FastAPI Analytics Engine (Render): ", True, DARK_TEXT), ("Executes rapid inference and explainability endpoints (/api/abpm/classify).", False, DARK_TEXT)],
        [(" • PostgreSQL Data Layer: ", True, DARK_TEXT), ("Stores patient records with column-level AES-256 encryption.", False, DARK_TEXT)],
        [(" • MLOps Human-in-the-Loop: ", True, DARK_TEXT), ("Logs doctor overrides; triggers retraining if override rate exceeds 3%.", False, DARK_TEXT)]
    ]
    add_text_block(COL2_X + Inches(0.2), Inches(7.6), COL_W - Inches(0.4), Inches(6.6), col2_design, size=14.5)

    # Embed Figure: System Architecture
    fig_arch = os.path.join(root_dir, "artifacts/topic7/topic7_architecture.png")
    add_image_fitted(fig_arch, COL2_X + Inches(0.4), Inches(14.3), COL_W - Inches(0.8), Inches(11.4))

    # 5. Methodological Rigor & Model Selection (Top = 26.5", Height = 20.3")
    draw_card(COL2_X, Inches(26.5), COL_W, Inches(20.3), "5. Rigorous Model Selection Protocol")
    col2_method = [
        [("Strict Zero-Leakage Cross-Validation Protocol:", True, NAVY)],
        [("Addressing methodological feedback, model selection and hyperparameter searches were conducted strictly via ", False, DARK_TEXT), 
         ("5-fold Stratified Cross-Validation on the 70% development cohort (1,260 patients)", True, NAVY), 
         (". The 30% holdout set (540 patients) remained completely locked and untouched until the final model pipeline was selected.", False, DARK_TEXT)],
        [("Pre-Set Adoption Rules & Nested Cross-Validation:", True, NAVY)],
        [(" • Hyperparameter Search: ", True, GREEN), ("Adopted (lowered log loss by 11.7 SE; held under nested CV).", False, DARK_TEXT)],
        [(" • Feature Engineering: ", True, ROYAL_BLUE), ("Retained for clinical interpretability (MAP, pulse pressure, dipping).", False, DARK_TEXT)],
        [(" • Isotonic Calibration: ", True, ORANGE), ("Rejected (worsened cross-validated log loss and multiplied latency 6x).", False, DARK_TEXT)],
        [(" • Morning Surge Features: ", True, MUTED_TEXT), ("Not adopted for staging (no statistically supported log-loss gain).", False, DARK_TEXT)]
    ]
    add_text_block(COL2_X + Inches(0.2), Inches(27.7), COL_W - Inches(0.4), Inches(6.8), col2_method, size=14.5)

    # Embed Figure: Cross-Validation Selection
    fig_cv = os.path.join(root_dir, "artifacts/topic7/topic7_cv_selection.png")
    add_image_fitted(fig_cv, COL2_X + Inches(0.5), Inches(34.6), COL_W - Inches(1.0), Inches(11.8))

    # =============================================================
    # COLUMN 3: Relevant Data Summaries, Future Recommendations
    # =============================================================

    # 6. Relevant Data Summaries & Empirical Outcomes (Top = 6.4", Height = 22.8")
    draw_card(COL3_X, Inches(6.4), COL_W, Inches(22.8), "6. Relevant Data Summaries & Findings")
    
    # Metric Callout Cards inside Column 3
    # Sub-card 1: Global Accuracy
    c1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, COL3_X + Inches(0.3), Inches(7.6), Inches(5.0), Inches(1.8))
    c1.fill.solid(); c1.fill.fore_color.rgb = WHITE; c1.line.color.rgb = ROYAL_BLUE; c1.line.width = Pt(1.5)
    tf = c1.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "90.2%"; p.font.name = "Arial"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ROYAL_BLUE; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = "Holdout Accuracy (95% CI: 87.4%–92.6%)"; p2.font.size = Pt(11); p2.font.color.rgb = MUTED_TEXT; p2.alignment = PP_ALIGN.CENTER

    # Sub-card 2: Crisis Recall
    c2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, COL3_X + Inches(5.7), Inches(7.6), Inches(5.0), Inches(1.8))
    c2.fill.solid(); c2.fill.fore_color.rgb = WHITE; c2.line.color.rgb = GREEN; c2.line.width = Pt(1.5)
    tf = c2.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "97.0%"; p.font.name = "Arial"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = GREEN; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = "Crisis Recall (<3% False Negatives)"; p2.font.size = Pt(11); p2.font.color.rgb = MUTED_TEXT; p2.alignment = PP_ALIGN.CENTER

    # Sub-card 3: Probability Calibration
    c3 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, COL3_X + Inches(0.3), Inches(9.6), Inches(5.0), Inches(1.8))
    c3.fill.solid(); c3.fill.fore_color.rgb = WHITE; c3.line.color.rgb = ORANGE; c3.line.width = Pt(1.5)
    tf = c3.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "0.014"; p.font.name = "Arial"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = ORANGE; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = "Expected Calibration Error (Brier: 0.148)"; p2.font.size = Pt(11); p2.font.color.rgb = MUTED_TEXT; p2.alignment = PP_ALIGN.CENTER

    # Sub-card 4: Inference Latency
    c4 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, COL3_X + Inches(5.7), Inches(9.6), Inches(5.0), Inches(1.8))
    c4.fill.solid(); c4.fill.fore_color.rgb = WHITE; c4.line.color.rgb = NAVY; c4.line.width = Pt(1.5)
    tf = c4.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = "22 ms"; p.font.name = "Arial"; p.font.size = Pt(28); p.font.bold = True; p.font.color.rgb = NAVY; p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph(); p2.text = "Total Latency (4.2 ms score + 17.8 ms SHAP)"; p2.font.size = Pt(11); p2.font.color.rgb = MUTED_TEXT; p2.alignment = PP_ALIGN.CENTER

    # Benchmark text & Chart
    col3_bench = [
        [("Benchmark Comparisons & Clinical Findings:", True, NAVY)],
        [(" • Guideline Rule Outperformance: ", True, DARK_TEXT), ("The refined model exceeds clinical office and ABPM guideline rules by ", False, DARK_TEXT), ("+24 to +33 percentage points", True, GREEN), (" in accuracy.", False, DARK_TEXT)],
        [(" • Simpler ML Models: ", True, DARK_TEXT), ("Matches Logistic Regression (88.3%) and Default XGBoost (88.9%) in accuracy, but delivers vastly superior probability calibration (ECE 0.014 vs 0.076) and full TreeSHAP explainability.", False, DARK_TEXT)],
        [(" • Error Clustering: ", True, DARK_TEXT), ("70% of misclassifications sit within 5 mmHg of diagnostic boundaries (Elevated vs Stage 1 overlap), reflecting clinical threshold ambiguity rather than model failure.", False, DARK_TEXT)]
    ]
    add_text_block(COL3_X + Inches(0.2), Inches(11.6), COL_W - Inches(0.4), Inches(5.2), col3_bench, size=14)

    # Embed Figure: Benchmark Comparison
    fig_bench = os.path.join(root_dir, "artifacts/topic7/topic7_benchmarks.png")
    add_image_fitted(fig_bench, COL3_X + Inches(0.5), Inches(16.9), COL_W - Inches(1.0), Inches(6.0))

    # Embed Figure: 24h Diurnal Circadian Profiles
    fig_circ = os.path.join(root_dir, "artifacts/topic6/topic6_fig6_circadian.png")
    add_image_fitted(fig_circ, COL3_X + Inches(0.5), Inches(23.1), COL_W - Inches(1.0), Inches(5.8))

    # 7. Recommendations, Limitations & References (Top = 29.5", Height = 17.3")
    draw_card(COL3_X, Inches(29.5), COL_W, Inches(17.3), "7. Future Recommendations & Impact")
    col3_fut = [
        [("Critical Assessment of Technical Limitations:", True, NAVY)],
        [(" • Synthetic Telemetry Bounding: ", True, ORANGE), ("Current evidence uses physiologically bounded synthetic data; the model is not cleared for autonomous clinical diagnosis without multi-center hospital trials.", False, DARK_TEXT)],
        [("Strategic Roadmap for Future Research:", True, NAVY)],
        [(" 1. Deep Waveform Models: ", True, NAVY), ("Transition from summary features to 1D-CNN/LSTM networks processing raw optical photoplethysmography (PPG) waveforms directly from smartwatches.", False, DARK_TEXT)],
        [(" 2. Edge ONNX Compilation: ", True, NAVY), ("Compile XGBoost to lightweight C++ binaries via ONNX Runtime to enable sub-10 ms local inference on microcontrollers without cloud dependency.", False, DARK_TEXT)],
        [(" 3. External Multi-Center Validation: ", True, NAVY), ("Validate against real-world clinical EHR repositories (MIMIC-IV) to evaluate comorbidity fairness (e.g., chronic kidney disease).", False, DARK_TEXT)],
        [(" 4. Conformal Prediction Sets: ", True, NAVY), ("Replace static 65% review thresholds with conformal prediction to output diagnostic sets with rigorous coverage guarantees.", False, DARK_TEXT)],
        [("Selected Key References (APA 7th):", True, NAVY)],
        [("• Collins, G. S., et al. (2024). TRIPOD+AI statement: Updated guidance for clinical prediction models. BMJ, 385, e078378.\n• Lundberg, S. M., et al. (2020). Explainable AI for trees. Nature Machine Intelligence, 2(1), 56–67.\n• Whelton, P. K., et al. (2018). 2017 ACC/AHA blood pressure guideline. JACC, 71(19), e127–e248.", False, MUTED_TEXT, 11.5)]
    ]
    add_text_block(COL3_X + Inches(0.2), Inches(30.7), COL_W - Inches(0.4), Inches(15.8), col3_fut, size=14)

    # -------------------------------------------------------------
    # FOOTER BAR
    # -------------------------------------------------------------
    footer_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(47.3), Inches(36.0), Inches(0.7))
    footer_bar.fill.solid()
    footer_bar.fill.fore_color.rgb = NAVY
    footer_bar.line.fill.background()

    tf_foot = footer_bar.text_frame
    tf_foot.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_foot.margin_left = Inches(0.8)
    p = tf_foot.paragraphs[0]
    p.text = "Grand Canyon University  |  Technology Capstone Showcase  |  Programmatic Competency MS-DS 3.3  |  Open Source Repository: github.com/rajachakraborti/telehealth-hypertension-analytics"
    p.font.name = "Calibri"
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE

    # Save PPTX
    prs.save(out_pptx)
    prs.save(brain_pptx)
    print(f"Poster PPTX saved to: {out_pptx}")
    print(f"Poster PPTX also saved to: {brain_pptx}")

    # Export to PDF via PowerPoint COM
    try:
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        # ppt_app.Visible = True # Needed for some COM versions
        deck = ppt_app.Presentations.Open(out_pptx, WithWindow=False)
        deck.SaveAs(out_pdf, 32) # 32 = ppSaveAsPDF
        deck.SaveAs(brain_pdf, 32)
        deck.Close()
        ppt_app.Quit()
        print(f"Poster PDF exported successfully to: {out_pdf}")
        print(f"Poster PDF also saved to: {brain_pdf}")
    except Exception as e:
        print("Error during PowerPoint COM PDF export:", e)

if __name__ == '__main__':
    build_poster()
