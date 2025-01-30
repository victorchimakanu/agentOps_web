# AgentOps Web Assistant

## Overview

This application allows users to interact with an intelligent assistant that can answer questions based on specific documentation sources. The assistant uses OpenAI's language model to generate responses and maintains a session for tracking interactions.

## Features

- **Interactive Chat Interface**: Users can type questions and receive responses from the assistant.
- **Environment Variable Management**: The application loads sensitive API keys from a `.env` file to ensure security.

## Requirements

To run this application, you need the following:

- Python 3.7 or higher
- Required Python packages:
  - `dash`
  - `langchain`
  - `langchain_openai`
  - `langchain_community`
  - `python-dotenv`
  - `agentops`
  - `openai`

## Installation

1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```


2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**: In the root directory of the project, create a file named `.env` and add the following lines:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   AGENTOPS_API_KEY=your_agentops_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```


## Running the Application

1. **Start the Dash Application**:
   ```bash
   python webassist_layout2.py
   ```

2. **Access the Application**: Open your web browser and go to `http://127.0.0.1:8050/` to access the web assistant.

## Usage

- Type your question in the input field and click the "Ask AgentOps" button.
- The assistant will respond based on the information from the specified documentation sources.
- The chat history will be maintained during the session, allowing for a more interactive experience.

