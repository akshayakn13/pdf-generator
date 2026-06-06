from flask import Flask, request, jsonify
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import base64
import os

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    html_content = data.get("html", "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        doc = SimpleDocTemplate(pdf_file.name)
        styles = getSampleStyleSheet()

        story = [Paragraph(html_content, styles["BodyText"])]
        doc.build(story)

        with open(pdf_file.name, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode()

    os.remove(pdf_file.name)

    return jsonify({
        "success": True,
        "pdf_base64": pdf_base64
    })

@app.route("/")
def home():
    return "PDF Generator Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
