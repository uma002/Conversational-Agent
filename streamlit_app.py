import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import requests

def speak(text):
    tts = gTTS(text=text, lang="en")
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Use 'afplay output.mp3' on macOS

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "Could not request results, please check your internet connection."

def main():
    st.title("Speech Recognition and Text-to-Speech App")
    
    if st.button("Start Listening"):
        recognized_text = recognize_speech()
        st.write(f"Recognized Text: {recognized_text}")
        speak(recognized_text)

if __name__ == "__main__":
    main()
