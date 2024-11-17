# Django Chatbot Server

![Docker](https://img.shields.io/badge/docker-yes-brightgreen.svg)
![Django](https://img.shields.io/badge/django-4.2%2B-green.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

A **Django-based server** that powers a chatbot using OpenAI and Google APIs. This project is containerized with Docker for easy deployment and scalability.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Clone the Repository](#clone-the-repository)
  - [Environment Variables](#environment-variables)
  - [Docker Setup](#docker-setup)
    - [Build Docker](#build-docker)
    - [Run the Docker container](#run-the-docker-container)
- [Contacts](#contacts)

## Features

- **Chatbot Integration**: Utilizes OpenAI for natural language processing and Google APIs for enhanced functionalities.
- **Dockerized**: Simplifies deployment across different environments.
- **Environment Configuration**: Securely manages API keys and configurations using a `.env` file.
- **Scalable Architecture**: Designed to handle multiple requests efficiently.
- **Session Management**: Maintains chat history using Django sessions.
- **Streaming Responses**: Provides real-time chatbot responses using server-sent events.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Git](https://git-scm.com/downloads) installed.
- API keys for:
  - [OpenAI](https://openai.com/)
  - [Google](https://cloud.google.com/)

## Installation

### Clone the Repository

```bash
git clone https://github.com/ArtiomOn/chatbot.git
cd chatbot
```

### Environment Variables

Create a `.env` file in the project root directory and add the following environment variables:

```bash
## Required Environment Variables
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# Google API Key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_google_cse_id

## Optional Environment Variables, defaults are provided in settings.py
# Django credentials
SECRET_KEY=yoursecretkey
DEBUG=True

# OpenAI Model Name and Temperature
OPENAI_MODEL_NAME="gpt-3.5-turbo"
OPENAI_TEMPERATURE=0.7
```

# Docker Setup

### Build Docker

```bash
docker build -t chatbot .
```

### Run the Docker container

```bash
docker run -d -p 8000:8000 chatbot
```

## Access the Chatbot

Open your browser and navigate to `http://localhost:8000/` to access the chatbot.

There is also an option to search in Google via a checkbox in the top right corner, which you can enable or disable as needed.


### Contacts

- LinkedIn: [Artiom Oncea](www.linkedin.com/in/artiom-oncea-8b2174216)
- Telegram: [Artiom](https://t.me/art1292)