from flask import Flask, request, jsonify, render_template
from openai import OpenAI

client = OpenAI()
from dotenv import load_dotenv
import os
import requests as rq
import json

MENURESPONSE = None

app = Flask(__name__)

load_dotenv()

def get_completion(prompt): 



    print("in get_completion")
    '''try:
        print("in try")

        print(type(response))

        # generated_text = response.json().get('generated_text')

        # Return the generated text as JSON response
        # return {"response": response}
        # return response
    except Exception as e:
        return render_template('apiError.html', code="Sharples is currently closed. Data will be displayed at meal time.")
        return jsonify(error=f"{e}"), 500
    print(type(response))'''

    # print(prompt) 

    CONTENT = "I will provide you with a JSON that contains key-value pairs where the values are lists of menu items. You will return to me a json file, with no other text, where the keys are the same keys from the json i give you and the values are lists of tuples, where in each tuple the first element is the element from the list of the first json file, and the second element is the primary ingredient used in making the first element."
    PREFIX = "I will provide you with a JSON that contains key-value pairs where the values are lists of menu items. You will return to me a json file, with no other text, where the keys are the same keys from the json i give you and the values are lists of tuples, where in each tuple the first element is the element from the list of the first json file, and the second element is the primary ingredient used in making the first element. Here is the json:"
    prompt = PREFIX + str(prompt)
    MODEL = "gpt-3.5-turbo"
    response = client.chat.completions.create(model=MODEL,
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": CONTENT},
        {"role": "user", "content": prompt}
    ],
    temperature=0)

    textResponse = response.choices[0].message.content
    print("text response type is: ", type(textResponse))
    return textResponse


@app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
def index():

    global MENURESPONSE

    sccsResponse = rq.get("http://dining.sccs.swarthmore.edu/api").json()
    rawAPI = rq.get("https://dash.swarthmore.edu/dining_json").json()
    meal = rawAPI['dining_center'][0]['title'].lower()

    if (meal == "closed"):
        return render_template('sharplesClosed.html')

    menu = {}
    try:
        mealList = sccsResponse['Dining Center'][meal]
        for i in mealList:
            if i in ['start', 'end', 'time']: 
                continue
            menu[i] = []
            for j in mealList[i]:
                # print(type(j))
                menu[i].append(j['item'])
    except KeyError as e:
        return render_template('sharplesClosed.html', code="KeyError. SCCS Dining API not updated. Try again later.")
    except Exception as e:
        return render_template('sharplesClosed.html', code="Non-Key Error. SCCS Dining API not updated. Try again later.")


    print(menu)

    if MENURESPONSE == None:
        MENURESPONSE = '{"hell":"yeah"}'
        response = get_completion(menu)
        MENURESPONSE = json.loads(response)
        print("menuresponse defined: ", type(MENURESPONSE))
    else:
        print("menuresponse already exists: ", type(MENURESPONSE))

    return render_template('index.html', title = str(rawAPI['dining_center'][0]['title']))


def read_csv():
    return

@app.route('/openai_api', methods=['GET', 'POST'])
def openai_api():

    # user prompt
    data = request.get_json()
    data['prompt'] = "Three-Bean-Salad"

    # input validation
    '''if not data or 'prompt' not in data or not data['prompt']:
        return jsonify(error="Missing Prompt."), 400
    elif type(data['prompt']) != str:
        return jsonify(error="Prompt must be a string"), 400
    elif len(data['prompt']) > 1000:
        return jsonify(error="Prompt must be less than 1000 characters"), 400'''


    CONTENT = "Given a list of menu items, you will identify the primary ingredients of each one, and return a JSON object pairing the menu item from the prompt with a comma-separated list of its main ingredients"
    PREFIX = "Return the primary ingredients of the following: "
    prompt = PREFIX + data.get('prompt')


    MODEL = "gpt-3.5-turbo"
    try:
        response = client.chat.completions.create(model=MODEL,
        messages=[
            {"role": "system", "content": CONTENT},
            {"role": "user", "content": prompt}
        ],
        temperature=0)

        # generated_text = response.json().get('generated_text')

        # Return the generated text as JSON response
        # return {"response": response}
        return response

    except Exception as e:
        return jsonify(error=f"{e}"), 500


if __name__ == '__main__':
    app.run()
