import streamlit as st
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text):
    """Convert text to speech and play the audio."""
    tts = gTTS(text=text, lang="en")
    audio_buffer = BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    
    # Convert MP3 to WAV for better compatibility
    audio = AudioSegment.from_file(audio_buffer, format="mp3")
    return audio

def main():
    st.title("Text-to-Speech Converter")
    user_input = st.text_area("Enter text to convert to speech:")

    if st.button("Speak"):
        if user_input.strip():
            audio = text_to_speech(user_input)
            audio.export("output.mp3", format="mp3")  # Save audio file
            
            # Play audio in Streamlit
            st.audio("output.mp3", format="audio/mp3")
            st.success("Audio generated successfully!")
        else:
            st.warning("Please enter some text!")

if __name__ == "__main__":
    main()
