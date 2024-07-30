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

    # DAYS UNTIL RACE
    # race_days_until = st.sidebar.select_slider("レースまでの日数", options=[i for i in range(1, 366)])
    race_day = st.sidebar.date_input("レース日")
    race_days_until = (race_day - datetime.now().date()).days



    ########################################################################
    # RACE DISTANCE
    # eventually be able to take other distances
    #######################################################################

    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km（ハーフ）': 21.1,
    '42.2km（フル）': 42.2,
    '100km（ウルトラ）': 100
    }
    race_distance_input = st.sidebar.selectbox("距離", list(distance_mapping.keys()))
    print('race_distance_input: ', race_distance_input)

    # get the distances in km
    race_distance = distance_mapping[race_distance_input]
    print('race_distance: ', race_distance)

    # if race_distance == 'その他（入力）':
    #     race_distance = st.sidebar.text_input("その他の距離を入力してください。")
    #     # add llm generate function that spits out 'you're running the cross japan race? good luck' or whatever depending on their input




    ########################################################################
    # GOAL TIME
    # make it a slider. diff for each distance.
    ########################################################################

    goaltime_mapping = {
    '5K': [f'{i}:00' for i in range(12, 60)],
    '10K': [f'{i}:00' for i in range(25, 100)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1)],
    '42.2km（フル）': [f'{h}h{m:02d}m' for h in range(2, 8) for m in range(0, 60, 1)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }
    race_goaltime = st.sidebar.select_slider("目標タイム", goaltime_mapping[race_distance_input])
    print('race_goaltime: ', race_goaltime)

    ########################################################################
    # GOALPACE cleaner/calculator
    # parse out into separate function later (this goes for entire script lol)
    ########################################################################

    # clean the goal time input


    # calculate the goal pace
    # race_goalpace = int(race_goaltime) / int(race_distance)


    st.sidebar.header("現在の走力や練習について教えてください。")
    st.sidebar.write('自由記述。詳細であればあるほど、より適切な練習プランが作成されます。')

    current_pb = st.sidebar.text_area("目標レース距離の現PB", height=50)

    current_mileage = st.sidebar.text_area("週間走行距離", height=50)

    current_frequency = st.sidebar.text_area("練習頻度", height=50)
    # specify: per week?
    # make it a slider? number input?


    # ask for 中間レース

    current_vo2max = st.sidebar.text_area("その他（VO2Max、閾値ペース、など）", height=50)


    # Submit button
    if st.sidebar.button("Submit"):
        # Process the inputs
        st.session_state.race_days_until = race_days_until
        st.session_state.race_distance = race_distance
        st.session_state.race_goaltime = race_goaltime
        st.session_state.race_goalpace = race_goalpace
        st.session_state.current_pb = current_pb
        st.session_state.current_mileage = current_mileage
        st.session_state.current_frequency = current_frequency
        st.session_state.current_vo2max = current_vo2max

        st.header("Your Training Plan")
        output = get_trainingplan(race_days_until, race_distance, race_goaltime, race_goalpace, current_pb, current_mileage, current_frequency, current_vo2max)

        # url = image_generator(output)
        # last_output = output.split("\n")[-2]
        process_inputs(output)



def process_inputs(input1):
    # Function to display the final output
    # Process the inputs here
    st.write(" ", input1)



if __name__ == "__main__":
    main()
