import streamlit as st
import requests
import json
import random

# 🔧 Page configuration
st.set_page_config(page_title="💌 My Memory Bot")

# 🔑 TEMP: Hardcoded Hugging Face API key (DO NOT COMMIT TO GITHUB)
HF_API_KEY = "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"  # Replace with your key
API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# 🧠 Load memory data
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# 🔁 Pick a matching memory
def get_memory_by_emotion(emotion):
    matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
    return random.choice(matches)["message"] if matches else None

# 🤖 Generate a loving message
def generate_reply(emotion, memory):
    prompt = f"""
You are a loving memory bot who knows everything about my love for Errorgon.
Your job is to tell him and express my love when he's feeling {emotion}.
Use the memory below and expand it into a warm, emotional, comforting message full of love and reassurance.

Memory: {memory}
"""
    # Send request to Hugging Face
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt},
        params={"wait_for_model": True}
    )

    # Debug output
    st.write("📡 API Status Code:", response.status_code)
    st.write("🧪 Raw Response:", response.text)

    try:
        output = response.json()
        return output[0]["generated_text"]
    except Exception as e:
        return "⚠️ Could not extract message. The model might not be ready or compatible."

# 🎨 UI
st.title("💌 My Memory Bot")
st.write("This bot is on a very emotional mission: to make **Errorgon** finally understand how ridiculously, hopelessly, dramatically much **Romi** loves him. Like, *'please don't leave me,I'm already emotionally deceased'* levels of love. 💖")

emotion = st.text_input("How am I feeling today? (e.g. sad, angry, lonely)")

if st.button("I love you dont stay angry on me 💘"):
    if not emotion:
        st.warning("Please enter an emotion first.")
    else:
        memory = get_memory_by_emotion(emotion)
        if memory:
            reply = generate_reply(emotion, memory)
            st.markdown("### 💖 Message")
            st.success(reply)
        else:
            st.error("No memory found for that emotion. Try another.")
