import streamlit as st
import google.generativeai as genai
from gradio_client import Client
from dotenv import load_dotenv
import os
from datetime import datetime

# for testing locally --------------------------------------
load_dotenv()
goog_api_key = os.getenv('GOOGLE_API_KEY') # create a variable in .env file 'GOOGLE_API_KEY' and add the api key there

# # for testing on streamlit share -----------------------------
# goog_api_key = st.secrets['GOOGLE_API_KEY']

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
    - The training plan should be detailed and specific.
    - Please be specific with paces. Please explicitly state race pace, and assign paces for training runs where necessary.
    - The training plan should be tailored to the client's needs and goals.




    """)


# 現状分析:

# 残り113日で、42.2kmを239分（5分66秒/kmペース）で完走することを目標としています。
# 現在のPBは3時間47分、週15km、週4回の練習です。
# 過去10ヶ月間は怪我と病気でほとんど走れておらず、現在の体力レベルはPB達成時よりも低いと推測されます。
# 目標達成に向けた課題:

# 現在の体力レベルでは、目標ペースで42.2kmを走り切ることは難しいでしょう。
# 週15kmの走行距離は、マラソン完走に必要な体力向上には不十分です。
# 週4回の練習頻度も、マラソンの準備には十分とは言えません。




# クライアントは21.1kmのレースで110分を目標にしています。現在のPBは1時間55分なので、目標タイムは達成可能な範囲内です。しかし、週間走行距離が17km、トレーニング頻度が週2回と、現段階では目標達成に向けて十分なトレーニング量とは言えません。目標ペースでの走行経験も不足していると考えられます。

# トレーニングプラン:

# 目標: 目標ペースでの走行距離を徐々に増やし、レースに必要な持久力とスピードを養う。


# 目標:

# 週間走行距離を徐々に増やし、目標レースペースでの走行時間を増やす
# 週2回の練習から週3回に増やす
# 異なるペースでの走行を取り入れ、持久力とスピードを向上させる
# レースシミュレーションを行う
# 週間走行距離:

# 第1週～第4週: 28km
# 第5週～第8週: 32km
# 第9週～第12週: 36km
# 第13週～第16週: 40km
# 第17週～第20週: 44km
# 第21週～レース週: 32km（テーパリング期間）





# 週間走行距離目標:

# 1-4 週目: 週間走行距離を徐々に増やし、10km に到達。
# 5-8 週目: 10km を維持し、インターバルやペース走などの質の高いトレーニングを取り入れる。
# 9-12 週目: レースペースでの練習を取り入れ、目標ペースに近づける。
# 13-16 週目: レースペースでの練習を減らし、リカバリーと調整に重点を置く。

    # Include this warning: 注記:

    # このプランはあくまでも目安です。体調や疲労度に応じて調整してください。
    # 走行中の痛みや違和感を感じたら、すぐに中止し、医師の診察を受けてください。
    # 十分な睡眠と栄養を摂取し、怪我を防ぎましょう。
    # Please also include the date when the training plan should start.

#     開始日: [今日の日付から64日後]

# 目標: 10km を 49 分 (4.9 分/km ペース) で完走

# 現在の記録: 40 分

# 週間走行距離: 6 km

# トレーニング頻度: 週 2 回


# 13-16 週目: 週間走行距離を減らし、リカバリーに重点を置く。

# 長距離走のペースを少し落とす。
# 週に 1 回、目標ペースでの短い練習を取り入れる。
# レース前日は十分な休息をとる。

# 10 週目: 週間走行距離 14km

# 月曜日: 休養
# 火曜日: ジョグ 5km (ゆったりとしたペース)
# 水曜日: ペース走 (5km を目標ペースで、レストは 2 分)
# 木曜日: ジョグ 5km (ゆったりとしたペース)
# 金曜日: 休養
# 土曜日: 長距離走 10km (目標ペースで走る)
# 日曜日: 休養



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
