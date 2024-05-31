from flask import Flask, request, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    concept = request.form.get('concept')
    functionality = request.form.get('functionality')
    vibe = request.form.get('vibe')
    features = request.form.get('features')
    creativity = request.form.get('creativity')
    if creativity == 'unimaginative':
        temperature = 0.3
    elif creativity == 'normal':
        temperature = 0.5
    else:
        temperature = 1
    text_prompt = f"A creative and innovative plastic product designed for {functionality} that evokes a sense of {vibe} in the user. The product should be based on this concept: {concept}. It should be designed for 3D printing and consider limitations in size, complexity, and printability. Describe this product in detail, highlighting any special features if provided, but only in one sentence. special features:{features}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant who takes ideas from customers and makes plastic product designs to be made into a 3D printer."},
                {"role": "user", "content": text_prompt}
            ],
            temperature = temperature,
            max_tokens=100
        )
        description = response.choices[0].message.content

        image_response = client.images.generate(
            model="dall-e-2",
            prompt = f"A photorealistic image of a 3D-printed plastic product described as: {description}. Consider the limitations of 3D printing.",
            size="512x512",
            quality="standard",
            n=1
        )
        image_url = image_response.data[0].url

        return render_template('result.html', description=description, image_url=image_url)
    except Exception as e:
        return render_template('error.html', error=str(e))  # Render a separate error template

