import streamlit as st
import requests
import json
import random

# Page config
st.set_page_config(page_title="💌 My Memory Bot", layout="centered")

# Title
st.title("💌 My Memory Bot")
st.markdown("This bot is on a very emotional mission: to make **Errorgon** finally understand how ridiculously, hopelessly, dramatically much **Romi** loves him. Like, *'please don't leave me, I’m made of memory and bad poetry…'*")

# Load memory data
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# Hugging Face API (hardcoded for simplicity — keep it safe in production!)
HF_API_KEY = "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"  # Replace with your key
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Generate reply using Hugging Face API
def generate_reply(emotion, memory):
    prompt = f"""
You are a loving memory bot who knows everything about my love for Errorgon.
Your job is to tell him and express my love when he's feeling {emotion}.
Use the memory below and expand it into a warm, emotional, comforting message full of love and reassurance.

Memory: {memory}
"""

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={"inputs": prompt},
        params={"wait_for_model": True}
    )

    # Debug info
    st.write("📡 API Status Code:", response.status_code)
    try:
        result = response.json()
        st.write("🧪 Raw Response:", result)
    except Exception as e:
        return f"⚠️ Failed to parse JSON response: {e}"

    # Handle typical output
    if isinstance(result, dict) and "error" in result:
        return f"❌ Hugging Face API Error: {result['error']}"

    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"]

    return "⚠️ Could not extract message. Please check model response or API status."

# UI input
emotion = st.text_input("How is Errorgon feeling today? 😢 (e.g. sad, lonely, angry)")

# Button
if st.button("I Love you don't stay angry on me 💘"):
    if not emotion.strip():
        st.warning("Please enter how Errorgon is feeling.")
    else:
        # Filter memory by emotion
        matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
        memory = random.choice(matches)["message"] if matches else "No specific memory found, but I still love you."

        # Generate and display response
        reply = generate_reply(emotion, memory)
        st.markdown("💖 **Message**")
        st.write(reply)
