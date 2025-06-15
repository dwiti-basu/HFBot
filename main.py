import streamlit as st
import requests
import json
import random

# 💬 Page setup
st.set_page_config(page_title="💌 My Memory Bot")

# ✅ ORIGINAL MESSAGE
st.title("💌 My Memory Bot")
st.write("""
This bot reminds Errorgon how much Romi loves him. 💖  
It's on a very emotional mission: to make **Errorgon** finally understand how ridiculously, hopelessly, dramatically much **Romi** loves him.  
Like, *"please don't leave me, you're my whole sky"* kind of love. 💘
""")

# 🔐 TEMP: Hardcoded Hugging Face API key
HF_API_KEY = "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"  # Replace with your actual key
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# 🧠 Load memory data
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

# 🔍 Pick memory based on emotion
def get_memory_by_emotion(emotion):
    matches = [m for m in memory_data["memories"] if emotion.lower() in m["emotion"].lower()]
    return random.choice(matches)["message"] if matches else None

# 🤖 Generate message using Hugging Face
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

    # Debug: Show raw Hugging Face response
    st.write("📡 API Status Code:", response.status_code)
    st.write("🧪 Raw Response:", response.text)

    try:
        result = response.json()
        return result[0]["generated_text"]
    except Exception:
        return "⚠️ Could not extract message. Please check model response or API status."

# ✍️ User input
emotion = st.text_input("How is Errorgon feeling today? (e.g. sad, lonely, angry)")

# 💖 Generate and display love message
if st.button("I love you dont stay angry on me 😢💘"):
    if not emotion:
        st.warning("Please enter an emotion first.")
    else:
        memory = get_memory_by_emotion(emotion)
        if memory:
            reply = generate_reply(emotion, memory)
            st.markdown("### 📝 Generated Message")
            st.success(reply)
        else:
            st.error("No matching memory found for that emotion. Try a different one.")
