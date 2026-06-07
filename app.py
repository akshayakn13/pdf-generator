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
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home():
    return "PDF Generator Running"


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json()
        html_content = data.get("html", "")

        soup = BeautifulSoup(html_content, "html.parser")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

            doc = SimpleDocTemplate(pdf_file.name)
            styles = getSampleStyleSheet()

            story = []

            title = soup.find(class_="title")

            if title:
                story.append(
                    Paragraph(title.get_text(strip=True), styles["Title"])
                )
                story.append(Spacer(1, 20))

            days = soup.find_all(class_="day")

            for i, day in enumerate(days):

                story.append(
                    Paragraph(day.get_text(strip=True), styles["Heading1"])
                )

                current = day.find_next_sibling()

                while current and "day" not in current.get("class", []):

                    text = current.get_text(" ", strip=True)

                    if text:
                        story.append(
                            Paragraph(text, styles["BodyText"])
                        )
                        story.append(Spacer(1, 6))

                    current = current.find_next_sibling()

                if i < len(days) - 1:
                    story.append(PageBreak())

            doc.build(story)

            with open(pdf_file.name, "rb") as f:
                pdf_base64 = base64.b64encode(
                    f.read()
                ).decode("utf-8")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
