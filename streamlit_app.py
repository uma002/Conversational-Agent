import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO

def text_to_speech(text):
    """Convert text to speech and return audio bytes."""
    tts = gTTS(text=text, lang="en")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def get_audio_download_link(audio_buffer, filename="speech.mp3"):
    """Generate a download link for the audio file."""
    b64 = base64.b64encode(audio_buffer.read()).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'
    return href

# Streamlit UI
st.set_page_config(page_title="Text-to-Speech", layout="centered")

st.title("🗣️ Text-to-Speech Converter")
st.markdown("Enter text below and convert it to speech.")

user_input = st.text_area("Enter your text:", height=150)

if st.button("🎤 Convert to Speech"):
    if user_input.strip():
        audio_buffer = text_to_speech(user_input)
        st.audio(audio_buffer, format="audio/mp3")
        st.markdown(get_audio_download_link(audio_buffer), unsafe_allow_html=True)
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")

st.markdown("---")
st.markdown("🔹 *Built with Streamlit & Google Text-to-Speech (gTTS)*")

