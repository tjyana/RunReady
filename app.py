import streamlit as st
from utils.functions import get_trainingplan
import random
import os
from datetime import datetime


# add english version as well. probably a radio button, with a copy of english version of the form


# separate out. this is a lot lol
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

    ##### add warning if race day is too close
    ##### also adjust so it outputs plan with dates


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
    race_distance: int = distance_mapping[race_distance_input]
    print('race_distance: ', race_distance)

    # if race_distance == 'その他（入力）':
    #     race_distance = st.sidebar.text_input("その他の距離を入力してください。")
    #     # add llm generate function that spits out 'you're running the cross japan race? good luck' or whatever depending on their input




    ########################################################################
    # GOAL TIME
    # make it a slider. diff for each distance.
    ########################################################################

    goaltime_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.2km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }
    race_goaltime_input: str = st.sidebar.select_slider("目標タイム", goaltime_mapping[race_distance_input])
    print('race_goaltime_input: ', race_goaltime_input)

    ########################################################################
    # GOALPACE cleaner/calculator
    # parse out into separate function later (this goes for entire script lol)
    ########################################################################

    # 1h40m -> 100
    # clean the goal time input

    race_goaltime = int(race_goaltime_input.split('h')[0]) * 60 + int(race_goaltime_input.split('h')[1].split('m')[0])

    # calculate the goal pace
    race_goalpace = race_goaltime / race_distance
    ### calculate the goal pace in 0:00 format


    st.sidebar.header("現在の走力や練習について教えてください。")

    pb_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.2km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }
    current_pb = st.sidebar.select_slider("目標レース距離の現PB", pb_mapping[race_distance_input])

    current_mileage = st.sidebar.select_slider("週間走行距離(km)", range(0, 300))

    current_frequency = st.sidebar.select_slider("練習頻度(週〇回)", range(0, 15))



    # ask for 中間レース

    current_othernotes = st.sidebar.text_area("その他（自由記述）", placeholder = 'VO2Max、閾値ペース、中間レース、ケガや制限、など。詳細であればあるほど、より適切な練習プランが作成されます。', height=50)


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
        st.session_state.current_othernotes = current_othernotes

        st.header("Your Training Plan")
        output = get_trainingplan(race_days_until, race_distance, race_goaltime, race_goalpace, current_pb, current_mileage, current_frequency, current_othernotes)

        # url = image_generator(output)
        # last_output = output.split("\n")[-2]
        process_inputs(output)



def process_inputs(input1):
    # Function to display the final output
    # Process the inputs here
    st.write(" ", input1)



if __name__ == "__main__":
    main()
