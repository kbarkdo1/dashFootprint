from flask import Flask, request, jsonify
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
import openai
from dotenv import load_dotenv
import os
# from flask_cors import CORS

# limiter = Limiter(app)


# load env variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# @app.route('/', methods=['POST'])
# @limiter.limit("15 per minute")


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


openai_api()