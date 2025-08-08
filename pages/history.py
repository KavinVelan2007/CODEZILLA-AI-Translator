import streamlit as st
import pandas as pd

# --- THEME COLORS ---
PRIMARY = "#18a6fe"
GRADIENT = "linear-gradient(90deg, #18a6fe 0%, #8658fb 100%)"
CARD_BG = "#f1f3f7"
OUTPUT_BG = "#fff"
TEXT_COLOR = "#22272c"
ACCENT_PURPLE = "#8658fb"

# --- SIDEBAR ---
st.sidebar.image("logo2.png")  
st.sidebar.page_link("pages/main.py", label="Home")
st.sidebar.page_link("pages/history.py", label="History")
st.markdown(f"""
    <style>
    html, body, .block-container {{
        background: #f5f7fa !important;
    }}
    .modern-card {{
        background: {CARD_BG};
        border-radius: 22px;
        box-shadow: 0 2px 16px #d1d5db33;
        padding: 2.5rem 2rem 2.5rem 2rem;
        margin: 2.5rem auto 2.5rem auto;
        color: {TEXT_COLOR};
    }}
    .stTextArea textarea {{
        background-color: #fff !important;
        border-radius: 13px !important;
        font-size: 1.09rem !important;
        color: {TEXT_COLOR} !important;
    }}
    .stTextInput input, .stSelectbox > div {{
        background-color: #fff !important;
        border-radius: 10px !important;
        font-size: 1.04rem !important;
        color: {TEXT_COLOR} !important;
    }}
    .stButton > button {{
        background: {GRADIENT};
        color: #fff !important;
        border-radius: 13px !important;
        border: none !important;
        font-weight: bold !important;
        padding: 0.8em 2.3em !important;
        margin-top: 1.1em !important;
        box-shadow: 0 2px 6px #0001;
        transition: 0.18s;
    }}
    .st-key-logout {{
        background: #FF000;
        color: #000000;
        padding: 0.8em 2.3em !important;
        
    }}
    .stButton > button:hover {{
        filter: brightness(1.07);
        box-shadow: 0 4px 16px #18a6fe22, 0 2px 16px #8658fb11;
    }}
    </style>
    """, unsafe_allow_html=True)
st.sidebar.markdown(
    f"""
    <div style="color:#444; font-size:1em; color:{PRIMARY}; margin-bottom:1em;">
        <b>Creative Language Translator</b> <br>
        Translate, adapt tone, style, and get creative outputs!
    </div>
    <hr style="margin-top:-0.2em;margin-bottom:1em;">
    <ul style="font-size:0.97em; color:#333; line-height:1.7;">
        <li><b>Languages:</b> 30+ supported</li>
        <li><b>Styles:</b> Formal, Casual, Creative</li>
        <li><b>Bonus:</b> Poem/Song/Prose outputs</li>
        <li><b>AI:</b> LLM-powered review</li>
    </ul>
    """,
    unsafe_allow_html=True
)

if st.session_state.get("logged_in", False):
    st.title("Translation History")
    username = st.session_state.get("username")
    df = pd.read_csv("history.csv")
    out_df = pd.DataFrame({"Username": [], "Input": [], "Input Lang": [], "Output": [], "Output Lang": [], "Output Style": [], "Output Dialect": [], "Idiomatic Slang": []})
    for i in range(len(df)):
        if df["Username"][i] == username:
            out_df = pd.concat([out_df, df.iloc[[i]]], ignore_index=True)
    out_df = out_df.drop(columns=["Username"])
    st.table(out_df)

    with st.sidebar:
        if st.button("Logout", key="logout"):
            st.session_state["logged_in"] = False
            st.session_state['username'] = None
            st.switch_page("login.py")
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color:   #b3ecff;
    }
    </style>
    """,
    unsafe_allow_html=True)
else:
    st.title("You must be logged in to view this page.")