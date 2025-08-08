# --- IMPORTS ---
import streamlit as st
import pandas as pd

# --- THEME COLORS ---
PRIMARY = "#18a6fe"
GRADIENT = "linear-gradient(90deg, #18a6fe 0%, #8658fb 100%)"
CARD_BG = "#f1f3f7"
OUTPUT_BG = "#fff"
TEXT_COLOR = "#22272c"
ACCENT_PURPLE = "#8658fb"

# --- PAGE CONFIG ---
st.set_page_config(layout="wide")


# --- SIDEBAR ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color:    #b3ecff;
    }
    </style>
    """,
    unsafe_allow_html=True)

st.sidebar.image("logo2.png")  
st.sidebar.page_link("login.py", label="Login")
st.sidebar.page_link("pages/create.py", label="Create account")
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

col1,col2,col3 = st.columns(3)
with col2:
    st.markdown("<h1 style='color: #000000;'>Login or Sign In</h1>", unsafe_allow_html=True) #

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


cols = st.columns(9)
with cols[3]:
    if st.button("Login", key="login_button"):
        if not username or not password:
            st.error("Fill all the fields")
        else: 
            if st.session_state.get("logged_in"):
                st.error("Please logout from the current account")
            else:
                try:
                    df = pd.read_csv("users.csv")
                except:
                    df = pd.DataFrame({"username": [], "password": []})
                if username not in list(df["username"]):
                    st.error("No users found. Please create an account first.")
                else:
                    for i in range(len(df)):
                        if username == df["username"][i] and password == str(df["password"][i]):
                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.success("Login successful!")
                            st.switch_page("pages/Main.py")

with cols[5]:
    if st.button("Create Account", key="create_account_button"):
        st.switch_page(page="pages/create.py")
