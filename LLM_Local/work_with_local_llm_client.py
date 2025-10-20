"""
API Client for LLaMA API Chat Service
This module provides a client class for interacting with the LLaMA API chat service using ollama package
"""


import ollama 

client=ollama.Client()
model="llama3.2"
prompt="what is python"

response=client.generate(model=model, prompt=prompt)
print(f"Response from {model}: ", response.response)