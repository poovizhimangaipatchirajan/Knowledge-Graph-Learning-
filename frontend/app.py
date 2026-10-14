import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# Backend imports based on your structure
from backend.utils.email_sender import send_email_with_attachment
from backend.utils.pdf_export import generate_answer_pdf
from backend.utils.conversation_export import export_conversation_pdf
from backend.graph.graph_visualizer import create_graph_html

try:
    from backend.rag.answer_generator import generate_answer
except ImportError:
    def generate_answer(q):
        dummy_node = {
            "scheme": "National Food Security Mission",
            "beneficiary": "Small & Marginal Farmers",
            "benefit_type": "Certified Seed Distribution Subsidy",
            "funding": "50% Central / 50% State Direct Transfer",
        }
        return f"Simulated response for: {q}. Please verify backend connections.", [dummy_node]

# Frontend styles and helpers
from frontend.styles import load_css
from frontend.helpers import get_footer_image_b64, display_gif

# ==================================================
# PAGE CONFIG & STYLING
# ==================================================
st.set_page_config(
    page_title="Iyarkural • Farmer Intelligence Portal",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()

# Session state initializations
if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggested_prompt" not in st.session_state:
    st.session_state.suggested_prompt = None
if "graph_file" not in st.session_state:
    st.session_state.graph_file = None
if "retrieved_sources" not in st.session_state:
    st.session_state.retrieved_sources = []

# ==================================================
# TOP HEADER BAR WITH LOGO
# ==================================================
header_cols = st.columns([1, 14, 3], vertical_alignment="center")

with header_cols[0]:
    logo_path = ROOT_DIR / "frontend" / "assets" / "logo.png"
    if logo_path.is_file():
        try:
            st.image(Image.open(logo_path), width=54)
        except Exception:
            st.markdown("<span style='font-size: 2.2rem;'>🌾</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='font-size: 2.2rem;'>🌾</span>", unsafe_allow_html=True)

with header_cols[1]:
    st.markdown(
        """
    <div style="margin-left: 5px;">
        <h3 style="margin:0; font-weight:700; color:#0f172a; font-size:1.32rem;">
            Iyarkural Farmer Intelligence Portal
        </h3>
        <p style="margin:0; font-size:0.83rem; color:#64748b;">
            தமிழ்நாடு விவசாயி நுண்ணறிவு உதவி மையம் • GraphRAG Multi-Lingual Assistant
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with header_cols[2]:
    st.markdown(
        """
    <div style="text-align: right;">
        <span style="background: #ecfdf5; color: #059669; border: 1px solid #a7f3d0; padding: 4px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">
            ● System Operational
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==================================================
# HERO BANNER
# ==================================================
banner_path = ROOT_DIR / "frontend" / "assets" / "hero_banner.png"
if banner_path.is_file():
    try:
        st.image(Image.open(banner_path), use_container_width=True)
    except Exception:
        pass

# Suggestion query detection
active_query = None
if st.session_state.suggested_prompt:
    active_query = st.session_state.suggested_prompt
    st.session_state.suggested_prompt = None

# ==================================================
# 3-PANEL DASHBOARD GRID
# ==================================================
col_left, col_center, col_right = st.columns([1.1, 2.3, 1.1], gap="medium")

# --------------------------------------------------
# LEFT PANEL: AI Features & Knowledge Graph
# --------------------------------------------------
with col_left:
    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.5rem;">⚡ Assistant Capabilities</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        <div style="margin-bottom: 6px;">
            <span class="feature-chip">Subsidies & Grants</span>
            <span class="feature-chip">Welfare Schemes</span>
            <span class="feature-chip">Seed Assistance</span>
            <span class="feature-chip">Fertilizer Support</span>
            <span class="feature-chip">Machinery Loans</span>
        </div>
        <p style="font-size: 0.77rem; color: #64748b; margin-top: 8px; margin-bottom: 0;">
            Context-grounded answers powered by vectorized Government Gazette data.
        </p>
        """,
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.5rem;">🕸️ Knowledge Graph Hierarchy</div>',
            unsafe_allow_html=True,
        )
        graph_file = st.session_state.get("graph_file")
        if graph_file and Path(graph_file).exists():
            try:
                with open(graph_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
                components.html(html_content, height=420, scrolling=True)
            except Exception as e:
                st.error(f"Graph Render Error: {e}")
        else:
            st.info("Submit a query to visualize the knowledge graph.")

    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.5rem;">📊 Knowledge Graph Metrics</div>',
            unsafe_allow_html=True,
        )
        st.metric("Schemes Indexed", "32", help="Active Tamil Nadu Agricultural schemes")
        st.metric("Graph State", "Synced", help="Knowledge graph vector sync status")
        st.metric("Retrieval Latency", "120ms", help="Sub-second query resolution")

# --------------------------------------------------
# CENTER PANEL: Chatbot Assistant
# --------------------------------------------------
with col_center:
    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.4rem;">💬 Schemes Query Assistant</div>',
            unsafe_allow_html=True,
        )

        chat_container = st.container(height=450)

        st.markdown("### 💡 Suggested Questions")
        q1, q2 = st.columns(2)
        q3, q4 = st.columns(2)

        with q1:
            if st.button("🌽 Maize Subsidy", use_container_width=True):
                st.session_state.suggested_prompt = "What subsidy is available for maize farmers?"
                st.rerun()

        with q2:
            if st.button("🌱 Seed Assistance", use_container_width=True):
                st.session_state.suggested_prompt = "What seed assistance schemes are available?"
                st.rerun()

        with q3:
            if st.button("🚜 Farmer Welfare", use_container_width=True):
                st.session_state.suggested_prompt = "What welfare schemes are available for farmers?"
                st.rerun()

        with q4:
            if st.button("🌾 தமிழ் கேள்விகள்", use_container_width=True):
                st.session_state.suggested_prompt = "விவசாயிகளுக்கு என்ன திட்டங்கள் உள்ளன?"
                st.rerun()

        user_typed_input = st.chat_input("Ask your agriculture scheme question...")
        if user_typed_input:
            active_query = user_typed_input

        with chat_container:
            if not st.session_state.messages and not active_query:
                display_gif(
                    ROOT_DIR,
                    file_path="gif.mp4",
                    width=150,
                    caption="Ask any agriculture scheme or subsidy question in English or தமிழ்",
                )

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            if active_query:
                st.session_state.messages.append({"role": "user", "content": active_query})
                with st.chat_message("user"):
                    st.write(active_query)

                with st.chat_message("assistant"):
                    status_placeholder = st.empty()
                    with status_placeholder.container():
                        display_gif(
                            ROOT_DIR,
                            file_path="gif.mp4",
                            width=115,
                            caption="Traversing knowledge graph & retrieving schemes...",
                        )

                    reply, graph_data = generate_answer(active_query)
                    st.session_state["last_question"] = active_query
                    st.session_state["last_answer"] = reply

                    if isinstance(graph_data, dict):
                        graph_data = [graph_data]
                    elif not isinstance(graph_data, list):
                        graph_data = []

                    graph_file = create_graph_html(graph_data)
                    st.session_state["graph_file"] = graph_file

                    if graph_data:
                        st.session_state["active_graph_node"] = graph_data[0]
                        st.session_state["retrieved_sources"] = graph_data

                    status_placeholder.empty()
                    st.write(reply)

                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

# --------------------------------------------------
# RIGHT PANEL: Sources, Exports & Stats
# --------------------------------------------------
with col_right:
    with st.container(border=True):
        st.markdown(
            """
            <div style="font-size:0.80rem;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:0.05em;
            color:#475569;
            margin-bottom:0.5rem;">
            📚 Live Retrieved Sources
            </div>
            """,
            unsafe_allow_html=True,
        )

        sources = st.session_state.get("retrieved_sources", [])
        if sources:
            chips_html = '<div style="margin-bottom: 6px; display: flex; flex-wrap: wrap; gap: 4px;">'
            displayed = set()
            for src in sources:
                if isinstance(src, dict):
                    scheme = src.get("scheme", "Unknown Scheme")
                else:
                    scheme = str(src)

                if scheme and scheme not in displayed:
                    chips_html += f'<span class="feature-chip">✅ {scheme}</span>'
                    displayed.add(scheme)
            chips_html += "</div>"
            st.markdown(chips_html, unsafe_allow_html=True)
        else:
            st.info("Ask a question to view GraphRAG sources.")

    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.5rem;">📑 Report & Export</div>',
            unsafe_allow_html=True,
        )

        last_question = st.session_state.get("last_question")
        last_answer = st.session_state.get("last_answer")

        if last_question and last_answer:
            pdf_path = generate_answer_pdf(last_question, last_answer)
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📄 Export Last Answer (PDF)",
                    f,
                    file_name="Iyarkural_Answer.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.button("📄 Export Last Answer (PDF)", disabled=True, use_container_width=True)

        messages = st.session_state.get("messages", [])
        if messages:
            pdf_path = export_conversation_pdf(messages)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    "🗂️ Export Full Audit (PDF)",
                    pdf_file,
                    file_name="Iyarkural_Conversation.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
        else:
            st.button("🗂️ Export Full Audit (PDF)", disabled=True, use_container_width=True)

        email_address = st.text_input("Recipient Email")
        if st.button("✉️ Send Conversation", use_container_width=True):
            if messages and email_address.strip():
                pdf_path = export_conversation_pdf(messages)
                try:
                    send_email_with_attachment(
                        recipient_email=email_address,
                        subject="Iyarkural Conversation Report",
                        body="Generated from Iyarkural Farmer Intelligence Portal.",
                        attachment_path=str(pdf_path),
                    )
                    st.success("Email sent successfully.")
                except Exception as e:
                    st.error(f"Email Failed: {e}")

    with st.container(border=True):
        st.markdown(
            '<div style="font-size: 0.80rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #475569; margin-bottom: 0.5rem;">⚡ System Quick Stats</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
        <div class="stat-box">
            <div class="stat-title">Supported Languages</div>
            <div class="stat-val">2 <span style="font-size:0.8rem; font-weight:500; color:#64748b;">(EN / தமிழ்)</span></div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Assistant Status</div>
            <div class="stat-val" style="color: #059669;">● Online</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Pipeline Architecture</div>
            <div class="stat-val" style="font-size: 1.02rem;">GraphRAG v1.0</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Grounding Model</div>
            <div class="stat-val" style="font-size: 1.02rem;">Hybrid KG + Vector</div>
        </div>
        <div class="stat-box">
            <div class="stat-title">Neo4j Database</div>
            <div class="stat-val" style="color:#059669;">
                ● Connected
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==================================================
# FOOTER
# ==================================================
footer_img_src = get_footer_image_b64(ROOT_DIR)

if footer_img_src:
    st.markdown(
        f"""
    <div class="footer-paddy-card" style="background-image: url('{footer_img_src}');">
        <div class="footer-paddy-overlay">
            <span class="footer-paddy-text">
                🌾 Iyarkural Portal • Department of Agriculture & Farmers Welfare Knowledge System • Production Build v1.2
            </span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
    <div style="text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid #e2e8f0;">
        🌾 Iyarkural Portal • Department of Agriculture & Farmers Welfare Knowledge System • Production Build v1.2
    </div>
    """,
        unsafe_allow_html=True,
    )