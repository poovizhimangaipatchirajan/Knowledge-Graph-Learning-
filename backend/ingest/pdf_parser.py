import fitz
import json
import re


def extract_schemes(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    schemes = []

    pattern = r"\*\*(\d+)\.\s(.*?)Source:\s(https://.*?)\*\*"

    matches = re.split(pattern, text)

    return matches


if __name__ == "__main__":

    schemes = extract_schemes(
        "data/TamilNadu_30_Schemes.pdf"
    )

    print(len(schemes))
