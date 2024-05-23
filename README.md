# Cohere Chatbot Proxy
Welcome to the Cohere Chatbot Proxy project! This repository contains the code for a Flask-based web application that acts as a proxy service for Cohere AI, allowing users to generate text responses using Cohere's language model.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Demo](#demo)
- [License](#license)

## Introduction

The Cohere Chatbot Proxy provides an interface for interacting with the Cohere AI language model. It supports real-time text generation, session management, and more. This project includes a Flask server and a CLI for interacting with the API.

## Features

- **Real-time text generation**: Stream text responses from Cohere AI.
- **Session management**: Store and retrieve chat sessions for users.
- **WebSocket support**: Real-time communication using Socket.IO.
- **Simple web interface**: Basic web page to demonstrate that the proxy service is online.
- **HTTP support**: Handles normal HTTP requests like GET and POST.

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
    ```

4. Start the Flask server:
    ```sh
    python app.py
    ```

## Usage

### Web Interface

Open your browser and navigate to `http://localhost:5000` to access the web interface. You will see a welcome message indicating that the proxy service is online.

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

To use the CLI, navigate to the `cli-version-for-fast-testing` folder and run the following command:

```sh
python cli.py
```

## Demo

For those who prefer not to host the service themselves, you are welcome to use my hosted demo version available [here](https://cohere-ai.motoemotovps.xyz). Please be aware that this demo may have rate limits or might not be operational at all times.

## License

This project does not have a license. You are free to use, modify, and distribute the code as you see fit. Enjoy!
# websocket may not work right now working on fixing it
