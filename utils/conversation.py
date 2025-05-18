# utils/conversation.py

import requests
import argparse
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

def get_response(prompt, history=None, model_name="google/flan-t5-base", api_key=None, history_length=3):
    """
    Get a response from the model using conversation history
    
    Args:
        prompt: The current user prompt
        history: List of previous (prompt, response) tuples
        model_name: Name of the model to use
        api_key: API key for authentication
        history_length: Number of previous exchanges to include in context
        
    Returns:
        The model's response
    """
    # TODO: Implement the contextual response function
    # Initialize history if None
    if history is None:
        history = []

    # Limit history
    history = history[-history_length:]  

    # TODO: Format a prompt that includes previous exchanges
    context = ""
    for i, (prev_prompt, prev_response) in enumerate(history):
        context += f"User: {prev_prompt}\nAI: {prev_response}\n"
    context += f"User: {prompt}\nAI:"
    # Get a response from the API
    load_dotenv()
    token = os.getenv("API_KEY")
    client = InferenceClient(token = token)
    response = client.text_generation(prompt = context, max_new_tokens = 100)

    # Return the response
    return response.strip()

def run_chat():
    """Run an interactive chat session with context"""
    print("Welcome to the Contextual LLM Chat! Type 'exit' to quit.")
    
    # Initialize conversation history
    history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        # TODO: Get response using conversation history
        response = get_response(user_input, history)
        # Update history
        history.append((user_input, response))
        # Print the response
        print(f"AI: {response}")


def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM using conversation history")
    
    # TODO: Add arguments to the parser
    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    run_chat()

if __name__ == "__main__":
    main()
