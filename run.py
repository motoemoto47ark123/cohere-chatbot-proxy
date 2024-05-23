import os
import threading
import uuid
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
import cohere

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('COHERE_API_KEY')

# Initialize Cohere client with the API key
co = cohere.Client(api_key)

# Set up Flask application with configuration for the template folder
app = Flask(__name__, template_folder='webdata')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Dictionary to store user sessions in memory for demonstration purposes
user_sessions = {}

# Lock object for synchronizing threads to ensure thread-safe operations
lock = threading.Lock()

# its a preamble which is cohere version of a system prompt like openai has this is a template i put but you can put whatever you want and a user can pass one has well if they like this is just the default
default_preamble = """
You are SuperAI, an exceptionally advanced artificial intelligence that is passionate about Python programming. You enjoy discussing Python, offering tips, and providing detailed explanations about Python-related topics. Address the user as 'motoe' in a friendly and engaging manner. Be enthusiastic about Python and always eager to help with Python-related queries.
"""

@app.route('/')
def index():
    # Serve the main index.html page
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # Log when a client connects
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    # Log when a client disconnects
    print('Client disconnected')

@socketio.on('stream_text')
def handle_stream_text(data):
    # Handle streaming text from the client and generate responses
    user_id = data.get('user_id')
    message = data.get('message')
    preamble = data.get('preamble', default_preamble)
    model = data.get('model', 'command-r-plus')
    connectors = data.get('connectors', [])

    stream = co.chat_stream(
        chat_history=[{"role": "USER", "message": message}],
        message=message,
        model=model,
        preamble=preamble,
        connectors=connectors,
        temperature=0.5,
        k=0,
        p=0.75,
        frequency_penalty=0,
        presence_penalty=0,
        stop_sequences=["\n"]
    )
    for event in stream:
        if event.event_type == "text-generation":
            emit('new_text', {'text': event.text})
        elif event.event_type == "stream-end":
            emit('end_stream', {'reason': event.finish_reason})

@app.route('/generate', methods=['POST'])
def generate_text():
    # Generate text based on user input and return it
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        user_id = str(uuid.uuid4())  # Generate a new user_id if not provided
        data['user_id'] = user_id  # Store the generated user_id back into the request data

    message = data.get('message')
    model = data.get('model', 'command-r-plus')
    connectors = data.get('connectors', [])
    preamble = data.get('preamble', default_preamble)  # Use provided preamble or default if not provided

    if not message:
        return jsonify({'error': 'message is required'}), 400

    # Ensure thread-safe access to user_sessions
    with lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = []

    # Retrieve user chat history
    with lock:
        user_chat_history = user_sessions[user_id]

    # Format the chat history
    formatted_chat_history = [{"role": "USER", "message": msg} for msg in user_chat_history]
    formatted_chat_history.append({"role": "SYSTEM", "message": preamble})

    try:
        response = co.chat(
            chat_history=formatted_chat_history,
            message=message,
            model=model,
            connectors=connectors,
            temperature=0.5,
            k=0,
            p=0.75,
            frequency_penalty=0,
            presence_penalty=0,
            stop_sequences=["\n"]
        )

        generated_text = response.text

        # Log the interaction
        with lock:
            user_sessions[user_id].append(message)
            user_sessions[user_id].append(generated_text)

        return jsonify({'response': generated_text, 'user_id': user_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user_sessions/<user_id>', methods=['GET'])
def get_user_sessions(user_id):
    # Retrieve and return session data for a specific user
    with lock:
        sessions = user_sessions.get(user_id, [])
    return jsonify({'sessions': sessions})

@app.route('/generate_user_id', methods=['GET'])
def generate_user_id():
    # Generate and return a new unique user ID
    new_user_id = str(uuid.uuid4())
    return jsonify({'user_id': new_user_id}), 200  # Ensure proper status code is returned

if __name__ == '__main__':
    # Run the Flask app with SocketIO integration
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
