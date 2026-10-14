from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from pathlib import Path


def generate_answer_pdf(
    question,
    answer
):

    output_path = Path(
        "frontend/last_answer.pdf"
    )

    doc = SimpleDocTemplate(
        str(output_path)
    )

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "Iyarkural Farmer Intelligence Portal",
            styles["Title"]
        ),

        Spacer(1, 12),

        Paragraph(
            f"<b>Question:</b><br/>{question}",
            styles["BodyText"]
        ),

        Spacer(1, 12),

        Paragraph(
            f"<b>Answer:</b><br/>{answer}",
            styles["BodyText"]
        )

    ]

    doc.build(content)

    return output_path