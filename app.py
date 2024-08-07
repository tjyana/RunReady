import streamlit as st
from utils.functions import get_trainingplan
import random
import os
from datetime import datetime, timedelta

# can we roadmap something for implementations?
# 1. unit tests
# 2. refactoring.
#   - separate the functions
#   - migrate the functions to a separate file
#   - add type hints
#   - add docstrings
# 3. user tracking. how many times the app has been used

# features backlog:
# 1. add more languages
# 2. add miles version
# 3. standardize output format?
    # - decide on exact output format
        # - fields: current situation, goal, gaps/problems, overview/goal of the plan, detailed plan
# 4. enable csv download
# 5. style output


# finetuning backlog:
# - the sliders are pretty wide right now bc it tries to take into account all possible times.
#   - maybe we can adjust the ranges to be more realistic
#   - or decide on a different input method

# add english version as well. probably a radio button, with a copy of english version of the form
# miles version too



# separate out. this is a lot lol
def main():




    # Title
    st.sidebar.title("Run Training Planner 🏃")
    st.sidebar.write("ランニングの長距離レースに向けて練習プランを作成するアプリです。")

    # Input fields
    st.sidebar.header("レースについて教えてください。")

    ########################################################################
    # GOAL RACE INFO
    #######################################################################

    # DAYS UNTIL RACE
    initial_date = datetime.now().date() + timedelta(days=60)
    race_day = st.sidebar.date_input("レース日", value = initial_date)
    race_days_until_int: int = (race_day - datetime.now().date()).days
    race_days_until: str = f'{(race_day - datetime.now().date()).days} days'
    if race_days_until_int < 14:
        st.warning(f"レースまで{race_days_until_int}日を切りました！この期間ではトレーニングプランに十分な時間がないかもしれません。")

    ##### add warning if race day is too close
    ##### also adjust so it outputs plan with dates


    #############################################
    # RACE DISTANCE
    # eventually be able to take other distances


    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km（ハーフ）': 21.1,
    '42.195km（フル）': 42.195,
    '100km（ウルトラ）': 100
    }
    race_distance_input: str = st.sidebar.selectbox("距離", list(distance_mapping.keys()))
    print('race_distance_input: ', race_distance_input)

    # get the distances in km
    race_distance_float: float = distance_mapping[race_distance_input]
    race_distance: str = f'{distance_mapping[race_distance_input]} kilometers'
    print('race_distance: ', race_distance)




    #############################################
    # GOAL TIME

    goaltime_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.195km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }
    race_goaltime_input: str = st.sidebar.select_slider("目標タイム", goaltime_mapping[race_distance_input])
    print('race_goaltime_input: ', race_goaltime_input)

    # convert the goal time to minutes
    # 1h40m -> 100
    race_goaltime_minutes = int(race_goaltime_input.split('h')[0]) * 60 + int(race_goaltime_input.split('h')[1].split('m')[0])

    # format for feeding to the model
    # get the goal time in 0:00 format
    race_goaltime: str = f"{race_goaltime_input.split('h')[0]}:{race_goaltime_input.split('h')[1].split('m')[0]}"
    print('race_goaltime: ', race_goaltime)

    #############################################
    # GOAL PACE
    # parse out into separate function later (this goes for entire script lol)

    ### calculate the goal pace in 0:00 format
    # eg.  55:00 for 10km -> 5:30 per kilometer

    # goalpace as a float.
    # eg. 5.5
    race_goalpace_float = race_goaltime_minutes / race_distance_float

    # get minutes and seconds
    # eg. 5.5 -> 5:30
    race_goalpace_minutes = str(race_goalpace_float).split(".")[0]
    print(race_goalpace_minutes)
    race_goalpace_seconds = str(round(float(str(race_goalpace_float).split(".")[1][0:2]) * 0.6))
    if len(race_goalpace_seconds) == 1:
        race_goalpace_seconds = '0' + race_goalpace_seconds
    print(race_goalpace_seconds)

    # format into 0:00
    race_goalpace: str = f'{race_goalpace_minutes}:{race_goalpace_seconds} per kilometer'
    print('race_goalpace: ', race_goalpace)


    ########################################################################
    # CURRENT RUNNING ABILITY
    ########################################################################

    st.sidebar.header("現在の走力や練習について教えてください。")

    pb_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.195km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }

    # Current PB
    # add a 'have you ever run this distance before' option. if no, hide the pb slider
    distance_experience = st.sidebar.radio("レース距離を走ったことはありますか？", ['はい', 'いいえ'], horizontal = True)
    # distance_experience = st.sidebar.toggle("レース距離を走ったことはありますか？")
    if distance_experience ==  'はい':
        current_pb_input = st.sidebar.select_slider("目標レース距離の現PB", pb_mapping[race_distance_input])
        current_pb_hours = current_pb_input.split('h')[0]
        current_pb_minutes = current_pb_input.split('h')[1].split('m')[0]
        current_pb: str = f'{current_pb_hours} hours {current_pb_minutes} minutes'
    else:
        current_pb: str = 'N/A'
    print('current_pb: ', current_pb)

    # Current Mileage
    current_mileage_input = st.sidebar.select_slider("週間走行距離", [f'{mileage} km' for mileage in range(0, 150)])
    current_mileage: str = f'{current_mileage_input} km per week'

    # Current Frequency
    current_frequency_input = st.sidebar.select_slider("練習頻度(週〇回)", [f'週{frequency}回' for frequency in range(0, 15)])
    print('current_frequency_input: ', current_frequency_input)
    current_frequency: str = f'I run {current_frequency_input}'

    # Free text input: other notes
    current_othernotes: str = st.sidebar.text_area("その他（自由記述）", placeholder = 'ランニング歴、レース経験、VO2Max、閾値ペース、予定している中間レース、ケガや制限、など。詳細であればあるほど、より適切な練習プランが作成されます。', height=50)


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
        print(output[0:10])
        # url = image_generator(output)
        # last_output = output.split("\n")[-2]
        process_inputs(output)



def process_inputs(input1):
    # Function to display the final output
    # Process the inputs here
    st.write(" ", input1)



if __name__ == "__main__":
    main()
