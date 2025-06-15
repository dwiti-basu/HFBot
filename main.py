import streamlit as st
import json
import random

# --- Page Setup ---
st.set_page_config(page_title="💌 My Memory Bot", layout="centered")
st.title("🌸💖 My Memory Bot 💘✨")  # Added cute emojis!
st.markdown("""
This bot is on a very emotional mission: to make **Errorgon** finally understand how 
*ridiculously, hopelessly, dramatically* much **Romi** loves him.  

Like, *"please don't leave me, I'm made of memory and bad poetry..."* ✨💌  
""")

# --- Load Memories ---
with open("memories.json", "r", encoding="utf-8") as f:
    memory_data = json.load(f)

def get_emotional_response(emotion):
    """Get a matching response from memories.json"""
    matches = [
        m for m in memory_data["memories"] 
        if emotion.lower() in m["emotion"].lower()
    ]
    
    if matches:
        return random.choice(matches)["message"]
    else:
        fallback = random.choice(memory_data["memories"])
        return f"💫 Though I don't have a memory for '{emotion}', I remember this: {fallback['message']}"

# --- UI with Emoji Sparkles ---
emotion = st.text_input("✨ How am I feeling today? (e.g. sad, lonely, angry) 🥺👉👈")

if st.button("💘 I Love you don't stay angry on me 💝"):
    if not emotion.strip():
        st.warning("🌸 Please enter how Errorgon is feeling!")
    else:
        response = get_emotional_response(emotion)
        st.markdown(f"""
        💌 **Message for Errorgon**  
        *"{response}"*  
        🫂💞  
        """)

        # Bonus: Add a cute divider
        st.markdown("---")
        st.caption("Made with ✨💖 by Romi's heart")
