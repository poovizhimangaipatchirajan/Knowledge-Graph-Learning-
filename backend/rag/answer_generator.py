import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.rag.graph_retriever import search_graph
from backend.rag.translator import detect_language

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question):
    # Detect language
    language = detect_language(question)

    search_query = question

    # Translate Tamil -> English for graph retrieval
    if language == "ta":
        translation_prompt = f"""
Translate this Tamil agricultural query into English.

Query:
{question}

Return only the English translation.
"""
        translation_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": translation_prompt
                }
            ]
        )
        search_query = (
            translation_response
            .choices[0]
            .message.content
            .strip()
        )

    # Search Knowledge Graph (Neo4j -> NetworkX fallback)
    graph_data = search_graph(search_query)

    # Top node to pass to UI hierarchy tree
    top_node = graph_data[0] if graph_data else None

    # No results found
    if not graph_data:
        if language == "ta":
            msg = """
மன்னிக்கவும், உங்கள் கேள்விக்கு தொடர்புடைய திட்டத் தகவல் கிடைக்கவில்லை.
வேறு விதமாக கேட்டு முயற்சிக்கவும்.
"""
        else:
            msg = """
Sorry, I could not find any matching scheme information.
Please try rephrasing your question.
"""
        return msg, None

    prompt = f"""
You are the official Iyarkural Farmer Intelligence Assistant.

Detected Language:
{language}

Question:
{question}

Retrieved Scheme Data:
{graph_data}

Instructions:
1. Use ONLY the retrieved scheme data.
2. Do NOT invent information.
3. Mention exact funding amounts whenever available.
4. Mention eligibility if available.
5. Mention the scheme name.
6. Mention the source scheme.
7. Answer completely in Tamil if language = ta.
8. Answer completely in English if language = en.
9. Do not leave sections empty.
10. Keep answer farmer-friendly.

Format:

Scheme Name:
...

Benefits:
...

Eligibility:
...

Funding Pattern:
...

Source:
...
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
You are an Agricultural Government Schemes Assistant.
Use only the retrieved graph data. Never hallucinate.
Always provide:
- Scheme Name
- Benefits
- Eligibility
- Funding Pattern
- Source
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer_text = response.choices[0].message.content
    return answer_text, graph_data


if __name__ == "__main__":
    ans, node = generate_answer("What subsidy is available for maize farmers?")
    print("Answer:\n", ans)
    print("Top Active Node:\n", node)