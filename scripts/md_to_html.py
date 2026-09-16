import markdown
import pathlib

src = pathlib.Path(r"C:\Users\rajac\Documents\gcu_project\telehealth-hypertension-analytics\docs\analytical_reports_and_visualizations.md")
out = src.with_suffix(".html")

md_text = src.read_text(encoding="utf-8")
body = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analytical Reports and Visualizations</title>
<style>
  body { font-family: Georgia, serif; max-width: 860px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #222; }
  h1 { font-size: 1.8em; border-bottom: 2px solid #333; padding-bottom: 8px; }
  h2 { font-size: 1.3em; margin-top: 2em; border-bottom: 1px solid #ccc; padding-bottom: 4px; }
  blockquote { background: #f4f4f4; border-left: 4px solid #666; margin: 1em 0; padding: 8px 16px; }
  img { max-width: 100%; border: 1px solid #ddd; border-radius: 4px; margin: 8px 0; }
  code { background: #f0f0f0; padding: 2px 5px; border-radius: 3px; font-size: 0.9em; }
  hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #ccc; padding: 6px 12px; }
  th { background: #f0f0f0; }
</style>
</head>
<body>
""" + body + """
</body>
</html>"""

out.write_text(html, encoding="utf-8")
print(f"Written to: {out}")
