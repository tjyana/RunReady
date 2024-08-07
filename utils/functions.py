import streamlit as st
import google.generativeai as genai
from gradio_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# # for testing locally --------------------------------------
# load_dotenv()
# goog_api_key = os.getenv('GOOGLE_API_KEY') # create a variable in .env file 'GOOGLE_API_KEY' and add the api key there

# for testing on streamlit share -----------------------------
goog_api_key = st.secrets['GOOGLE_API_KEY']

import time
import functools

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
    - The training plan should start day after {datetime.now().strftime('%Y-%m-%d')}.
    - If shorter than 24 weeks, please display plan for all weeks.
    - The training plan should be detailed and specific.
    - Please be specific with paces. Please explicitly state race pace, and assign paces for training runs where necessary.
    - The training plan should be tailored to the client's needs and goals.
    - The training plan should be realistic and achievable.




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
