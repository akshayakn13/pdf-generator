from flask import Flask, request, jsonify
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import tempfile
import base64
import os
import re

app = Flask(__name__)


@app.route("/")
def home():
    return "PDF Generator Running"


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        data = request.get_json()

        html_content = data.get("html", "")

        # Clean HTML tags
        clean_text = re.sub(r"<[^>]+>", "", html_content)

        # Decode HTML entities
        clean_text = (
            clean_text.replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&lt;", "<")
            .replace("&gt;", ">")
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:

            doc = SimpleDocTemplate(pdf_file.name)

            styles = getSampleStyleSheet()

            story = []

            story.append(
                Paragraph(
                    "Social Media Content Calendar",
                    styles["Title"]
                )
            )

            story.append(Spacer(1, 12))

            # Split into sections
            sections = clean_text.split("Day ")

            for section in sections:
                section = section.strip()

                if not section:
                    continue

                story.append(
                    Paragraph(
                        f"Day {section[:1]}",
                        styles["Heading2"]
                    )
                )

                story.append(
                    Paragraph(
                        section,
                        styles["BodyText"]
                    )
                )

                story.append(Spacer(1, 12))

            doc.build(story)

            with open(pdf_file.name, "rb") as f:
                pdf_base64 = base64.b64encode(
                    f.read()
                ).decode("utf-8")

        os.remove(pdf_file.name)

        return jsonify(
            {
                "success": True,
                "pdf_base64": pdf_base64
            }
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "error": str(e)
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
