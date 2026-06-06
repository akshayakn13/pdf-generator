from flask import Flask, request, jsonify
from weasyprint import HTML
import tempfile
import os
import base64

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    data = request.json
    html_content = data.get("html", "")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        HTML(string=html_content).write_pdf(pdf_file.name)

        with open(pdf_file.name, "rb") as f:
            pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

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
