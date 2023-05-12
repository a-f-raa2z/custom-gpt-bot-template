import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
chat_history = []

@app.route('/', methods=['GET', 'POST'])
def knowledge():
    if request.method == 'POST':
        global chat_history
        chat_history = []
        botknowledge = request.form.get('botknowledge', '')
        return render_template('index.html', botknowledge=botknowledge, chat_history=chat_history)
    else:
        chat_history = []
        return render_template('index.html', chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask():
    botknowledge = request.form.get('botknowledge', '')
    userquestion = request.form['userquestion']
    chat_history.append({'user': userquestion})
    prompt = f"{botknowledge}\nQ: {userquestion}\nA:"
    response = generate_response(prompt)
    answer = request.args.get("answer")
    chat_history[-1]['bot'] = response
    return render_template('index.html', chat_history=chat_history, response=response, answer=answer, botknowledge=botknowledge, userquestion=userquestion)


def generate_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.6,
    )

    message = response.choices[0].text.strip()
    return message
