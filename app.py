import streamlit as st
from utils.functions import get_trainingplan
import random
import os
from datetime import datetime


def main():
    # Title
    st.sidebar.title("Run Training Planner 🏃")
    st.sidebar.write("ランニングの練習プランを作成するアプリです。")

    # Input fields
    st.sidebar.header("目標にしているレースについて教えてください。")

    race_distance = st.sidebar.selectbox("距離", ['5K', '10K', '21.1km（ハーフ）', '30K', '42.2km（フル）', '100km（ウルトラ）', 'その他（入力）'])
    if race_distance == 'その他（入力）':
        race_distance = st.sidebar.text_input("その他の距離を入力してください。")
        # add llm generate function that spits out 'you're running the cross japan race? good luck' or whatever depending on their input

    # race_days_until = st.sidebar.select_slider("レースまでの日数", options=[i for i in range(1, 366)])
    race_day = st.sidebar.date_input("レース日")
    race_days_until = (race_day - datetime.now().date()).days


    race_goaltime = st.sidebar.text_input("目標タイム（自由記述）")
    # create
    # race_days_until = st.sidebar.select_slider("レースまでの日数", options=[i for i in range(1, 366)])

    st.sidebar.header("現在の走力や練習について教えてください。")
    st.sidebar.write('自由記述。詳細であればあるほど、より適切な練習プランが作成されます。')

    current_pb = st.sidebar.text_area("目標レース距離の現PB", height=50)

    current_mileage = st.sidebar.text_area("週間走行距離", height=50)

    current_frequency = st.sidebar.text_area("練習頻度", height=50)
    # specify: per week?
    # make it a slider? number input?

    current_vo2max = st.sidebar.text_area("その他（VO2Max、閾値ペース、など）", height=50)


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

        st.header("Your Training Plan")
        output = get_trainingplan(race_days_until, race_distance, race_goaltime, current_pb, current_mileage, current_frequency, current_vo2max)

        # url = image_generator(output)
        # last_output = output.split("\n")[-2]
        process_inputs(output)



def process_inputs(input1):
    # Function to display the final output
    # Process the inputs here
    st.write(" ", input1)



if __name__ == "__main__":
    main()
