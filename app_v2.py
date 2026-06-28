
import numpy as np
import re
import streamlit as st
from streamlit_mic_recorder import speech_to_text

# 1. Update the initialization logic to include the new range
if 'length' not in st.session_state:
    st.session_state.length = 5.0 # Start at the minimum

# 2. Add a safety check to ensure it stays in bounds (5 to 50)
if st.session_state.length < 5.0:
    st.session_state.length = 5.0
elif st.session_state.length > 50.0:
    st.session_state.length = 50.0

# 3. Update the slider definition to match
st.slider("Distance", 5.0, 50.0, key='length')

# 1. Update the initialization logic to include the new range
if 'length' not in st.session_state:
    st.session_state.length = 5.0 # Start at the minimum

# 2. Add a safety check to ensure it stays in bounds (5 to 50)
if st.session_state.length < 5.0:
    st.session_state.length = 5.0
elif st.session_state.length > 50.0:
    st.session_state.length = 50.0

# 3. Update the slider definition to match
st.slider("Distance", 5.0, 50.0, key='length')
# 1. Initialize ALL variables in session_state
defaults = {"length": 10, "speed": 10.0, "slope": 0.0, "firmness": 6.0}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# st.title("PuttSim - Multi-Sync")

# 2. Voice Input
voice_input = speech_to_text(language='en', start_prompt="🎙️ Say commands", stop_prompt="Stop")

# 3. Dynamic Loop Parser
if voice_input:
    text = voice_input.lower()
    for key in defaults.keys():
        # Look for: "speed 12", "slope 5", etc.
        pattern = rf"{key}\s*(?:to|is|=)?\s*(-?\d*\.?\d+)"
        match = re.search(pattern, text)
        if match:
            st.session_state[key] = float(match.group(1))
            st.success(f"Updated {key} to {st.session_state[key]}")

# 4. Display Sliders (Automatically bound to state)
# Each slider updates its respective key in st.session_state
st.slider("Green Speed", 0.0, 20.0, key='speed')
st.slider("Slope Degree", -10.0, 10.0, key='slope')
st.slider("Distance", 0.0, 1.0, key='length')
st.slider("Ball Hardness", 0.0, 2.0, key='hardness')

# 5. Calculation Step
# This will always use the latest values from sliders OR voice
result = (st.session_state.speed * 1.5) + (st.session_state.slope * 0.5)
st.write(f"### Simulation Result: {result}")

# 5. Calculation Step
# This will always use the value, regardless of whether it came from the slider or voice
result = st.session_state.speed * 1.5
st.write(f"### Simulation Result: {result}")
    
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
