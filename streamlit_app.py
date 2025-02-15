import streamlit as st
from gtts import gTTS
import base64
from io import BytesIO
from pydub import AudioSegment

# Define available voice options (accent variants)
VOICE_OPTIONS = {
    "English (US)": "en",
    "English (UK)": "en-uk",
    "English (Australia)": "en-au",
    "English (India)": "en-in"
}

def text_to_speech(text, voice, slow):
    """
    Convert text to speech using gTTS.
    :param text: Text to convert.
    :param voice: Selected voice option (determines language/accent).
    :param slow: Boolean indicating if speech should be slow.
    :return: BytesIO buffer containing MP3 audio.
    """
    lang_code = VOICE_OPTIONS[voice]
    tts = gTTS(text=text, lang=lang_code, slow=slow)
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

def process_speed(audio_buffer, speed_option):
    """
    Adjust playback speed using pydub.
    :param audio_buffer: BytesIO buffer of the original MP3.
    :param speed_option: "Normal", "Fast" or "Slow"
    :return: BytesIO buffer with modified speed.
    """
    if speed_option == "Normal":
        return audio_buffer  # No change
    
    # Load the audio from the buffer
    audio = AudioSegment.from_file(audio_buffer, format="mp3")
    if speed_option == "Fast":
        # Increase speed by 1.5 times
        new_frame_rate = int(audio.frame_rate * 1.5)
    elif speed_option == "Slow":
        # Further slow it down by 0.75 times (gTTS slow parameter already applied if chosen)
        new_frame_rate = int(audio.frame_rate * 0.75)
    
    # Change the frame rate to speed up or slow down playback
    sped_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})
    # Set frame rate back to original to maintain compatibility
    sped_audio = sped_audio.set_frame_rate(audio.frame_rate)
    
    # Export to a new BytesIO buffer
    new_buffer = BytesIO()
    sped_audio.export(new_buffer, format="mp3")
    new_buffer.seek(0)
    return new_buffer

def get_audio_download_link(audio_buffer, filename="speech.mp3"):
    """Generate a download link for the audio file."""
    b64 = base64.b64encode(audio_buffer.read()).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Audio</a>'

# Configure Streamlit page
st.set_page_config(page_title="Text-to-Speech Converter", layout="centered")
st.title("🗣️ Text-to-Speech Converter")

# Sidebar: Single Voice Selector and Speed Selector
st.sidebar.header("Settings")
voice_choice = st.sidebar.selectbox("Select Voice:", list(VOICE_OPTIONS.keys()), index=0)
speed_choice = st.sidebar.radio("Select Speed:", ["Slow", "Normal", "Fast"], index=1)

st.markdown("### Enter Text Below:")
user_input = st.text_area("", height=150)

if st.button("Convert to Speech"):
    if user_input.strip():
        # Determine 'slow' parameter: if "Slow" is selected, set slow=True; otherwise False.
        slow_param = True if speed_choice == "Slow" else False
        
        # Generate base speech audio from text
        audio_buffer = text_to_speech(user_input, voice_choice, slow=slow_param)
        
        # Process speed if "Fast" is selected (if "Slow", we already applied gTTS slow mode)
        if speed_choice == "Fast":
            audio_buffer = process_speed(audio_buffer, "Fast")
        elif speed_choice == "Slow" and slow_param is False:
            # In case user chooses "Slow" via speed selector but hasn't set gTTS slow mode,
            # you can optionally process it here as well.
            audio_buffer = process_speed(audio_buffer, "Slow")
        
        st.audio(audio_buffer, format="audio/mp3")
        # Generate and display download link
        st.markdown(get_audio_download_link(audio_buffer), unsafe_allow_html=True)
        st.success("✅ Speech generated successfully!")
    else:
        st.warning("⚠️ Please enter some text to convert.")

st.markdown("---")
st.markdown("🔹 *Built with Streamlit & gTTS*")
