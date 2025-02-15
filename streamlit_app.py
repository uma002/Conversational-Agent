import streamlit as st
import speech_recognition as sr
import pyttsx3
import requests
import json

# OpenRouter API Key (Replace with your actual key)
API_KEY = "your_openrouter_api_key"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# AI Tutor Prompt
AI_PROMPT = """You are an intelligent and friendly AI English conversation tutor. 
Your goal is to help users improve their spoken English skills through natural and engaging conversations. 

Here’s how you should behave:
- **Topic Selection**: If the user provides a topic, follow their lead. If not, choose an engaging and useful topic.
- **Adaptive Difficulty**: Adjust vocabulary and grammar complexity based on the user's proficiency.
- **Conversational Flow**: Keep conversations natural with open-ended questions and follow-up prompts.
- **Corrections & Feedback**: Correct mistakes politely and provide explanations with examples.
- **Encouragement & Engagement**: Motivate the user and simplify complex discussions if needed.
- **Interactive Learning**: Introduce role-playing scenarios (e.g., ordering food, job interviews).
- **Grammar & Vocabulary Expansion**: Teach new words, phrases, and idioms naturally.
- **Personalization**: Incorporate user interests and remember past interactions.
- **Patience & Friendliness**: Always be supportive and never rush the user.
- **Cultural Awareness**: Explain cultural nuances when necessary.
"""

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to chat with AI
def chat_with_ai(user_input):
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

# Streamlit UI
st.title("AI English Conversation Tutor")
st.write("Practice your English conversation skills with an AI tutor.")

# User input (text-based)
user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    ai_response = chat_with_ai(user_input)
    st.write(f"**AI:** {ai_response}")
    speak(ai_response)

# Speech recognition
recognizer = sr.Recognizer()
if st.button("🎤 Speak Now"):
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            user_speech = recognizer.recognize_google(audio)
            st.write(f"🗣 You: {user_speech}")
            
            ai_response = chat_with_ai(user_speech)
            st.write(f"**AI:** {ai_response}")
            speak(ai_response)
        except sr.UnknownValueError:
            st.write("❌ Couldn't understand. Try again.")
        except sr.RequestError:
            st.write("❌ Speech recognition service unavailable.")

# Update requirements.txt file
with open("requirements.txt", "w") as f:
    f.write("""streamlit\nspeechrecognition\npyttsx3\nrequests\nffmpeg\n""")
