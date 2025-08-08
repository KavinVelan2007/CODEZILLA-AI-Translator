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

# --- SIDEBAR ---
st.sidebar.image("logo2.png")  
st.sidebar.page_link("pages/create.py", label="Create account")
st.sidebar.page_link("login.py", label="Login")
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

# --- COLUMNS ---

col1 , col2 , col3 = st.columns(3)

with col2:
    st.title("Create Account")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:", type="password")
    confirm_password = st.text_input("Confirm your password:", type="password")

cols = st.columns(9)

with cols[3]:
    if st.button("Create Account and Login"):
        if password == confirm_password:
            # Here you would typically save the new user to a database
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            try:
                df = pd.read_csv("users.csv")
            except:
                df = pd.DataFrame({"username": [], "password": []})
            if username not in list(df["username"]):
                new_user = pd.DataFrame({"username": [username], "password": [password]})
                df = pd.concat([df, new_user], ignore_index=True)
                try:
                    history_df = pd.read_csv("history.csv")
                except:
                    history_df = pd.DataFrame({"Username": [], "Input": [], "Input Lang": [], "Output": [], "Output Lang": [], "Output Style": [], "Output Dialect": [], "Idiomatic Slang": []})
                df.to_csv("users.csv", index=False)
                history_df.to_csv("history.csv", index=False)
                st.success("Account created successfully!")
                st.session_state['logged_in'] = True
                st.session_state["username"] = username
                st.switch_page("pages/Main.py")
            else:
                st.warning("Account already exists")
        else:
            st.warning("Passwords do not match.")

with cols[5]:
    if st.button("Back to Login"):
        st.switch_page(page="login.py")


# --- SIDEBAR COLOR ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color:    #b3ecff;
    }
    </style>
    """,
    unsafe_allow_html=True)

# --- BACKGROUND COLOR ---

st.markdown(
        """
        <style>
        [data-testid="stHeader"] { 
            background-color:  #FFFFFF ; 
        }
        </style>
        """,##ccf2ff #215e4b
        unsafe_allow_html=True
    )
