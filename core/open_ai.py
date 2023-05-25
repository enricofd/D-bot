import os
import openai

CHATGPT_KEY = os.environ.get("CHATGPT_KEY")

def chat_gpt (message):

    openai.api_key = CHATGPT_KEY

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": message},
        ]
    )
    return response['choices'][0]['message']['content']
