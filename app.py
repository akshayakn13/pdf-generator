from flask import Flask, request, jsonify
from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import base64
import os
import re

app = Flask(**name**)

@app.route("/")
def home():
return "PDF Generator Running"

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
try:
data = request.get_json()
html_content = data.get("html", "")

```
    # Remove HTML tags
    text_content = re.sub(r"<[^>]+>", "", html_content)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

        doc = SimpleDocTemplate(pdf_file.name)
        styles = getSampleStyleSheet()

        story = []

        lines = text_content.split("\n")

        for line in lines:
            line = line.strip()

            if not line:
                story.append(Spacer(1, 6))
                continue

            story.append(
                Paragraph(
                    line.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;"),
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 4))

        doc.build(story)

        with open(pdf_file.name, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    os.remove(pdf_file.name)

    return jsonify({
        "success": True,
        "pdf_base64": pdf_base64
    })

except Exception as e:
    return jsonify({
        "success": False,
        "error": str(e)
    }), 500
```

if **name** == "**main**":
app.run(host="0.0.0.0", port=5000)
