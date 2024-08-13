# marathon-planner

Training for a long distance running event requires a good deal of planning, which can be tedious and confusing. This app is meant to help runners create specific and customized training plans in order to reach their running goals.

How it works: 
The inputs are taken in and processed a bit on the backend in order to provide more info for the LLM. For example, there are backend functions that takes the user’s ‘goal time’ input and extrapolates extra information from it such as ‘goal pace’, so the LLM can make better suggestions for training paces (eg. Today: Run 5km at goal pace).
All this info is compiled into a lengthy prompt before it’s fed into the Gemini API. The prompt is pretty much the culmination of my 40 iterative prompts from my original try with ChatGPT lol. 
The frontend is all done on Streamlit and I tried to be as intuitive as possible with the input widgets.



[v1.0](https://github.com/tjyana/marathon-planner/releases/tag/v1.0)

### v1.0
- Created basic MVP
- Able to take user input and output a plan
- Created for Japanese users
- User can input: race distance (select box), days until race (calendar), goal time (text input), current pb (text input), current mileage (text input), practice frequency (text input), VO2Max (text input).

## Installation

```sh
git clone https://github.com/tjyana/marathon-planner.git
cd your-project
pip install -r requirements.txt

# Usage
streamlit run app.py
