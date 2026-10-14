import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #ffffff !important;
    background-image: none !important;
    color: #0f172a;
}

header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
}

.main, 
[data-testid="stAppViewContainer"],
section.main {
    background-color: #ffffff !important;
    padding-top: 0 !important;
    margin-top: 0 !important;
    min-height: auto !important;
}

.main .block-container,
div[data-testid="stAppViewBlockContainer"] {
    max-width: 1520px;
    padding-top: 0.5rem !important;
    padding-bottom: 0.2rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
    margin-top: 0 !important;
}

div[data-testid="stVerticalBlock"] > div:first-child {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
}

.feature-chip {
    display: inline-block;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    color: #334155;
    padding: 4px 9px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 2px 2px;
}

.stat-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px 12px;
    margin-bottom: 7px;
}
.stat-title {
    font-size: 0.70rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
}
.stat-val {
    font-size: 1.20rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
    margin-top: 2px;
}

div[data-testid="stMetricValue"] {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
}
div[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
}

.stButton > button {
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.82rem;
    padding: 0.40rem 0.9rem;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    color: #1e293b;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    border-color: #059669;
    color: #059669;
    background: #f0fdf4;
}

div[data-testid="InputInstructions"] {
    display: none !important;
}
.stTextInput {
    margin-bottom: 0 !important;
}
.stTextInput input {
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    font-size: 0.9rem !important;
    height: 44px !important;
    color: #0f172a !important;
}
.stTextInput input:focus {
    border-color: #059669 !important;
    box-shadow: 0 0 0 1px #059669 !important;
}

button[kind="primaryFormSubmit"], div[data-testid="stFormSubmitButton"] > button {
    background: #059669 !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
    height: 44px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
button[kind="primaryFormSubmit"]:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: #047857 !important;
}

div[data-testid="stChatInput"] {
    border-radius: 10px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
}
div[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
}
div[data-testid="stChatInput"]:focus-within {
    border-color: #059669 !important;
    box-shadow: 0 0 0 1px #059669 !important;
}

.footer-paddy-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    margin-top: 0.85rem;
    margin-bottom: 0.4rem;
    border: 1px solid #e2e8f0;
    height: 76px;
    background-size: cover !important;
    background-position: center bottom !important;
    display: flex;
    align-items: center;
    justify-content: center;
}

.footer-paddy-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.92) 0%, rgba(255, 255, 255, 0.45) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
}

.footer-paddy-text {
    position: relative;
    z-index: 2;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1e293b;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.9);
}
</style>
"""

def load_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)