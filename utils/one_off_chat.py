# utils/one_off_chat.py

import requests
import argparse
import os
from dotenv import load_dotenv

def get_response(prompt, model_name="google/flan-t5-base", api_key=None):
    """
    Get a response from the model
    
    Args:
        prompt: The prompt to send to the model
        model_name: Name of the model to use
        api_key: API key for authentication (optional for some models)
        
    Returns:
        The model's response
    """
    from huggingface_hub import InferenceClient

    # Replace with your actual Hugging Face API token
    load_dotenv()
    HF_TOKEN = os.getenv("API_KEY")
    client = InferenceClient(token = HF_TOKEN)
    response = client.text_generation(prompt = prompt)
    return response

def run_chat():
    """Run an interactive chat session"""
    print("Welcome to the Simple LLM Chat! Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        # TODO: Get response from the model
        response = get_response(user_input)
        print(response)
        
def main():
    parser = argparse.ArgumentParser(description="Chat with an LLM")

    # TODO: Add arguments to the parser
    args = parser.parse_args()
    
    # TODO: Run the chat function with parsed arguments
    run_chat()

if __name__ == "__main__":
    main()
