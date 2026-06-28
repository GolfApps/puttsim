
import streamlit as st
import numpy as np
import streamlit as st

from streamlit_mic_recorder import speech_to_text

st.title("PuttSim")

# 1. DEFINE the variable first
voice_data = speech_to_text(language='en', start_prompt="🎙️ Speak", stop_prompt="Stop")

# 2. NOW use the variable
st.write("Debug: Current voice_data variable is:", voice_data)

if voice_data:
    st.success(f"I heard you say: {voice_data}")# --- Sidebar: The Control Center ---
with st.sidebar:
    st.header("Voice Controls")
    # This button sits in the sidebar, perfect for mobile thumbs
    voice_data = speech_to_text(
        language='en', 
        start_prompt="🎙️ Speak Setting", 
        stop_prompt="🛑 Stop"
    )

# --- Logic: Handle the voice input ---
# We initialize our simulation variables
if 'green_speed' not in st.session_state:
    st.session_state.green_speed = 10.0

if voice_data:
    st.sidebar.write(f"Recognized: {voice_data}")
    # Simple parser: look for numbers in the speech
    words = voice_data.lower().split()
    for word in words:
        # If the user says "set speed to 12", this catches "12"
        if word.replace('.','',1).isdigit():
            st.session_state.green_speed = float(word)
            st.sidebar.success(f"Updated to {st.session_state.green_speed}")

# --- Main App: The Simulation ---
st.title("PuttSim")
st.write(f"Current Green Speed: {st.session_state.green_speed}")


# --- PAGE CONFIG ---
st.set_page_config(page_title="PuttAlign", page_icon="⛳")

st.title("⛳ PuttAlign")
st.markdown("Calculate your break angle instantly.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Green Conditions")
distance_ft = st.sidebar.slider("Distance (ft)", 5, 50, 6)
slope_percent = st.sidebar.slider("Side Slope (%)", 0.5, 4.0, 1.0, 0.5)
stimp_speed = st.sidebar.slider("Green Speed", 1, 20, 9)
past_hole_inches = st.sidebar.number_input("Past Hole (inches)", 0, 12, 6)

# --- PHYSICS LOGIC ---
def calculate_angle(d, s, stimp, past_in):
    g = 32.17
    past_ft = past_in / 12
    h_stimp = 11.5 / 12.0
    v_ramp = np.sqrt(2 * g * h_stimp)
    a = v_ramp**2 / (2 * stimp)
    
    d_total = d + past_ft
    v_launch = np.sqrt(2 * a * d_total)
    discriminant = v_launch**2 - 2 * a * d
    T = (v_launch - np.sqrt(max(0, discriminant))) / a
    
    a_lat = g * (s / 100.0)
    y = 0.5 * a_lat * T**2
    return round(np.degrees(np.arctan2(y, d)), 1)

# --- DISPLAY RESULT ---
angle = calculate_angle(distance_ft, slope_percent, stimp_speed, past_hole_inches)

st.divider()
st.metric(label="Required Aim Angle", value=f"{angle}°")
st.info(f"Targeting {distance_ft}ft putt with {slope_percent}% slope at Green Speed of {stimp_speed}.")
