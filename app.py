#import streamlit as st
#import pickle
#import string
#import nltk
#from pathlib import Path
#from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
#
## -------------------------------
## App configuration
## -------------------------------
#st.set_page_config(
    #page_title="Shelid AI | Spam Detector",
    #page_icon="📩",
    #layout="centered"
#)
#
#BASE_DIR = Path(__file__).resolve().parent
#VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
#MODEL_PATH = BASE_DIR / "model.pkl"
#
#ps = PorterStemmer()
#
#
## -------------------------------
## Download required NLTK resources
## -------------------------------
#@st.cache_resource
#def setup_nltk():
    #resources = {
        #"tokenizers/punkt": "punkt",
        #"corpora/stopwords": "stopwords",
    #}
#
    #for resource_path, package in resources.items():
        #try:
            #nltk.data.find(resource_path)
        #except LookupError:
            #nltk.download(package, quiet=True)
#
    ## Required by some newer NLTK versions
    #try:
        #nltk.data.find("tokenizers/punkt_tab")
    #except LookupError:
        #nltk.download("punkt_tab", quiet=True)
#
    #return stopwords.words("english")
#
#
## -------------------------------
## Load model and vectorizer
## -------------------------------
#@st.cache_resource
#def load_models():
    #if not VECTORIZER_PATH.exists():
        #raise FileNotFoundError(
            #f"Missing vectorizer file: {VECTORIZER_PATH.name}"
        #)
#
    #if not MODEL_PATH.exists():
        #raise FileNotFoundError(
            #f"Missing model file: {MODEL_PATH.name}"
        #)
#
    #with open(VECTORIZER_PATH, "rb") as file:
        #vectorizer = pickle.load(file)
#
    #with open(MODEL_PATH, "rb") as file:
        #model = pickle.load(file)
#
    #return vectorizer, model
#
#
## -------------------------------
## Text preprocessing
## -------------------------------
#def transform_text(text, english_stopwords):
    #text = text.lower()
    #tokens = nltk.word_tokenize(text)
#
    #cleaned_tokens = []
#
    #for token in tokens:
        #if token.isalnum() and token not in english_stopwords:
            #cleaned_tokens.append(ps.stem(token))
#
    #return " ".join(cleaned_tokens)
#
#
## -------------------------------
## Initialize dependencies
## -------------------------------
#st.title("📩 Shelid AI")
#st.subheader("SMS Spam Detection")
#st.write("Enter a message below to check whether it is spam.")
#
#try:
    #english_stopwords = setup_nltk()
    #tfidf, model = load_models()
#except Exception as error:
    #st.error("Unable to initialize the spam detector.")
    #st.exception(error)
    #st.stop()
#
#
## -------------------------------
## User input and prediction
## -------------------------------
#input_sms = st.text_area(
    #"Enter your message",
    #placeholder="Example: Congratulations! You have won a free prize...",
    #height=150
#)
#
#if st.button("🔍 Predict", type="primary", use_container_width=True):
    #if not input_sms.strip():
        #st.warning("Please enter a message before predicting.")
    #else:
        #try:
            #transformed_sms = transform_text(
                #input_sms, english_stopwords
            #)
#
            #vector_input = tfidf.transform([transformed_sms])
            #result = model.predict(vector_input)[0]
#
            #if result == 1:
                #st.error("🚨 Spam detected!")
                #st.write("This message appears to be spam.")
            #else:
                #st.success("✅ Not Spam")
                #st.write("This message appears to be legitimate.")
#
        #except Exception as error:
            #st.error("Prediction failed. Please check your model and vectorizer.")
            #st.exception(error)


import pickle
import string
from pathlib import Path

import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# --------------------------------------------------
# Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Shield AI | Spam Intelligence",
    page_icon="📩",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"

ps = PorterStemmer()


# --------------------------------------------------
# Custom styling
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080b14;
    --panel: #101625;
    --border: #222b40;
    --text: #f0f4ff;
    --muted: #8995ad;
    --accent: #9b8cff;
    --cyan: #5ee7f5;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMain"] {
    background:
        radial-gradient(ellipse at 50% 0%, #242044 0%, transparent 48%),
        var(--bg);
}

.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    height: 0;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0 65px 0;
}

.brand-icon {
    width: 43px;
    height: 43px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    background: linear-gradient(135deg, #a89bff, #6555e8);
    font-size: 23px;
    box-shadow: 0 0 35px #8475ff35;
}

.brand-name {
    font: 700 21px 'Space Grotesk', sans-serif;
    color: #f4f3ff;
}

.brand-caption {
    color: #8f9ab2;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero {
    text-align: center;
    margin: 0 auto 38px auto;
    max-width: 760px;
}

.eyebrow {
    display: inline-block;
    border: 1px solid #4d477a;
    background: #18162c;
    border-radius: 100px;
    color: #c0b5ff;
    padding: 7px 14px;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 23px;
}

.hero h1 {
    font: 700 clamp(36px, 5.5vw, 62px)/1.12
         'Space Grotesk', sans-serif;
    letter-spacing: -2px;
    margin: 0 0 20px 0;
    color: #f5f6ff;
}

.gradient-text {
    background: linear-gradient(100deg, #a99aff, #72dff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #9aa6bf;
    font-size: 16px;
    line-height: 1.8;
    max-width: 570px;
    margin: auto;
}

.section-label {
    color: #dfe5f8;
    font: 600 17px 'Space Grotesk', sans-serif;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #8793ac;
    font-size: 13px;
    margin-bottom: 20px;
}

[data-testid="stTextArea"] textarea {
    background: #0d1321 !important;
    color: #f0f4ff !important;
    border: 1px solid #2a3550 !important;
    border-radius: 16px !important;
    padding: 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    min-height: 180px;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: #9685ff !important;
    box-shadow: 0 0 0 2px #9685ff20 !important;
}

[data-testid="stTextArea"] label {
    color: #cdd5e8 !important;
}

.stButton > button {
    border-radius: 12px;
    min-height: 49px;
    font-weight: 700;
    border: 1px solid #a397ff;
    background: linear-gradient(110deg, #9a87ff, #7663e8);
    color: white;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: #c7bfff;
    box-shadow: 0 0 25px #8877ff35;
    transform: translateY(-1px);
    color: white;
}

.sample-title {
    color: #c8d1e6;
    font-size: 13px;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
}

div[data-testid="stHorizontalBlock"] {
    gap: 12px;
}

.sample-note {
    color: #77849d;
    font-size: 12px;
    margin-top: 10px;
}

.result {
    margin-top: 28px;
    border-radius: 18px;
    padding: 25px;
    border: 1px solid #303a50;
    background: linear-gradient(135deg, #141d2d, #101522);
}

.result.spam {
    border-color: #813c55;
    background: linear-gradient(135deg, #2b1725, #141522);
}

.result.safe {
    border-color: #246a62;
    background: linear-gradient(135deg, #102b2b, #101722);
}

.result-heading {
    font: 700 23px 'Space Grotesk', sans-serif;
    margin-bottom: 8px;
}

.result-description {
    color: #b0bad0;
    font-size: 14px;
    line-height: 1.7;
}

.result-tag {
    display: inline-block;
    border-radius: 50px;
    padding: 6px 11px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.tag-spam {
    background: #562338;
    color: #ff9eb6;
}

.tag-safe {
    background: #16443e;
    color: #8af1d5;
}

.info-card {
    background: #101625;
    border: 1px solid #222b40;
    border-radius: 16px;
    padding: 22px 18px;
    min-height: 135px;
}

.info-icon {
    font-size: 24px;
    margin-bottom: 12px;
}

.info-heading {
    color: #e7ebfa;
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 7px;
}

.info-description {
    color: #8995ad;
    font-size: 12px;
    line-height: 1.7;
}

.footer {
    text-align: center;
    color: #69758d;
    border-top: 1px solid #1e2637;
    padding-top: 24px;
    margin-top: 65px;
    font-size: 12px;
}

@media (max-width: 640px) {
    .brand {
        margin-bottom: 42px;
    }
    .hero h1 {
        letter-spacing: -1px;
    }
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Load model and vectorizer
# --------------------------------------------------
@st.cache_resource
def load_models():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("model.pkl was not found.")

    if not VECTORIZER_PATH.exists():
        raise FileNotFoundError("vectorizer.pkl was not found.")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    return vectorizer, model


@st.cache_resource
def load_stopwords():
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        return set(stopwords.words("english"))


def transform_text(text, english_stopwords):
    text = text.lower()
    tokens = nltk.word_tokenize(text)

    cleaned_tokens = []

    for token in tokens:
        if token.isalnum() and token not in english_stopwords:
            cleaned_tokens.append(ps.stem(token))

    return " ".join(cleaned_tokens)


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown("""
<div class="brand">
    <div class="brand-icon">✉</div>
    <div>
        <div class="brand-name">Shelid AI</div>
        <div class="brand-caption">Message Intelligence</div>
    </div>
</div>

<div class="hero">
    <div class="eyebrow">✦ &nbsp; AI-POWERED PROTECTION</div>
    <h1>Know what's real.<br>
    <span class="gradient-text">Filter out the noise.</span></h1>
    <p>
        Analyze suspicious SMS messages in seconds.
        Let machine learning help you identify unwanted
        messages before you trust them.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Main application
# --------------------------------------------------
try:
    tfidf, model = load_models()
    english_stopwords = load_stopwords()
except Exception as error:
    st.error(f"Unable to initialize the spam detector: {error}")
    st.stop()


st.markdown(
    '<div class="section-label">Message analyzer</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-subtitle">'
    'Paste an SMS below to analyze its content.</div>',
    unsafe_allow_html=True,
)

# Store input in session state so sample buttons work.
if "sms_input" not in st.session_state:
    st.session_state.sms_input = ""

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "analyzed_message" not in st.session_state:
    st.session_state.analyzed_message = ""


def use_sample(message):
    st.session_state.sms_input = message
    st.session_state.prediction = None


input_sms = st.text_area(
    "Your message",
    key="sms_input",
    height=180,
    placeholder=(
        "e.g. Congratulations! You've won a free prize. "
        "Click here to claim..."
    ),
    max_chars=10000,
    label_visibility="collapsed",
)

st.markdown(
    '<div class="sample-title">TRY A SAMPLE MESSAGE</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    st.button(
        "🎁  Try a spam example",
        key="spam_sample",
        use_container_width=True,
        on_click=use_sample,
        args=(
            "Congratulations! You have won a FREE prize! "
            "Call now to claim your reward.",
        ),
    )

with col2:
    st.button(
        "💬  Try a normal message",
        key="safe_sample",
        use_container_width=True,
        on_click=use_sample,
        args=(
            "Hey, are we still meeting for lunch today? "
            "Let me know when you arrive.",
        ),
    )

st.markdown(
    '<div class="sample-note">'
    'Your messages are processed by the local model in this app. '
    'No external API is used by the prediction code.</div>',
    unsafe_allow_html=True,
)

st.write("")

if st.button(
    "✦   Analyze message",
    type="primary",
    use_container_width=True,
):
    if not input_sms.strip():
        st.warning("Please enter a message before analyzing.")
        st.session_state.prediction = None
    else:
        try:
            transformed_sms = transform_text(
                input_sms, english_stopwords
            )

            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]

            st.session_state.prediction = int(result)
            st.session_state.analyzed_message = input_sms

        except Exception as error:
            st.session_state.prediction = None
            st.error(f"Prediction failed: {error}")


# --------------------------------------------------
# Results
# --------------------------------------------------
if st.session_state.prediction is not None:
    result = st.session_state.prediction

    if result == 1:
        st.markdown("""
        <div class="result spam">
            <div class="result-tag tag-spam">⚠ SPAM DETECTED</div>
            <div class="result-heading">This message looks suspicious.</div>
            <div class="result-description">
                The model classified this message as spam.
                Avoid clicking unknown links or sharing personal
                information until you have verified the sender.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="result safe">
            <div class="result-tag tag-safe">✓ NOT FLAGGED AS SPAM</div>
            <div class="result-heading">No spam detected.</div>
            <div class="result-description">
                The model classified this message as not spam.
                Still verify unexpected requests, links, and
                payment instructions before taking action.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("View analyzed message"):
        st.write(st.session_state.analyzed_message)

    st.caption(
        "This is a machine-learning prediction, not a guarantee. "
        "Results depend on your model's training data and accuracy."
    )


# --------------------------------------------------
# Feature cards
# --------------------------------------------------
st.write("")
st.write("")

st.markdown(
    '<div class="section-label">Built for smarter messaging</div>',
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

features = [
    (
        "⚡",
        "Fast analysis",
        "Get a prediction in seconds using your trained ML model.",
    ),
    (
        "🧠",
        "Machine learning",
        "Text preprocessing and TF-IDF features power classification.",
    ),
    (
        "🛡️",
        "Spam awareness",
        "Spot potentially unwanted messages and stay cautious.",
    ),
]

for col, (icon, heading, description) in zip(
    (c1, c2, c3), features
):
    with col:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-icon">{icon}</div>
                <div class="info-heading">{heading}</div>
                <div class="info-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div class="footer">
    <div style="margin-bottom:8px;color:#a5acc1;">
        ✦ &nbsp; SHELID AI
    </div>
    Built with Python, Streamlit &amp; Scikit-learn
    <br><br>
    AI-assisted classification · Always verify suspicious messages
</div>
""", unsafe_allow_html=True)

