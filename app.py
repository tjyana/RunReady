import streamlit as st
from utils.functions import get_trainingplan
import random
import os
from datetime import datetime, timedelta
from utils.functions import get_race_info, get_goal_info, calculate_race_goalpace, get_current_running_ability, ui_title

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

    ui_title()
    # # Title
    # st.sidebar.title("Run Training Planner 🏃")
    # st.sidebar.write("ランニングの長距離レースに向けて練習プランを作成するアプリです。")

    # # Input fields
    # st.sidebar.header("レースについて教えてください。")

    race_days_until, race_distance_input, race_distance_float, race_distance = get_race_info()

    race_goaltime_minutes, race_goaltime = get_goal_info(race_distance_input)

    race_goalpace = calculate_race_goalpace(race_goaltime_minutes, race_distance_float)

    current_pb, current_mileage, current_frequency, current_othernotes = get_current_running_ability(race_distance_input)



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
