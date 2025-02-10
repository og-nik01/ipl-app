import streamlit as st
import pickle
import pandas as pd
from PIL import Image


st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: url("https://via.placeholder.com/1500x800.png?text=IPL+Background") no-repeat center center fixed;
        background-size: cover;
    }

    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.8);
    }

    .main-title {
        font-family: 'Helvetica', sans-serif;
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #FF5733; /* Vibrant orange */
        background: linear-gradient(90deg, #FF5733, #FFC300, #DAF7A6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subheading {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        color: #DAF7A6; /* Fresh green */
    }
    .stButton > button {
        background-color: #FFC300; /* Bright yellow */
        color: black;
        font-weight: bold;
        font-size: 18px;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: all 0.3s; /* Smooth transition for hover effects */
    }
    .stButton > button:hover {
        background-color: #FF5733; /* Vibrant orange */
        color: white;
    }
    .dropdown-item::before {
        content: "⚡"; /* Custom icon before item */
        color: #4CAF50; /* Green */
    }
    .metrics-card {
        background: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Add background image and a more polished title section
st.markdown("<h1 class='main-title'>IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheading'>Predict your team's victory probability with style!</p>", unsafe_allow_html=True)

# Adding team images
col1, col2 = st.columns(2)

with col1:
    st.image("https://via.placeholder.com/150.png?text=Team+Logo", use_column_width=True, caption="Batting Team")
with col2:
    st.image("https://via.placeholder.com/150.png?text=Team+Logo", use_column_width=True, caption="Bowling Team")

st.markdown("---")  # Division line
teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']
cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']
# Replace dropdown and input sections with styled input boxes
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), key="batting_team")
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams), key="bowling_team")

selected_city = st.selectbox('Select host city', sorted(cities), key="city_select")
target = st.number_input('Target', key="target_input", step=1)

# Score input fields
col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', key="score_input", step=1)
with col4:
    overs = st.number_input('Overs completed', key="overs_input", format="%.2f", step=0.1)
with col5:
    wickets = st.number_input('Wickets out', key="wickets_input", step=1)

# Prediction button
if st.button('Predict Probability', key="predict_button"):
    # Calculations for prediction
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_remaining = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets_remaining],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })
    pipe = pickle.load(open('pipe.pkl', 'rb'))
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    # Display prediction results
    col6, col7 = st.columns(2)
    with col6:
        # Batting Team Win Probability
        st.markdown(
            f"<div class='metrics-card'><h2 style='color:#4CAF50;'>Win Probability</h2>"
            f"<h3>{batting_team}</h3><p>{round(win * 100)}%</p></div>",
            unsafe_allow_html=True,
        )
    with col7:
        # Bowling Team Loss Probability
        st.markdown(
            f"<div class='metrics-card'><h2 style='color:#FF0000;'>Loss Probability</h2>"
            f"<h3>{bowling_team}</h3><p>{round(loss * 100)}%</p></div>",
            unsafe_allow_html=True,
        )
