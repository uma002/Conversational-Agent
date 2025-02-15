import os
import streamlit as st
from gtts import gTTS
from tempfile import TemporaryFile
import subprocess

# Define stop words
STOP_WORDS = ["quit", "exit", "stop", "bye"]

def speak(text):
    """Convert text to speech using gTTS and play it in real-time"""
    tts = gTTS(text=text, lang='en')
    
    with TemporaryFile() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Try using playsound if available
        try:
            from playsound import playsound
            temp_filename = "temp_audio.mp3"
            with open(temp_filename, "wb") as f:
                f.write(fp.read())
            playsound(temp_filename)
            os.remove(temp_filename)
        except ImportError:
            # Fallback to system call (Linux/macOS)
            try:
                fp.seek(0)
                with open("temp_audio.mp3", "wb") as f:
                    f.write(fp.read())
                subprocess.run(["mpg321", "temp_audio.mp3"], check=True)
                os.remove("temp_audio.mp3")
            except Exception as e:
                st.error(f"Audio playback failed: {e}")

def main():
    st.title("Conversational Agent")
    
    user_input = st.text_input("Enter your message:")
    if st.button("Speak"):
        if user_input.lower() in STOP_WORDS:
            st.write("Exiting...")
        else:
            speak(user_input)
            st.write("Spoken successfully!")

if __name__ == "__main__":
    main()
