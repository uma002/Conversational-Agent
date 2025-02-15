import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO
from pydub import AudioSegment

# Define available voice options (gender + accent)
# Note: gTTS does not truly differentiate by gender.
VOICE_OPTIONS = {
    "Female - English (US)": "en",
    "Male - English (US)": "en",
    "Female - English (UK)": "en-uk",
    "Male - English (UK)": "en-uk",
    "Female - English (Australia)": "en-au",
    "Male - English (Australia)": "en-au",
    "Female - English (India)": "en-in",
    "Male - English (India)": "en-in"
}

def text_to_speech(text, voice, slow):
    """
    Convert text to speech using gTTS.
    :param text: Text to convert.
    :param voice: Selected voice option; determines language/accent.
    :param slow: Boolean indicating whether to speak slowly.
    :return: BytesIO buffer containing MP3 audio.
    """
    lang_code = VOICE_OPTIONS[voice]
    tts = gTTS(text=text, lang=lang_code, slow=slow)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def get_audio_download_link(audio_buffer, filename="speech.mp3"):
    """Generate a download link for the generated speech audio file."""
    b64 = base64.b64encode(audio_buffer.read()).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'

# Configure Streamlit page
st.set_page_config(page_title="Text-to-Speech Converter", layout="centered")
st.title("🗣️ Text-to-Speech Converter")

# Sidebar: Voice and Speed selectors
st.sidebar.header("Settings")
voice_choice = st.sidebar.selectbox("Select Voice:", list(VOICE_OPTIONS.keys()), index=0)
speed_choice = st.sidebar.radio("Select Speed:", ["Normal", "Slow"], index=0)
slow_param = True if speed_choice == "Slow" else False

st.markdown("### Enter Text Below:")
user_input = st.text_area("", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        audio_buffer = text_to_speech(user_input, voice_choice, slow_param)
        st.audio(audio_buffer, format="audio/mp3")
        # Provide download link
        st.markdown(get_audio_download_link(audio_buffer), unsafe_allow_html=True)
        st.success(f"✅ Speech generated in {voice_choice} accent at {speed_choice} speed!")
    else:
        st.warning("⚠️ Please enter some text to convert.")

st.markdown("---")
st.markdown("🔹 *Built with Streamlit & gTTS*")
