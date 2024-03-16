from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os
import requests as rq

app = Flask(__name__)

load_dotenv()

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    response = rq.get("https://dash.swarthmore.edu/dining_json")
    ingredients = response.json()
    print(ingredients['sharples'][0]['title'])

    if (ingredients['sharples'][0]['title'] == "Closed"):
        return render_template('sharplesClosed.html')
    
    

    return render_template('index.html', title = ingredients['sharples'][0]['title'])


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
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CONTENT},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        # generated_text = response.json().get('generated_text')

        # Return the generated text as JSON response
        # return {"response": response}
        return response

    except Exception as e:
        return jsonify(error=f"{e}"), 500


if __name__ == '__main__':
    app.run()
