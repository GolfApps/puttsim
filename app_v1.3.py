import streamlit as st
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="PuttAlign", page_icon="⛳")

st.title("⛳ PuttAlign")
st.markdown("Calculate your Putt Number instantly.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Green Conditions")
distance_ft = st.sidebar.slider("Distance (ft)", 5, 50, 10)
slope_percent = st.sidebar.slider("Side Slope (%)", 0.5, 5.0, 1.0, 0.5)
base_speed = st.sidebar.slider("Green Speed", 1.0, 20.0, 10.0, 0.5)
elevation = st.sidebar.slider("🔻 Downhill --------------(%)----------------- Uphill🔺",-5.0,5.0,0.0,0.5)
pace = st.sidebar.selectbox("Putt Pace:",("Holing speed", "Die speed", "Make speed"))

spd_adj = 1.2
eladj = (elevation *-1)
stimp_speed = base_speed*(spd_adj**eladj)
adj_speed = round(stimp_speed)

if elevation < 0: puttslope = "downhill"
if elevation > 0: puttslope = "uphill"
if elevation == 0: puttslope = "flat"
abselev = abs(elevation)

if pace == "Die speed": past_hole_inches = 3
if pace == "Holing speed": past_hole_inches = 6
if pace == "Make speed": past_hole_inches = 9

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
    return round(np.degrees(np.arctan2(y, d)), 0)

# --- DISPLAY RESULT ---
angle_val = calculate_angle(distance_ft, slope_percent, stimp_speed, past_hole_inches)
angle = int(angle_val)

# Assign putt number value based on angle
if angle == 1: puttval = "3/0+ Inside the hole"
if angle == 2: puttval = "3/1- Edge"
if angle == 3: puttval = "3/1"
if angle == 4: puttval = "4/1"
if angle == 5: puttval = "5/1"
if angle == 6: puttval = "6/1"
if angle == 7: puttval = "3/2+"
if angle == 8: puttval = "4/2"
if angle == 9: puttval = "3/3"
if angle == 10: puttval = "5/2"
if angle == 11: puttval = "6/2-"
if angle == 12: puttval = "4/3"
if angle == 13: puttval = "4/3-"
if angle == 14: puttval = "5/3-"
if angle == 15: puttval = "5/3"
if angle == 16: puttval = "4/4"
if angle == 17: puttval = "4/4+"
if angle == 18: puttval = "6/3"
if angle == 19: puttval = "5/4-"
if angle == 20: puttval = "5/4"
if angle == 21: puttval = "5/4+"
if angle == 22: puttval = "3/7+"
if angle == 23: puttval = "4/6-"
if angle == 24: puttval = "4/6"
if angle == 25: puttval = "5/5"
if angle == 26: puttval = "5/5+"
if angle == 27: puttval = "6/4+"
if angle == 28: puttval = "4/7"
if angle == 29: puttval = "5/4-"
if angle == 30: puttval = "6/5"
if angle > 30: puttval = "Wow Good Luck!"


st.divider()
st.metric(label="Required Aim Angle", value=f"{angle}°")
st.metric(label="Your Putt Number is",value=f"{puttval}")

st.info(f"Targeting {distance_ft}ft putt with {pace}. Side slope {slope_percent}%.")
if abselev > 0: st.info(f"Green Speed {base_speed} on the stimpmeter. Adjusting for {abselev}% {puttslope} using {adj_speed} for estimation.")
if abselev == 0: st.info(f"Green Speed {base_speed} on the stimpmeter.")

# --- Updates to selectbox for pace and updates info box -- 6.29.2026
# --- Updated with adjustments for uphill/downhill putts -- 6.29.2026
