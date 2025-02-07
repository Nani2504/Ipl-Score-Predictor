import streamlit as st
import pickle
import numpy as np

# IPL Teams
teams = [
    'Chennai Super Kings', 'Delhi Capitals', 'Kings XI Punjab', 
    'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
    'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
]

team_encoding = {team: idx for idx, team in enumerate(teams)}

# Load the trained model
model_filename = 'ipl_score_predictor.pkl'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Streamlit app
st.title('IPL Score Predictor')

# Input fields
batting_team = st.selectbox('Batting Team', teams)
bowling_team = st.selectbox('Bowling Team', teams)
runs = st.number_input('Runs Scored', min_value=0, max_value=200, value=50)
wickets = st.number_input('Wickets Lost', min_value=0, max_value=10, value=2)
overs = st.number_input('Overs Bowled', min_value=5.0, max_value=20.0, step=0.1, value=10.0)
runs_in_prev_5 = st.number_input('Runs Scored in Last 5 Overs', min_value=0, max_value=50, value=30)
wickets_in_prev_5 = st.number_input('Wickets Lost in Last 5 Overs', min_value=0, max_value=5, value=1)

# Weather conditions
weather = st.selectbox('Weather Condition', ['Clear', 'Rainy', 'Dew'])
weather_impact = 0

if weather == 'Rainy':
    weather_impact = st.slider('Percentage Reduction due to Rain (%)', min_value=0, max_value=50, value=20)
elif weather == 'Dew':
    weather_impact = st.slider('Percentage Increase due to Dew (%)', min_value=0, max_value=50, value=10)

# Convert team names to numeric codes
batting_team_encoded = team_encoding[batting_team]
bowling_team_encoded = team_encoding[bowling_team]

# Prediction
if st.button('Predict Score'):
    input_data = np.array([[batting_team_encoded, bowling_team_encoded, runs, wickets, overs, runs_in_prev_5, wickets_in_prev_5]])
    predicted_score = model.predict(input_data)[0]
    
    if weather == 'Rainy':
        predicted_score *= (1 - weather_impact / 100)
    elif weather == 'Dew':
        predicted_score *= (1 + weather_impact / 100)
    
    st.write(f'Predicted Target Score: {predicted_score:.2f}')
