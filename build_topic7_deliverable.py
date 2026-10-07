"""Build the Topic 7 report (DOCX + PDF) from Topic_7_Final_Capstone_Deliverable.md.

The Markdown file is the single source of truth: edit it, then run
    python build_topic7_deliverable.py
Supports headings, paragraphs (**bold**, *italic*, `code`, links), bullets, numbered lists,
pipe tables and figures written as  ![Figure caption](relative/path.png){width=6.0}
"""
import os
import re

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(ROOT, "Topic_7_Final_Capstone_Deliverable.md")
DOCX = os.path.join(ROOT, "Topic_7_Final_Capstone_Deliverable.docx")
PDF = os.path.join(ROOT, "Topic_7_Final_Capstone_Deliverable.pdf")

NAVY, BLUE, INK = RGBColor(31, 78, 121), RGBColor(46, 117, 182), RGBColor(40, 40, 40)
TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*\s][^*]*?\*|`[^`]+`|https?://[^\s)]+)")


def runs(p, text, size=11):
    for tok in TOKEN.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r = p.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("`") and tok.endswith("`"):
            r = p.add_run(tok[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(size - 1.5); r.font.color.rgb = RGBColor(150, 40, 40)
            continue
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = p.add_run(tok[1:-1]); r.italic = True
        elif tok.startswith("http"):
            r = p.add_run(tok); r.font.color.rgb = NAVY; r.font.underline = True
        else:
            r = p.add_run(tok)
        r.font.name = "Calibri"; r.font.size = Pt(size)
        if r.font.color.rgb is None:
            r.font.color.rgb = INK


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    size, color, before = {1: (16, NAVY, 16), 2: (13, NAVY, 14), 3: (11.5, BLUE, 10)}[level]
    p.paragraph_format.space_before, p.paragraph_format.space_after = Pt(before), Pt(6)
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text); r.font.name = "Arial"; r.font.size = Pt(size); r.bold = True; r.font.color.rgb = color


def table(doc, rows):
    header, body = rows[0], rows[2:]            # rows[1] is the |---| separator
    n = len(header)
    t = doc.add_table(rows=1, cols=n); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    by_header = {"ID": [0.4, 1.4, 3.0, 0.75, 0.95], "Step": [1.9, 1.3, 0.5, 2.8], "Slide": [0.5, 3.7, 2.3]}
    widths = by_header.get(header[0].strip(), [6.5 / n] * n)
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed"); tblPr.append(layout)
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]; c.text = ""; shade(c, "1F4E79")
        r = c.paragraphs[0].add_run(h.strip()); r.bold = True; r.font.size = Pt(9); r.font.name = "Calibri"
        r.font.color.rgb = RGBColor(255, 255, 255)
    for k, row in enumerate(body):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            runs(cells[i].paragraphs[0], v.strip(), size=9)
            if k % 2:
                shade(cells[i], "EEF3F8")
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit"); trPr.append(cant)          # keep each row on one page
        for i, w in enumerate(widths):
            row.cells[i].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def figure(doc, caption, path, width):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(os.path.join(ROOT, path), width=Inches(width))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER; c.paragraph_format.space_after = Pt(8)
    runs(c, caption, size=9.5)


def build():
    lines = open(MD, encoding="utf-8").read().split("\n")
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1)
    in_refs, i = False, 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s == "---":
            if s == "---":
                doc.add_paragraph().paragraph_format.space_after = Pt(4)
            i += 1; continue
        if s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append([c for c in lines[i].strip().strip("|").split("|")]); i += 1
            table(doc, block); continue
        m = re.match(r"!\[(.+?)\]\((.+?)\)(?:\{width=([\d.]+)\})?", s)
        if m:
            figure(doc, m.group(1), m.group(2), float(m.group(3) or 6.0)); i += 1; continue
        if s.startswith("### "):
            heading(doc, s[4:], 3)
        elif s.startswith("## "):
            in_refs = "references" in s.lower(); heading(doc, s[3:], 2)
        elif s.startswith("# "):
            in_refs = "references" in s.lower(); heading(doc, s[2:], 1)
        elif in_refs:
            p = doc.add_paragraph(); pf = p.paragraph_format
            pf.left_indent, pf.first_line_indent, pf.space_after, pf.line_spacing = Inches(0.5), Inches(-0.5), Pt(6), 1.15
            runs(p, s)
        elif re.match(r"^(\* |- |\d+\. )", s):
            num = re.match(r"^\d+\. ", s)
            p = doc.add_paragraph(style="List Number" if num else "List Bullet")
            p.paragraph_format.space_after = Pt(3); p.paragraph_format.line_spacing = 1.1
            runs(p, re.sub(r"^(\* |- |\d+\. )", "", s))
        else:
            p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(5); p.paragraph_format.line_spacing = 1.15
            runs(p, s)
        i += 1
    doc.save(DOCX)
    print("DOCX saved:", DOCX)

    import win32com.client
    word = win32com.client.Dispatch("Word.Application"); word.Visible = False
    try:
        d = word.Documents.Open(DOCX)
        d.ExportAsFixedFormat(PDF, 17)
        pages = d.ComputeStatistics(2)
        d.Close(False)
    finally:
        word.Quit()
    print("PDF saved:", PDF, f"({pages} pages)")


if __name__ == "__main__":
    build()
