import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import wavio
import openai
import os
from gtts import gTTS
import tempfile

# Set OpenAI API Key (Replace with your own API key)
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'

def record_audio(duration=5, fs=44100):
    st.info("Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    st.success("Recording finished!")
    
    # Save recording as WAV
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    wavio.write(temp_wav.name, recording, fs, sampwidth=2)
    return temp_wav.name

def recognize_speech(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech recognition service unavailable."

def generate_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response["choices"][0]["message"]["content"]

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    tts.save(temp_audio.name)
    return temp_audio.name

def main():
    st.title("🎤 Real-Time Conversational AI")
    st.write("Talk to an AI using real-time speech recognition!")
    
    if st.button("Record & Speak"):
        audio_file = record_audio()
        user_input = recognize_speech(audio_file)
        st.write("**You said:**", user_input)
        
        if user_input:
            response = generate_response(user_input)
            st.write("**AI says:**", response)
            
            audio_response = text_to_speech(response)
            st.audio(audio_response, format='audio/mp3')

if __name__ == "__main__":
    main()
