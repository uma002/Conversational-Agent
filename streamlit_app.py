import streamlit as st
import speech_recognition as sr
import requests
import json
import pygame
import io
from gtts import gTTS

# OpenAI API Key (Replace with your own)
API_KEY = "your_api_key_here"
AI_PROMPT = "You are a helpful AI assistant. Respond concisely and informatively."
STOP_WORDS = ["quit", "exit", "stop", "bye"]

# Initialize pygame mixer
pygame.mixer.init()

def speak(text):
    """Convert text to speech using gTTS and play it in real-time"""
    tts = gTTS(text=text, lang="en", slow=False)
    audio_stream = io.BytesIO()
    tts.write_to_fp(audio_stream)
    audio_stream.seek(0)
    
    pygame.mixer.music.load(audio_stream, "mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue  # Wait until speech is finished

def chat_with_ai(user_input):
    """Send user input to OpenAI and return the response"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": AI_PROMPT},
            {"role": "user", "content": user_input},
        ],
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "I'm having trouble connecting to the AI. Please try again later."

def listen_and_respond():
    """Listen to user speech, convert to text, get AI response, and speak it out"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("🎤 Speak now... (Say 'quit' to stop)")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio).lower()
            st.write(f"🗣 You: {user_input}")

            # Check if user wants to exit
            if any(word in user_input for word in STOP_WORDS):
                st.write("👋 Goodbye! See you next time.")
                speak("Goodbye! See you next time.")
                return False  # Stop loop

            ai_response = chat_with_ai(user_input)
            st.write(f"🤖 AI: {ai_response}")
            speak(ai_response)
            return True  # Continue loop

        except sr.UnknownValueError:
            st.write("❌ Couldn't understand. Try again.")
        except sr.RequestError:
            st.write("❌ Speech recognition service unavailable.")

# Streamlit UI
st.title("🗣️ Real-Time Conversational AI")
st.write("Talk to an AI assistant using voice commands!")

if st.button("Start Conversation"):
    continue_conversation = True
    while continue_conversation:
        continue_conversation = listen_and_respond()
