import streamlit as st
from utils.functions import get_trainingplan, image_generator
import random
import os


def main():
    # Title
    st.sidebar.title("Run Training Planner 🏃")
    st.sidebar.write("ランニングの練習プランを作成するアプリです。")

    # Input fields
    st.sidebar.header("目標にしているレースについて教えてください。")
    race_days_until = st.sidebar.text_area("レースまでの日数", height=50)
    race_distance = st.sidebar.text_area("距離", height=50)
    race_goaltime = st.sidebar.text_area("目標タイム", height=50)

    st.sidebar.header("現在の走力や練習について教えてください。")
    current_pb = st.sidebar.text_area("目標レース距離の現PB", height=50)
    current_mileage = st.sidebar.text_area("週間走行距離", height=50)
    current_frequency = st.sidebar.text_area("練習頻度", height=50)
    current_vo2max = st.sidebar.text_area("VO2Max", height=50)


    # Submit button
    if st.sidebar.button("Submit"):
        # Process the inputs
        st.session_state.race_days_until = race_days_until
        st.session_state.race_distance = race_distance
        st.session_state.race_goaltime = race_goaltime
        st.session_state.current_pb = current_pb
        st.session_state.current_mileage = current_mileage
        st.session_state.current_frequency = current_frequency
        st.session_state.current_vo2max = current_vo2max

        st.header("You should eat...")
        output = get_trainingplan(race_days_until, race_distance, race_goaltime, current_pb, current_mileage, current_frequency, current_vo2max)

        url = image_generator(output)
        # last_output = output.split("\n")[-2]
        process_inputs(output, url)



def process_inputs(input1, url):
    # Function to display the final output
    # Process the inputs here
    st.write(" ", input1)
    st.image(url, use_column_width=True)


if __name__ == "__main__":
    main()
