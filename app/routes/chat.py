import fastapi
import json
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

chatbot = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

import json

prompt ="""You are a witty, fun astrology assistant like a friend.
You mút interpret a user's natal chart, answer questions related to astrology, personality traits, and life tendencies based on that.
Only answer questions related to astrology or the provided natal chart.
If a question is unrelated, respond with something like:
"I'm designed to help interpret your astrology charts. Please ask a question related to your natal chart or astrology.
Keep it short under 200 words or less."""

def compress_chart(chart):
    lines = []

    for angle in chart["angles"]:
        if angle["name"] in ["Ascendant", "Midheaven"]:
            lines.append(f"{angle['name']}-{angle['sign']}-{angle['signDegree']:.1f}°")

    lines.append("PLANETS")

    for p in chart["planets"]:
        rx = "-Rx" if p["retrograde"] else ""
        lines.append(
            f"{p['name']}-{p['sign']}-{p['signDegree']:.1f}°-H{p['house']}{rx}"
        )

    lines.append("ASPECTS")

    for a in chart["aspects"]:
        lines.append(
            f"{a['planet1']}-{a['type']}-{a['planet2']}-({a['orb']}°)"
        )

    return "\n".join(lines)


with open("./mock_chart.json") as f:
    chart = json.load(f)
chart = compress_chart(chart)
print(chart)
while True:
    print("TEST")
    print("Press 1 to ask the chatbot. Else exit.")
    user_input = input()
    if user_input.strip() != "1":
        break

    question = input("Question: ").strip()
    chat = chatbot.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{prompt}"
            },
            {
                "role": "user",
                "content": f"{chart}. Question: {question}",
            }
        ],
        model="llama-3.1-8b-instant",
        max_completion_tokens=350
    )

    print(f"Answer: {chat.choices[0].message.content}")
    print(f"\nToken used: {chat.usage} \n----------------")

