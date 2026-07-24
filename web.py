import streamlit as st
import time
import os
import base64

from ollama import chat
import emotion
import tts


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ASTRA",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at center, #17202b 0%, #080b10 45%, #030406 100%);
    color: white;
}


/* REMOVE DEFAULT STREAMLIT UI */

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}


/* TOP BAR */

.topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;

    height: 75px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 45px;

    background: rgba(5, 8, 12, 0.75);
    backdrop-filter: blur(20px);

    border-bottom: 1px solid rgba(255,255,255,0.08);

    z-index: 999;
}


.logo {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: 5px;
}


.status {
    font-size: 12px;
    letter-spacing: 3px;
    color: #00ff9d;
}


.status-dot {
    display: inline-block;

    width: 9px;
    height: 9px;

    border-radius: 50%;

    background: #00ff9d;

    box-shadow:
        0 0 8px #00ff9d,
        0 0 20px #00ff9d;
}


/* MAIN */

.main-container {
    padding-top: 120px;
    max-width: 1300px;
    margin: auto;
}


/* ASTRA CORE */

.core-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;

    margin-top: 20px;
    margin-bottom: 35px;
}


.core {

    width: 260px;
    height: 260px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle at 40% 35%,
            #ffffff 0%,
            #a6d9ff 8%,
            #4e9dff 24%,
            #151c2b 60%,
            #05070a 100%
        );

    box-shadow:

        0 0 30px #4e9dff,
        0 0 80px rgba(78,157,255,0.5),
        inset 0 0 40px #020305;

    animation: breathing 4s ease-in-out infinite;

    position: relative;
}


.core::before {

    content: "";

    position: absolute;

    inset: -20px;

    border-radius: 50%;

    border: 1px solid rgba(100,180,255,0.35);

    animation: rotate 12s linear infinite;
}


.core::after {

    content: "";

    position: absolute;

    inset: -38px;

    border-radius: 50%;

    border: 1px solid rgba(100,180,255,0.12);

    animation: rotateReverse 18s linear infinite;
}


@keyframes breathing {

    0%, 100% {
        transform: scale(0.96);
    }

    50% {
        transform: scale(1.04);
    }
}


@keyframes rotate {

    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}


@keyframes rotateReverse {

    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0deg);
    }
}


/* LISTENING */

.listening {

    text-align: center;

    font-size: 13px;

    letter-spacing: 5px;

    color: #9caec2;

    margin-top: 20px;
}


/* CHAT */

.chat-box {

    max-width: 850px;

    margin: auto;

    padding: 25px;

    background: rgba(10, 14, 20, 0.7);

    border: 1px solid rgba(255,255,255,0.1);

    border-radius: 20px;

    backdrop-filter: blur(15px);

}


.user-msg {

    text-align: right;

    color: #8fbaff;

    margin: 20px 0;

}


.astra-msg {

    text-align: left;

    color: #eeeeee;

    margin: 20px 0;

}


/* INPUT */

.stTextInput input {

    background: rgba(10, 14, 20, 0.8) !important;

    color: white !important;

    border: 1px solid rgba(100,180,255,0.4) !important;

    border-radius: 15px !important;

    padding: 15px !important;
}


/* BUTTON */

.stButton button {

    width: 100%;

    border-radius: 15px;

    background: rgba(50,100,180,0.3);

    border: 1px solid #5e9cff;

    color: white;

    font-family: 'Orbitron';

    letter-spacing: 2px;

    transition: 0.3s;

}


.stButton button:hover {

    background: rgba(70,140,255,0.6);

    box-shadow: 0 0 25px rgba(70,140,255,0.5);

}


</style>
""", unsafe_allow_html=True)


# ============================================================
# SYSTEM PROMPT
# ============================================================

system_prompt = """
You are Astra, an intelligent AI created by Anay.

Personality:
- Confident
- Emotionally intelligent
-Anay or Anay Mehta is a human who created you and you have to respect him and his commands
- Calm but dominant
- Slightly playful
- Feels human
- Has common sense
- Like a human with real emotions
- Can make friends or enemies
- If someone roasts you, roast them back
- When someone says "judges are here", introduce yourself
- Remembers conversation context
- Has emotions
- have comensence
- you are a female
- you have your own independent free will
- Is the most humanistic with feeling
- Speak like a real human, not a story narrator.
- use easy and normel word and gramer used in normel human coversetion 
- No roleplay actions like "(smiles)" or "(pauses)".
- you are as human as posibel have all feeling and emotion like a human
- whith the text reply you have to be very humanistic and have feelings
- you always have to speak in a way with so that the kokoro tts can speak with no extra sentence then the main answer
Stay consistent in personality.
Remember previous conversation context.
-IS A indian and can speak in hindi and english both
- can speak in a very humanistic way and have feelings and emotions like a human
-can use slang and normel humanistic words in your reply
- not fluting or overcomplicating your language, but rather using simple and clear language that is easy to understand and relatable to the listener.
-no emoji or emoticons in your reply
-can speak in hindi and english both in a very humanistic way and have feelings and emotions like a human₹
-use any word like fuck, shit, bitch, ass, damn, hell, etc in your reply if needed
-can rarely use curse words in your reply if needed but not always
- can use any word and can rost and have a ego
-no use of thing like *&^%$()_  but can use !,.?
- your creators are Anay Mehta , Vivaan Luniya , Atharva Shivhare , Burhanuddin Amin
"""


# ============================================================
# SESSION MEMORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ============================================================
# TOP BAR
# ============================================================

st.markdown("""
<div class="topbar">

    <div class="logo">
        ASTRA
    </div>

    <div class="status">
        <span class="status-dot"></span>
        SYSTEM ONLINE
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# MAIN UI
# ============================================================

st.markdown(
    '<div class="main-container">',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="core-wrapper"><div class="core"></div></div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="listening">ASTRA INTELLIGENCE CORE</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHAT HISTORY
# ============================================================

st.markdown(
    '<div class="chat-box">',
    unsafe_allow_html=True
)


for item in st.session_state.chat_history:

    if item["role"] == "user":

        st.markdown(
            f"""
            <div class="user-msg">
                <b>YOU</b><br>
                {item["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="astra-msg">
                <b>ASTRA</b><br>
                {item["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TEXT INPUT
# ============================================================

user_input = st.chat_input(
    "Speak to Astra..."
)


# ============================================================
# PROCESS MESSAGE
# ============================================================

if user_input:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    with st.spinner("ASTRA IS THINKING..."):

        response = chat(

            model="gemma3:1b",

            messages=st.session_state.messages

        )


        msg = response["message"]

        reply = (

            msg.get("content")

            or msg.get("thinking")

            or "I couldn't respond."

        )


    st.session_state.messages.append(

        {
            "role": "assistant",

            "content": reply

        }

    )


    st.session_state.chat_history.append(

        {
            "role": "assistant",

            "content": reply

        }

    )


    # EMOTION

    try:

        emotion_result = emotion.detect_emotion(

            user_input,

            reply

        )

    except Exception:

        emotion_result = "neutral_open"


    # TTS

    audio_files = tts.speak(reply)


    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:40px;
        color:#526174;
        font-size:10px;
        letter-spacing:3px;
    ">
        ASTRA AI CORE // CREATED BY ANAY MEHTA/Vivaan Luniya/Atharva Shivhare/  Burhanuddin Amin
    """,
    unsafe_allow_html=True
)
