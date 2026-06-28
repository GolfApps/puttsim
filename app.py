import streamlit as st
import numpy as np

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
