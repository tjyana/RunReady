import streamlit as st
import google.generativeai as genai
from gradio_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime

# # for testing locally --------------------------------------
# load_dotenv()
# goog_api_key = os.getenv('GOOGLE_API_KEY') # create a variable in .env file 'GOOGLE_API_KEY' and add the api key there

# for testing on streamlit share -----------------------------
goog_api_key = st.secrets['GOOGLE_API_KEY']




# add current date, so it gives out specific dates
def get_trainingplan(race_days_until, race_distance, race_goaltime, current_pb, current_mileage, current_frequency, current_vo2max):
    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(f"""
    You are a professional running coach and you have a new client who is preparing to run a race.
    They have provided you with the following information:

    Days until the race: {race_days_until}
    Race distance: {race_distance} km
    Goal time: {race_goaltime}

    Current PB: {current_pb}
    Weekly mileage: {current_mileage} km
    Training frequency: {current_frequency} per week
    VO2Max: {current_vo2max}

    Please make a training plan based on this information, and output it in Japanese.
    Please make sure to follow this output format:
    - The training plan should be divided into weeks. Please show scheduled mileage total for that week.
    - Each week should have a different training plan.
    - Each day should have a different training plan.
    - The training plan should be detailed and specific.
    - Please be specific with paces. Please explicitly state race pace, and assign paces for training runs where necessary.
    - The training plan should be tailored to the client's needs and goals.
    - If their Goal time is faster than the world record for Race distance, please inform them.

    """)

    answer = response.text

    return answer

    # Last output: ```{last_output}```




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
