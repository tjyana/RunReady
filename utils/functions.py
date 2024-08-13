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



def language_options():
    st.sidebar.header("Select Language:")
    language = st.sidebar.radio("Language", ['English', '日本語'], horizontal = True)
    return language



############### English ################

def EN_ui_title():
    # Title
    st.sidebar.title("RunReady 🏃")
    st.sidebar.write("Create training plans for long-distance running races.")


def EN_ui_get_race_info():

    # Input fields
    st.sidebar.header("Please tell me about the race you are training for.")

    # DAYS UNTIL RACE
    initial_date = datetime.now().date() + timedelta(days=60)
    race_day = st.sidebar.date_input("Race Day", value = initial_date)

    # RACE DISTANCE
    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km (Half)': 21.1,
    '42.195km (Full)': 42.195,
    '100km (Ultra)': 100
    }
    race_distance_input: str = st.sidebar.selectbox("Distance", list(distance_mapping.keys()), index = 3)

    return race_day, race_distance_input

def EN_get_race_info(race_distance_input, race_day):
    """
    Processes race days until and race distance input from the user.
    UI taken out of the function

    Args:
        none

    Returns:
        race_days_until
        race_distance_input
        race_distance_float
        race_distance
    """

    # RACE DAYS UNTIL
    race_days_until_int: int = (race_day - datetime.now().date()).days
    race_days_until: str = f'{(race_day - datetime.now().date()).days} days'

    # RACE DISTANCE
    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km (Half)': 21.1,
    '42.195km (Full)': 42.195,
    '100km (Ultra)': 100
    }
    # get the distances in km from race_distance_input
    race_distance_float: float = distance_mapping[race_distance_input]
    race_distance: str = f'{distance_mapping[race_distance_input]} kilometers'


    return race_days_until_int, race_days_until, race_distance_float, race_distance

def EN_ui_warnings(race_days_until_int):
    if race_days_until_int < 0:
        st.warning("The race has already ended!")
    elif 0 < race_days_until_int < 14:
        st.warning(f"The race is in less than {race_days_until_int} days! There may not be enough time for training during this period.")
    elif race_days_until_int > 180:
        st.warning(f"The race is quite far away! The training plan may be summarized in the output.")



def EN_ui_get_goal_info(race_distance_input):
    goaltime_mapping = {
        '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
        '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
        '21.1km (Half)': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
        '42.195km (Full)': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
        '100km (Ultra)': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
        }
    race_goaltime_input: str = st.sidebar.select_slider("Goal Time", goaltime_mapping[race_distance_input], value = goaltime_mapping[race_distance_input][(len(goaltime_mapping[race_distance_input])//2)])

    return race_goaltime_input


def EN_ui_get_current_ability(race_distance_input):

    st.sidebar.header("Please tell me about your current running ability and training.")

    pb_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km (Half)': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.195km (Full)': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km (Ultra)': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }

    # Current PB
    # Have you ever run this distance?
    distance_experience = st.sidebar.radio("Have you ever ran this distance before?", ['Yes', 'No'], horizontal = True)

    if distance_experience ==  'Yes':
        current_pb_input = st.sidebar.select_slider("Current personal best for the race distance", pb_mapping[race_distance_input], value = pb_mapping[race_distance_input][(len(pb_mapping[race_distance_input])//2)])
        current_pb_hours = current_pb_input.split('h')[0]
        current_pb_minutes = current_pb_input.split('h')[1].split('m')[0]
        current_pb: str = f'{current_pb_hours} hours {current_pb_minutes} minutes'
    else:
        current_pb: str = 'N/A'

    # Current Mileage
    mileage_options = [f'{mileage} km' for mileage in range(0, 150)]
    current_mileage_input = st.sidebar.select_slider("Weekly mileage", mileage_options, value = mileage_options[len(mileage_options)//2])
    current_mileage: str = f'{current_mileage_input} km per week'

    # Current Frequency
    frequency_options = [f'{frequency}/week' for frequency in range(0, 15)]
    current_frequency_input = st.sidebar.select_slider("Training frequency (runs/week)", frequency_options, value = frequency_options[len(frequency_options)//2])
    current_frequency: str = f'I run {current_frequency_input}'

    # Free text input: other notes
    current_othernotes: str = st.sidebar.text_area("Other (free text)", placeholder = 'Running history, race experience, VO2Max, threshold pace, planned intermediate races, injuries or limitations, etc. The more detailed the information, the more specific the training plan will be.', height=100)

    return current_pb, current_mileage, current_frequency, current_othernotes

############### /English ################





############### Japanese ################

def ui_title():
    # Title
    st.sidebar.title("RunReady 🏃")
    st.sidebar.write("ランニングの長距離レースに向けて練習プランを作成するアプリです。")

    # Input fields
    st.sidebar.header("レースについて教えてください。")


def ui_get_race_info():
    # DAYS UNTIL RACE
    initial_date = datetime.now().date() + timedelta(days=60)
    race_day = st.sidebar.date_input("レース日", value = initial_date)

    # RACE DISTANCE
    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km（ハーフ）': 21.1,
    '42.195km（フル）': 42.195,
    '100km（ウルトラ）': 100
    }
    race_distance_input: str = st.sidebar.selectbox("距離", list(distance_mapping.keys()), index = 3)

    return race_day, race_distance_input


def ui_warnings(race_days_until_int):
    if race_days_until_int < 0:
        st.warning("レースはすでに終了しています！")
    elif 0 < race_days_until_int < 14:
        st.warning(f"レースまで{race_days_until_int}日を切りました！この期間ではトレーニングする十分な時間がないかもしれません。")
    elif race_days_until_int > 180:
        st.warning(f"レースまでだいぶ先ですね！トレーニングプランが要約されて出力されるかもしれません。")


def ui_get_goal_info(race_distance_input):
    goaltime_mapping = {
        '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
        '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
        '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
        '42.195km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
        '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
        }
    race_goaltime_input: str = st.sidebar.select_slider("目標タイム", goaltime_mapping[race_distance_input], value = goaltime_mapping[race_distance_input][(len(goaltime_mapping[race_distance_input])//2)])

    return race_goaltime_input


def ui_get_current_ability(race_distance_input):

    st.sidebar.header("現在の走力や練習について教えてください。")

    pb_mapping = {
    '5K': [f'{h}h{m:02d}m' for h in range(0, 1) for m in range(0, 60, 1) if (h > 0 or m >= 12)],
    '10K': [f'{h}h{m:02d}m' for h in range(0, 2) for m in range(0, 60, 1) if (h > 0 or m >= 25) and (h < 2 or m <= 20)],
    '21.1km（ハーフ）': [f'{h}h{m:02d}m' for h in range(1, 4) for m in range(0, 60, 1) if (h > 0 or m >= 57)],
    '42.195km（フル）': [f'{h}h{m:02d}m' for h in range(1, 8) for m in range(0, 60, 1) if (h > 1 or m >= 59)],
    '100km（ウルトラ）': [f'{h}h{m:02d}m' for h in range(6, 20) for m in range(0, 60, 1)],
    }

    # Current PB
    # Have you ever run this distance?
    distance_experience = st.sidebar.radio("レース距離を走ったことはありますか？", ['はい', 'いいえ'], horizontal = True)

    if distance_experience ==  'はい':
        current_pb_input = st.sidebar.select_slider("目標レース距離の現PB", pb_mapping[race_distance_input], value = pb_mapping[race_distance_input][(len(pb_mapping[race_distance_input])//2)])
        current_pb_hours = current_pb_input.split('h')[0]
        current_pb_minutes = current_pb_input.split('h')[1].split('m')[0]
        current_pb: str = f'{current_pb_hours} hours {current_pb_minutes} minutes'
    else:
        current_pb: str = 'N/A'

    # Current Mileage
    mileage_options = [f'{mileage} km' for mileage in range(0, 150)]
    current_mileage_input = st.sidebar.select_slider("週間走行距離", mileage_options, value = mileage_options[len(mileage_options)//2])
    current_mileage: str = f'{current_mileage_input} km per week'

    # Current Frequency
    frequency_options = [f'週{frequency}回' for frequency in range(0, 15)]
    current_frequency_input = st.sidebar.select_slider("練習頻度(週〇回)", frequency_options, value = frequency_options[len(frequency_options)//2])
    current_frequency: str = f'I run {current_frequency_input}'

    # Free text input: other notes
    current_othernotes: str = st.sidebar.text_area("その他（自由記述）", placeholder = 'ランニング歴、レース経験、VO2Max、閾値ペース、予定している中間レース、ケガや制限、など。詳細であればあるほど、より適切な練習プランが作成されます。', height=100)

    return current_pb, current_mileage, current_frequency, current_othernotes

############### /Japanese ################



def get_race_info(race_distance_input, race_day):
    """
    Processes race days until and race distance input from the user.
    UI taken out of the function

    Args:
        none

    Returns:
        race_days_until
        race_distance_input
        race_distance_float
        race_distance
    """

    # RACE DAYS UNTIL
    race_days_until_int: int = (race_day - datetime.now().date()).days
    race_days_until: str = f'{(race_day - datetime.now().date()).days} days'

    # RACE DISTANCE
    distance_mapping = {
    '5K': 5,
    '10K': 10,
    '21.1km（ハーフ）': 21.1,
    '42.195km（フル）': 42.195,
    '100km（ウルトラ）': 100
    }
    # get the distances in km from race_distance_input
    race_distance_float: float = distance_mapping[race_distance_input]
    race_distance: str = f'{distance_mapping[race_distance_input]} kilometers'


    return race_days_until_int, race_days_until, race_distance_float, race_distance


def get_goal_info(race_goaltime_input):
    """
    Processes the goal time input from the user.
    Calculate the goal time in minutes, and also format it for the model.
    UI taken out of the function.

    Args:
        race_distance_input

    Returns:
        race_goaltime_minutes
        race_goaltime
    """

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
    # Calculate goalpace as a float.
    # eg. 5.5
    race_goalpace_float = race_goaltime_minutes / race_distance_float

    # get minutes and seconds
    # eg. 5.5 -> 5:30
    # minutes
    race_goalpace_minutes = str(race_goalpace_float).split(".")[0]
    # seconds
    race_goalpace_seconds = str(round(float(str(race_goalpace_float).split(".")[1][0:2]) * 0.6))
    if len(race_goalpace_seconds) == 1:
        race_goalpace_seconds = '0' + race_goalpace_seconds

    # format into 0:00
    race_goalpace: str = f'{race_goalpace_minutes}:{race_goalpace_seconds} per kilometer'
    print('race_goalpace: ', race_goalpace)

    return race_goalpace








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
def get_trainingplan(language, race_day, race_days_until: str, race_distance, race_goaltime, race_goalpace, current_pb, current_mileage, current_frequency, current_othernotes):
    """
    Function to generate a training plan for a runner based on the inputs provided.
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    print('running get_training_plan')

    response = model.generate_content(f"""
    You are a professional running coach with a new client who is preparing to run a race.
    Your client has provided you with the following information:

    Days until the race: {race_days_until}
    Race distance: {race_distance}
    Goal time: {race_goaltime}
    Goal pace: {race_goalpace}

    Current personal best for {race_distance}: {current_pb}
    Weekly mileage: {current_mileage}
    Training frequency: {current_frequency}
    Other notes to keep in mind: {current_othernotes}

    Please analyze your client's current ability and compare it to the goal they have set.
    Based on the above analysis, please propose a training plan to your client.

    - Output should be in {language}.
    - The training plan should be divided into weeks. Please show scheduled mileage total for that week, and make sure the miles in that week add up to the total.
    - Each week should have a different training plan.
    - Each day should have a different training plan. Please include rest days.
    - Number of runs per week should be based on the client's current training frequency of {current_frequency}.

    - The training plan should start on {datetime.now().strftime('%Y-%m-%d(%A)')}. Please make sure the day of the week is correct.
    - Race day is {race_day}. Please include this in the plan.


    - Do not increase weekly mileage by more than 10%. Please make sure the increase is gradual.
    - No need to increase mileage every single week. Please include recovery weeks.

    - Please be specific with paces. Please explicitly state race pace, and assign paces for training runs where necessary.
    - Interval training paces should be faster than {race_goalpace} pace.
    - Please include cross-training, strength training, and stretching in the plan where necessary.

    - Please display the full plan with all weeks.

    After your analysis, please output weekly/daily plan in below format delineated by ```, with appropriate content in []
    (below plan is assuming we start on 8/15/2024):
    ```
    Analysis: [Your analysis here]

    Current situation: [Current situation here]

    Training Plan Overview: [Overview here]

    Training Plan Details: [output in format below]

    Phase 1: Base Building (Weeks 1-12, August 15 - November 4) This phase focuses on building a solid aerobic base and increasing mileage gradually.

    Week 1 (August 15 - August 19) Total Mileage: [Total mileage for that week]
    8/15 (Thu): [Training plan for that day]
    8/16 (Fri): [Training plan for that day]
    8/17 (Sat): [Training plan for that day]
    8/18 (Sun): [Training plan for that day]

    ```

    """)
    print({datetime.now().strftime('%Y-%m-%d (%A)')})
    answer = response.text

    return answer

# Couldn't get below to work:
    # - If the output is too long, please provide a summary of the plan and a link to download the full plan as a CSV file.
