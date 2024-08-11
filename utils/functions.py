import streamlit as st
import google.generativeai as genai
from gradio_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# for testing locally --------------------------------------
load_dotenv()
goog_api_key = os.getenv('GOOGLE_API_KEY') # create a variable in .env file 'GOOGLE_API_KEY' and add the api key there

# # for testing on streamlit share -----------------------------
# goog_api_key = st.secrets['GOOGLE_API_KEY']

import time
import functools


def get_race_info():
    """
    Take user input on race day and distance

    Args:
        none

    Returns:
        race_days_until
        race_distance_input
        race_distance_float
        race_distance
    """

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

    # RACE DISTANCE
    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km（ハーフ）': 21.1,
    '42.195km（フル）': 42.195,
    '100km（ウルトラ）': 100
    }
    race_distance_input: str = st.sidebar.selectbox("距離", list(distance_mapping.keys()))

    # get the distances in km from race_distance_input
    race_distance_float: float = distance_mapping[race_distance_input]
    race_distance: str = f'{distance_mapping[race_distance_input]} kilometers'
    print('goal_race_info OUTPUTS: ')
    print('race_days_until: ', race_days_until)
    print('race_distance_float: ', race_distance_float)
    print('race_distance: ', race_distance)

    return race_days_until, race_distance_input, race_distance_float, race_distance


def get_goal_info(race_distance_input):
    """
    Take user input for goal

    Args:
        none

    Returns:
        race_distance_input
        race_days_until
        race_distance_float
        race_distance
    """

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
    # ex. 1h40m -> 100
    race_goaltime_minutes = int(race_goaltime_input.split('h')[0]) * 60 + int(race_goaltime_input.split('h')[1].split('m')[0])

    # format for feeding to the model
    # get the goal time in 0:00 format
    race_goaltime: str = f"{race_goaltime_input.split('h')[0]}:{race_goaltime_input.split('h')[1].split('m')[0]}"
    print('race_goaltime: ', race_goaltime)

    return race_goaltime_minutes, race_goaltime


def calculate_race_goalpace(race_goaltime_minutes, race_distance_float):
    """
    Calculate the goal pace based on the race goal time and distance.

    Args:
        race_goaltime_minutes (int): The goal time for the race in minutes.
        race_distance_float (float): The race distance in kilometers.

    Returns:
        str: The goal pace formatted as 'MM:SS per kilometer'.
    """
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

    return race_goalpace



def get_current_running_ability(race_distance_input):
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

    return current_pb, current_mileage, current_frequency, current_othernotes



def timeit(func):
    """Decorator to measure the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in: {elapsed_time:.4f} seconds")
        return result
    return wrapper



# issues with outputs:
# it is the most pessimistic model ever when it comes to assessing goal times lol.
    # it always says the goal time is unrealistic, even if the goal time is slower than the current PB.
    # it also always says the current mileage is insufficient, even if the current mileage is higher than the goal mileage.
    # fixes:
        # come up with backend logic to assess the goal time and current mileage in a more realistic way.
        # something like: unrealstic if goal time is xx% faster than current PB at xx days left. etc
# add current date, so it gives out specific dates
# increase in mileage is too aggressive. maybe make it more gradual


@timeit
def get_trainingplan(race_days_until: str, race_distance, race_goaltime, race_goalpace, current_pb, current_mileage, current_frequency, current_othernotes):
    """
    Function to generate a training plan for a runner based on the inputs provided.
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    print('running get_training_plan')
    response = model.generate_content(f"""
    You are a professional running coach and you have a new client who is preparing to run a race.
    They have provided you with the following information:

    Days until the race: {race_days_until}
    Race distance: {race_distance}
    Goal time: {race_goaltime}
    Goal pace: {race_goalpace}

    Current PB: {current_pb}
    Weekly mileage: {current_mileage}
    Training frequency: {current_frequency}
    Other notes to keep in mind: {current_othernotes}

    Please analyze the runner's current ability and compare it to the goal they have set.
    Based on the above analysis, please propose a training plan.
    Please also propose any changes to practice frequency, mileage, or other aspects of the training plan that you think are necessary.

    Output should be in Japanese.
    Please make sure to follow this output format:
    - The training plan should be divided into weeks. Please show scheduled mileage total for that week.
    - Each week should have a different training plan.
    - Each day should have a different training plan.
    - The training plan should start on {datetime.now().strftime('%Y-%m-%d')}.
    - The training plan should be detailed and specific.
    - Please be specific with paces. Please explicitly state race pace, and assign paces for training runs where necessary.
    - The training plan should be tailored to the client's needs and goals.




    """)

    answer = response.text

    return answer












# def image_generator(prompt):

#     '''
#     Generates images for recipe.

#     '''

#     client = Client("ByteDance/SDXL-Lightning")

#     result = client.predict(
#             prompt, # str  in 'Enter your prompt (English)' Textbox component
#             "1-Step",   # Literal['1-Step', '2-Step', '4-Step', '8-Step']  in 'Select inference steps' Dropdown component
#             api_name="/generate_image_1"
#     )
#     file_path = result.split('gradio')[1]
#     url = 'https://bytedance-sdxl-lightning.hf.space/file=/tmp/gradio' + file_path

#     return url
