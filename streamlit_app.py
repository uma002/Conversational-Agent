import streamlit as st
from gtts import gTTS, gTTSError
import base64
from io import BytesIO

# Define available accent options using the tld parameter
ACCENTS = {
    "English (US)": "com",
    "English (UK)": "co.uk",
    "English (Australia)": "com.au",
    "English (India)": "co.in"
}

def text_to_speech(text, accent_tld, slow=False):
    """
    Convert text to speech using gTTS with the specified accent (via tld) and speed.
    Returns a BytesIO buffer containing MP3 audio.
    """
    try:
        tts = gTTS(text=text, lang="en", tld=accent_tld, slow=slow)
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except gTTSError as e:
        st.error(f"Error generating speech: {e}")
        return None

def get_audio_download_link(audio_buffer, filename="speech.mp3"):
    """
    Generate a download link for the generated speech audio file.
    """
    b64 = base64.b64encode(audio_buffer.read()).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'

# Configure Streamlit page
st.set_page_config(page_title="Text-to-Speech Converter", layout="centered")
st.title("🗣️ Text-to-Speech Converter")
st.markdown("Enter text below to convert to speech. Select an accent from the sidebar.")

# Sidebar: Accent selection and slow speech option
st.sidebar.header("Settings")
accent_choice = st.sidebar.selectbox("Select Accent:", list(ACCENTS.keys()), index=0)
slow_option = st.sidebar.checkbox("Slow Speech", value=False, help="Check to generate speech at a slower pace.")

# Main text input
user_input = st.text_area("Enter your text:", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        accent_tld = ACCENTS[accent_choice]
        audio_buffer = text_to_speech(user_input, accent_tld, slow=slow_option)
        if audio_buffer is not None:
            st.audio(audio_buffer, format="audio/mp3")
            # Generate and display download link
            st.markdown(get_audio_download_link(audio_buffer), unsafe_allow_html=True)
            st.success(f"✅ Speech generated successfully with {accent_choice} accent!")
    else:
        st.warning("⚠️ Please enter some text to convert.")

st.markdown("---")
st.markdown("*Built with Streamlit and Google Text-to-Speech (gTTS)*")
