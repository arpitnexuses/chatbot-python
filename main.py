from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
ASSISTANT_ID = "asst_SizeRJtLIRnks53yEh8G6fU5"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Create a thread with the user's message
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ]
    )

    # Submit the thread to the assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Wait for run to complete
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    # Get the latest message from the thread
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0].content[0].text.value

    return jsonify({'response': latest_message})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
