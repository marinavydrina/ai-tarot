import random
import openai
from flask import Flask, request, jsonify, render_template

openai.api_key = "YOUR_OPENAI_API_KEY"

TAROT_CARDS = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]

def interpret_tarot(card, question):
    prompt = f"""
You are a mystical tarot reader. A person asked: "{question}". 
You drew the card "{card}". Explain the meaning of this card in the context of the question, using beautiful, poetic and intuitive language.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=500
    )
    return response.choices[0].message["content"]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "Что мне нужно знать прямо сейчас?")
    card = random.choice(TAROT_CARDS)
    interpretation = interpret_tarot(card, question)
    return jsonify({
        "card": card,
        "interpretation": interpretation
    })


# (Render сам запустит gunicorn)
