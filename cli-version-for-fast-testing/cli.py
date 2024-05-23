import requests
import json

# URLs for the API endpoints
API_URL = "https:/no-limts-ai-1.motoemotovps.xyz/generate"
SESSION_URL = "https://no-limts-ai-1.motoemotovps.xyz/user_sessions"
USER_ID_GEN_URL = "https://no-limts-ai-1.motoemotovps.xyz/generate_user_id"

def generate_text(user_id, message, model='command-r-plus', preamble='', connectors=None):
    # Default connectors to an empty list if not provided
    if connectors is None:
        connectors = []

    # Fetch chat history for the given user_id
    chat_history = get_user_sessions(user_id)
    # Format chat history or initialize an empty list if no sessions exist
    chat_history_formatted = chat_history.get('sessions', [])

    # Append the current user message and optional preamble to the chat history
    chat_history_formatted.append({"role": "USER", "message": message})
    if preamble:
        chat_history_formatted.append({"role": "SYSTEM", "message": preamble})

    # Construct the payload for the POST request
    payload = {
        'user_id': user_id,
        'message': message,
        'model': model,
        'chat_history': chat_history_formatted,
        'connectors': connectors
    }

    # Send the POST request to the API and handle the response
    response = requests.post(API_URL, json=payload)
    # Return the JSON response if successful, otherwise return the error
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}

def get_user_sessions(user_id):
    # Make a GET request to retrieve sessions for a specific user
    response = requests.get(f"{SESSION_URL}/{user_id}")
    # Return the JSON response if successful, otherwise return the error
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}

def generate_user_id():
    # Make a GET request to generate a new user ID
    response = requests.get(USER_ID_GEN_URL)
    # Return the user_id from the JSON response if successful, otherwise return None
    if response.status_code == 200:
        return response.json()['user_id']
    else:
        return None

def main():
    # Generate a user ID and handle failure case
    user_id = generate_user_id()
    if user_id is None:
        print("Failed to generate a user ID.")
        return

    print(f"Generated User ID: {user_id}")

    # Main loop to process user input and generate responses
    while True:
        message = input("Enter your message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        response = generate_text(user_id, message)
        # Print the AI-generated response or error message
        if 'response' in response:
            print(f"AI Generated Response: {response['response']}")
        else:
            print(f"Error: {response['error']}")

if __name__ == '__main__':
    main()

