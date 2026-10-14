from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from pathlib import Path


def export_conversation_pdf(messages):

    output_path = Path(
        "frontend/conversation.pdf"
    )

    doc = SimpleDocTemplate(
        str(output_path)
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Iyarkural Farmer Intelligence Portal",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 12)
    )

    for msg in messages:

        role = msg["role"].capitalize()

        content = msg["content"]

        story.append(
            Paragraph(
                f"<b>{role}</b>",
                styles["Heading3"]
            )
        )

        story.append(
            Paragraph(
                content,
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 8)
        )

    doc.build(story)

    return output_path