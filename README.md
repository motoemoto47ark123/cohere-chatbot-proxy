# Cohere Chatbot Proxy

Welcome to the Cohere Chatbot Proxy project! This repository contains the code for a Flask-based web application that acts as a proxy service for Cohere AI, allowing users to generate text responses using Cohere's language model.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Demo](#demo)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Cohere Chatbot Proxy provides an interface for interacting with the Cohere AI language model. It supports real-time text generation, session management, and more. This project includes a Flask server and a CLI for interacting with the API.

## Features

- **Real-time text generation**: Stream text responses from Cohere AI.
- **Session management**: Store and retrieve chat sessions for users.
- **WebSocket support**: Real-time communication using Socket.IO.
- **Simple web interface**: Basic web page to demonstrate the proxy service.

## Setup

To set up the project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/motoemoto47ark123/cohere-chatbot-proxy.git
    cd cohere-chatbot-proxy
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following content:
    ```
    COHERE_API_KEY=your_cohere_api_key
    FLASK_SECRET_KEY=your_flask_secret_key
    ```

4. Start the Flask server:
    ```sh
    python app.py
    ```

## Usage

### Web Interface

Open your browser and navigate to `http://localhost:5000` to access the web interface. You will see a welcome message and can interact with the proxy service.

### API Endpoints

- **Generate text**: `POST /generate`
    ```json
    {
        "user_id": "your_user_id",
        "message": "your_message",
        "model": "command-r-plus",
        "connectors": [],
        "preamble": "optional_preamble"
    }
    ```

- **Get user sessions**: `GET /user_sessions/<user_id>`

- **Generate new user ID**: `GET /generate_user_id`

### CLI

The CLI script is located in the repository. To use the CLI, run the following command:

```sh
python cli.py
```

This will start the CLI, allowing you to interact with the Cohere Chatbot Proxy.

## Demo

Check out a live demo of the proxy service [here](https://no-limts-ai-1.motoemotovps.xyz).

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to follow the existing code style and include tests for new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
