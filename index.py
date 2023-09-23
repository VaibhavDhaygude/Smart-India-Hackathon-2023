from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Put your URI endpoint:port here for your local inference server (in LM Studio)
openai.api_base = 'http://localhost:1234/v1'
# Put in an empty API Key
openai.api_key = ''

# Alpaca style prompt format:
prefix = "### Instruction:\n" 
suffix = "\n### Response:"

def get_completion(prompt, model="local model", temperature=0.0):
    formatted_prompt = f"{prefix}{prompt}{suffix}"
    messages = [{"role": "user", "content": formatted_prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_code', methods=['POST'])
def generate_code():
    prompt = request.form['prompt']
    response = get_completion(prompt, temperature=1)
    print(response)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
