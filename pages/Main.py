#QUESTION
'''
Problem Statement GAI2: Creative Language Translator
Context:
Beyond literal translation, creative language tools can adapt tone and style. Generative AI can translate text while preserving nuance or even transform writing style (e.g., modern to Shakespearean). This hackathon challenge is to build an AI translator that maintains the original voice and style of the content.

Challenge:
Develop an AI translation system that converts text between languages or writing styles while preserving meaning and tone.

Core Requirements:
- Translate text between at least two languages (e.g., English⇆Spanish) or transform text style (formal to casual, prose to poetry).
- Maintain the original meaning, tone, and style in the output.
- Provide options for specifying target style or dialect.

Bonus Features:
- Support creative rephrasing (e.g., turn input into a poem or song lyrics).
- Include idiomatic or slang translation handling for more natural output.
'''

#bolt.ai or wix.ai

# --- IMPORTS ---
import os
import sys
import io
import pandas as pd
from deep_translator import GoogleTranslator
import streamlit as st
from langdetect import detect
import ollama
import langid

translator = GoogleTranslator()

# --- THEME COLORS ---
PRIMARY = "#18a6fe"
GRADIENT = "linear-gradient(90deg, #18a6fe 0%, #8658fb 100%)"
CARD_BG = "#f1f3f7"
OUTPUT_BG = "#fff"
TEXT_COLOR = "#22272c"
ACCENT_PURPLE = "#8658fb"



# --- LANGUAGE CODES ---
languages = [
    "English", "Spanish", "French", "German", "Italian", "Portuguese", "Russian", "Chinese (Simplified)", "Chinese (Traditional)",
    "Japanese", "Korean", "Arabic", "Hindi", "Bengali", "Turkish", "Vietnamese", "Polish", "Dutch", "Greek", "Hebrew",
    "Thai", "Indonesian", "Romanian", "Ukrainian", "Czech", "Hungarian", "Swedish", "Finnish", "Danish", "Norwegian",
    "Slovak", "Bulgarian", "Serbian", "Croatian", "Malay", "Filipino"
]
lang_code_map = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar",
    "Hindi": "hi",
    "Bengali": "bn",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Polish": "pl",
    "Dutch": "nl",
    "Greek": "el",
    "Hebrew": "he",
    "Thai": "th",
    "Indonesian": "id",
    "Romanian": "ro",
    "Ukrainian": "uk",
    "Czech": "cs",
    "Hungarian": "hu",
    "Swedish": "sv",
    "Finnish": "fi",
    "Danish": "da",
    "Norwegian": "no",
    "Slovak": "sk",
    "Bulgarian": "bg",
    "Serbian": "sr",
    "Croatian": "hr",
    "Malay": "ms",
    "Filipino": "tl"
}

# --- STYLES/DIALECTS ---
default_styles = [
    "None (just translate)", "Formal", "Casual", "Poetic", "Prose",
    "Storytelling", "Academic", "Song Lyrics", "Rap Lyrics", "Shakespearean"
]
language_style_options = {lang: default_styles for lang in languages}
language_dialect_options = {
    "English": [
        "Default", "US English", "UK English", "Australian English", "Canadian English", "Indian English", "South African English"
    ],
    "Spanish": [
        "Default", "Mexican Spanish", "Castilian Spanish", "Latin American Spanish", "Argentinian Spanish", "Colombian Spanish", "Chilean Spanish"
    ],
    "French": [
        "Default", "Metropolitan French", "Canadian French", "Swiss French", "Belgian French", "African French"
    ],
    "German": [
        "Default", "Standard German", "Swiss German", "Austrian German"
    ],
    "Italian": [
        "Default", "Tuscan", "Sicilian", "Neapolitan", "Venetian", "Romanesco"
    ],
    "Portuguese": [
        "Default", "European Portuguese", "Brazilian Portuguese", "African Portuguese"
    ],
    "Russian": [
        "Default", "Moscow Russian", "Saint Petersburg Russian", "Siberian Russian"
    ],
    "Chinese (Simplified)": [
        "Default", "Mainland Mandarin", "Singapore Mandarin"
    ],
    "Chinese (Traditional)": [
        "Default", "Taiwanese Mandarin", "Hong Kong Cantonese", "Macau Cantonese"
    ],
    "Japanese": [
        "Default", "Tokyo Japanese", "Kansai Japanese", "Kyushu Japanese"
    ],
    "Korean": [
        "Default", "Seoul Korean", "Busan Korean", "Jeju Korean"
    ],
    "Arabic": [
        "Default", "Modern Standard Arabic", "Egyptian Arabic", "Levantine Arabic", "Gulf Arabic", "Maghrebi Arabic"
    ],
    "Hindi": [
        "Default", "Khari Boli", "Braj Bhasha", "Awadhi", "Bhojpuri"
    ],
    "Bengali": [
        "Default", "Bangladeshi Bengali", "West Bengali Bengali", "Sylheti"
    ],
    "Turkish": [
        "Default", "Istanbul Turkish", "Anatolian Turkish"
    ],
    "Vietnamese": [
        "Default", "Northern Vietnamese", "Central Vietnamese", "Southern Vietnamese"
    ],
    "Polish": [
        "Default", "Warsaw Polish", "Kraków Polish"
    ],
    "Dutch": [
        "Default", "Netherlands Dutch", "Belgian Dutch (Flemish)"
    ],
    "Greek": [
        "Default", "Athens Greek", "Cypriot Greek"
    ],
    "Hebrew": [
        "Default", "Modern Hebrew", "Biblical Hebrew"
    ],
    "Thai": [
        "Default", "Central Thai", "Northern Thai", "Isan Thai", "Southern Thai"
    ],
    "Indonesian": [
        "Default", "Jakarta Indonesian", "Sumatran Indonesian", "Javanese Indonesian"
    ],
    "Romanian": [
        "Default", "Moldovan Romanian", "Transylvanian Romanian"
    ],
    "Ukrainian": [
        "Default", "Kyiv Ukrainian", "Lviv Ukrainian"
    ],
    "Czech": [
        "Default", "Prague Czech", "Moravian Czech"
    ],
    "Hungarian": [
        "Default", "Budapest Hungarian", "Transylvanian Hungarian"
    ],
    "Swedish": [
        "Default", "Stockholm Swedish", "Gothenburg Swedish", "Scanian"
    ],
    "Finnish": [
        "Default", "Helsinki Finnish", "Western Finnish", "Eastern Finnish"
    ],
    "Danish": [
        "Default", "Copenhagen Danish", "Jutlandic Danish"
    ],
    "Norwegian": [
        "Default", "Bokmål", "Nynorsk"
    ],
    "Slovak": [
        "Default", "Eastern Slovak", "Western Slovak"
    ],
    "Bulgarian": [
        "Default", "Sofia Bulgarian", "Varna Bulgarian"
    ],
    "Serbian": [
        "Default", "Ekavian Serbian", "Ijekavian Serbian", "Torlakian"
    ],
    "Croatian": [
        "Default", "Shtokavian", "Chakavian", "Kajkavian"
    ],
    "Malay": [
        "Default", "Malaysian Malay", "Indonesian Malay", "Singaporean Malay"
    ],
    "Filipino": [
        "Default", "Tagalog", "Cebuano", "Ilocano"
    ]
}

# --- TRANSLATION FUNCTIONS ---

# --- TRANSLATION FUNCTIONS ---
def detect_language(text):
    lang, conf = langid.classify(text)
    return lang

def fast_translate(text, src_lang, tgt_lang):
    src_code = lang_code_map.get(src_lang, "auto") if src_lang != "Auto Detect" else "auto"
    tgt_code = lang_code_map.get(tgt_lang, "en")
    return GoogleTranslator(source=src_code, target=tgt_code).translate(text)

def creative_translate(original, src_lang, tgt_lang, style, dialect, make_idiomatic):
    if style == "None (just translate)":
        return fast_translate(original, src_lang, tgt_lang)
    else:
        extra = ""
        if make_idiomatic:
            extra += f" Use idioms, slang, or expressions common in {tgt_lang} to make the translation feel natural and conversational, if appropriate."
        if dialect and dialect != "Default":
            extra += f" Write in the dialect of {dialect}."
        prompt = (
            f"IMPORTANT: Do not translate, change, explain, or adapt any names or proper nouns (such as people or place names). "
            f"Names like 'M K Vinaykrish' should remain exactly the same in the output, without any modification, translation, or explanation.\n"
            "Respond **only** with the translated text. Do NOT include any additional explanations or comments.\n"
            f"Translate the following text from {src_lang} to {tgt_lang} in a {style} style. "
            "Preserve the original meaning, tone, and style exactly.\n\n"
            f"Text:\n{original}"
        )
        response = ollama.generate(model="phi3", prompt=prompt, stream=False)
        return response["response"].strip()

def do_translation(text, src_lang, tgt_lang, style, dialect, make_idiomatic, verify=True):
    detected_lang = detect_language(text)
    actual_src_lang = src_lang if src_lang != "Auto Detect" else next((lang for lang, code in lang_code_map.items() if code == detected_lang), "English")
    # If verification is requested, the model acts as expert translator
    if verify:
        translation = creative_translate(text, actual_src_lang, tgt_lang, style, dialect, make_idiomatic)
        return translation, actual_src_lang
    else:
        translation = fast_translate(text, actual_src_lang, tgt_lang)
        return translation, actual_src_lang

def get_download_bytes(text, filename="translation.txt"):
    return io.BytesIO(text.encode("utf-8")).getvalue()

def swap_lang_and_texts():
    st.session_state["selected_src_language"], st.session_state["selected_tgt_language"] = \
        st.session_state["selected_tgt_language"], st.session_state["selected_src_language"]
    st.session_state["text_area"], st.session_state["translation"] = \
        st.session_state.get("translation", ""), st.session_state.get("text_area", "")
    
# --- MAIN APP ---

if st.session_state.get("logged_in", False):
    st.set_page_config(page_title="Creative Language Translator", page_icon="🌍", layout='wide', initial_sidebar_state='expanded')

    st.markdown("""
        <style>
        .block-container, .main .block-container {
            padding-top: 0rem !important;
            margin-top: 0rem !important;
        }
        .modern-card {
            margin-top: 0rem !important;
        }
        header[data-testid="stHeader"] {
            height: 0px !important;
            min-height: 0px !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        [data-testid="stToolbar"] {
            min-height: 0px !important;
            height: 0px !important;
            visibility: hidden !important;
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.image("logo2.png")
    st.sidebar.page_link("pages/main.py", label="Home")
    st.sidebar.page_link("pages/history.py", label="History")
    st.sidebar.markdown(f"""
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
        """, unsafe_allow_html=True)

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

    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:48px; font-weight:bold;">Hi, {st.session_state.get("username", "Guest")}</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    # ---- COLUMN 1: Source ----
    with col1:
        st.markdown("#### Source Language")
        src_language_options = ["Auto Detect"] + languages
        if "selected_src_language" not in st.session_state:
            st.session_state["selected_src_language"] = "Auto Detect"
        if "selected_tgt_language" not in st.session_state:
            st.session_state["selected_tgt_language"] = "Spanish"

        selected_src_language = st.selectbox(
            "",
            src_language_options,
            index=src_language_options.index(st.session_state["selected_src_language"]),
            key="src_lang_box"
        )
        st.markdown("""
        <style>
        /* Reduces space between markdown (h4/h5) and the next selectbox */
        .css-1v0mbdj.egzxvld4, .stSelectbox {
            margin-top: -18px !important;  /* Try -18px to -30px as needed */
        }
        </style>
    """, unsafe_allow_html=True)

        st.markdown("#### Target Style")
        style_options = language_style_options.get(selected_src_language if selected_src_language != "Auto Detect" else "English", default_styles)
        selected_style = st.selectbox(
            "",
            style_options,
            key="style_box"
        )

        st.markdown("#### Enter text to translate")
        text_input_value = st.session_state.pop("tmp_text_area", st.session_state.get("text_area", ""))
        text_input = st.text_area("", value=text_input_value, height=123, key="text_area")

        st.markdown("""
        <style>
        .stTextArea {
            margin-top: -1.6em !important;
        }
        </style>
    """, unsafe_allow_html=True)

        idiomatic = st.checkbox("Use idiomatic/slang expressions for natural output", key="idiom_box")
        llm_verify_box = st.checkbox("Use LLM verification for translation accuracy", value=True, key="llm_verify_box")
        translate_clicked = st.button("#### Translate", key="translate_btn")

    # ---- COLUMN 2: Target ----
    with col2:
        st.markdown("#### Target Language")
        target_language_options = [l for l in languages if l != selected_src_language]
        selected_target_language = st.selectbox(
            "",
            target_language_options,
            index=target_language_options.index(st.session_state["selected_tgt_language"]) if st.session_state["selected_tgt_language"] in target_language_options else 0,
            key="tgt_lang_box"
        )
        st.markdown("""
        <style>
        /* Reduces space between markdown (h4/h5) and the next selectbox */
        .css-1v0mbdj.egzxvld4, .stSelectbox {
            margin-top: -18px !important;  /* Try -18px to -30px as needed */
        }
        </style>
    """, unsafe_allow_html=True)

        st.markdown("#### Dialect")
        dialect_options = language_dialect_options.get(selected_target_language, ["Default"])
        selected_dialect = st.selectbox(
            "",
            dialect_options,
            key="dialect_box"
        )

        st.markdown("#### Translated Text")
        output_placeholder = st.empty()
        

    # --- BUTTONS ----
    btn_col1, btn_col2 = st.columns([1, 1], gap="small")

    # --- TRANSLATION LOGIC ---
    if translate_clicked:
        if not text_input.strip():
            output_placeholder.info("Please enter text to translate.")
        else:
            translation, detected_src_lang = do_translation(
                text_input, selected_src_language, selected_target_language,
                selected_style, selected_dialect, idiomatic, verify=llm_verify_box
            )
            st.session_state["translation"] = translation
            st.session_state["translated"] = True
            st.session_state["original"] = text_input
            st.session_state["detected_src_lang"] = detected_src_lang
            df = pd.read_csv("history.csv") if os.path.exists("history.csv") else pd.DataFrame(columns=["Username", "Input", "Input Lang", "Output", "Output Lang", "Output Style", "Output Dialect", "Idiomatic Slang"])
            new_entry = {
                "Username": st.session_state.get("username"),
                "Input": text_input,
                "Input Lang": detected_src_lang,
                "Output": translation,
                "Output Lang": selected_target_language,
                "Output Style": selected_style,
                "Output Dialect": selected_dialect,
                "Idiomatic Slang": bool(idiomatic)
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv("history.csv", index=False)
            # Show result
            output_placeholder.markdown(
                f'<div style="background: {OUTPUT_BG}; color: {TEXT_COLOR}; border-radius: 13px; '
                f'box-shadow: 0 1px 6px #d1d5db33; padding: 1.3em 1.1em 1.3em 1.1em; font-size: 1.11em; min-height: 60px;">'
                f'{translation}</div>',
                unsafe_allow_html=True
            )
    else:
        output_placeholder.markdown(
            f'<div style="background: {OUTPUT_BG}; color: #888; border-radius: 13px; box-shadow: 0 1px 6px #d1d5db22; padding: 1.3em 1.1em 1.3em 1.1em; font-size: 1.07em; min-height: 55px;">'
            f'Your translation will appear here after you click <b>Translate</b>.'
            f'</div>',
            unsafe_allow_html=True
        )

with st.sidebar:
    if st.button("Logout", key="logout"):
        st.session_state["logged_in"] = False
        st.session_state['username'] = None
        st.switch_page("login.py")

#Side Bar color
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color:    #b3ecff;
    }
    </style>
    """,
    unsafe_allow_html=True)


#page bg
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://wallpapers.com/images/featured/plain-blue-dmlktw5iuzdjvb7j.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)