import os
import random

import openai
from openai import OpenAI
from config import  apikey
client = OpenAI(api_key=apikey)

openai.api_key=apikey
def ai(prompt):

  text = f"OpenAI response for Prompt :{prompt} \n ******************\n\n"

  response = client.completions.create(
    model="davinci-002",  # latest model (the one used for GPT-3)
    prompt=prompt,
    temperature=random.randrange(50, 90) / 100,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    timeout=10
  )
  print(response.choices[0].text)

  text += response.choices[0].text
  if not os.path.exists("Openai"):
    os.mkdir("Openai")

  with open(f"Openai/prompt- {random.randint(1, 234343456)}", "w") as f:
    f.write(text)

ai("Helllo")
