import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO

# Define available accents for each gender
ACCENTS = {
    "Male": {
        "English (US)": "en",
        "English (UK)": "en-uk",
        "English (Australia)": "en-au",
        "English (India)": "en-in"
    },
    "Female": {
        "English (US)": "en",
        "English (UK)": "en-uk",
        "English (Australia)": "en-au",
        "English (India)": "en-in"
    }
}

def text_to_speech(text, gender, accent):
    """Convert text to speech with the selected gender and accent, returning an audio buffer."""
    lang_code = ACCENTS[gender][accent]
    tts = gTTS(text=text, lang=lang_code)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def get_audio_download_link(audio_buffer, filename="speech.mp3"):
    """Generate a download link for the generated speech audio file."""
    b64 = base64.b64encode(audio_buffer.read()).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'
    return href

# Streamlit UI
st.set_page_config(page_title="Text-to-Speech", layout="centered")

st.title("🗣️ AI Text-to-Speech Converter")

# Sidebar Configuration
st.sidebar.header("🎙️ Settings")

# Gender Selection (Default: Female)
gender_choice = st.sidebar.radio("Select Gender:", ["Female", "Male"], index=0)

# Accent Selection (Dynamically changes based on gender, Default: US)
accent_choice = st.sidebar.selectbox("Select an Accent:", list(ACCENTS[gender_choice].keys()), index=0)

st.markdown("### Enter your text below:")
user_input = st.text_area("", height=150)

if st.button("🎤 Convert to Speech"):
    if user_input.strip():
        audio_buffer = text_to_speech(user_input, gender_choice, accent_choice)
        st.audio(audio_buffer, format="audio/mp3")
        st.markdown(get_audio_download_link(audio_buffer), unsafe_allow_html=True)
        st.success(f"✅ Speech generated successfully in {gender_choice} ({accent_choice}) accent!")
    else:
        st.warning("⚠️ Please enter some text to convert.")

st.markdown("---")
st.markdown("🔹 *Built with Streamlit & Google Text-to-Speech (gTTS)*")

