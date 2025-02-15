import streamlit as st
from streamlit_audio_recorder import st_audio_recorder
import speech_recognition as sr
import gtts
import tempfile
import os
from pydub import AudioSegment

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Could not request results, check internet connection."

def text_to_speech(text):
    tts = gtts.gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

st.title("Speech Recognition and Text-to-Speech App")

audio_bytes = st_audio_recorder("Record your voice")
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    # Save the recorded audio
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(temp_wav.name, "wb") as f:
        f.write(audio_bytes)

    # Convert to text
    text = recognize_speech(temp_wav.name)
    st.write("Recognized Text:", text)

    # Convert text to speech
    tts_file = text_to_speech(text)
    st.audio(tts_file, format="audio/mp3")

    os.unlink(temp_wav.name)
    os.unlink(tts_file)
