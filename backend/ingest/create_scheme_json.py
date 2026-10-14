import fitz
import re
import json


pdf = fitz.open("data/TamilNadu_30_Schemes.pdf")

schemes = []

for page in pdf:

    txt = page.get_text()

    scheme = {}

    title = re.search(
        r"Scheme Title\/Name:\s*(.*?)(?:Associated Scheme|$)",
        txt,
        re.S
    )

    beneficiary = re.search(
        r"Beneficiaries:\s*(.*?)(?:Types of Benefits|$)",
        txt,
        re.S
    )

    benefit_type = re.search(
        r"Types of Benefits:\s*(.*?)(?:Eligibility criteria|$)",
        txt,
        re.S
    )

    funding = re.search(
        r"Funding Pattern:\s*(.*?)(?:Beneficiaries|$)",
        txt,
        re.S
    )

    description = re.search(
        r"Description:\s*(.*?)(?:Scheme Type|$)",
        txt,
        re.S
    )

    scheme["title"] = (
        title.group(1).strip()
        if title else ""
    )

    scheme["beneficiary"] = (
        beneficiary.group(1).strip()
        if beneficiary else ""
    )

    scheme["benefit_type"] = (
        benefit_type.group(1).strip()
        if benefit_type else ""
    )

    scheme["funding"] = (
        funding.group(1).strip()
        if funding else ""
    )

    scheme["description"] = (
        description.group(1).strip()
        if description else ""
    )

    schemes.append(scheme)

with open(
    "data/schemes.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        schemes,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Saved {len(schemes)} schemes"
)