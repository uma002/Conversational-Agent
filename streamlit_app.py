import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import gtts
import os
import tempfile
from scipy.io.wavfile import write

def record_audio(duration=5, samplerate=44100):
    st.info("Recording... Speak now!")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return audio, samplerate

def save_audio(audio, samplerate):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_file.name, samplerate, audio)
    return temp_file.name

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
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

if st.button("Record Audio"):
    audio, samplerate = record_audio()
    audio_file = save_audio(audio, samplerate)
    st.audio(audio_file, format="audio/wav")
    
    text = recognize_speech(audio_file)
    st.write("Recognized Text:", text)
    
    tts_file = text_to_speech(text)
    st.audio(tts_file, format="audio/mp3")
    
    os.unlink(audio_file)
    os.unlink(tts_file)
