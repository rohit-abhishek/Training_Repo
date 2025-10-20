"""
API Client for LLaMA API Chat Service
This module provides a client class for interacting with the LLaMA API chat service using requests module. Refer program work_with_local_llm_client.py which uses ollama model
"""


import json 
import requests

url="http://localhost:11434/api/chat"
model="llama3.2"

payload={
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": "Is GIL removed in Python version 3.14? answer only if you are absolutely sure"
        }
    ]
}

response=requests.post(url=url, json=payload, stream=True)
if response.status_code==200:
    print(f"Streaming response from {model}: \n")
    for line in response.iter_lines(decode_unicode=True): 
        if line:
            try:
                json_data=json.loads(line)
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")

            except json.JSONDecodeError:
                print(f"Failed to parse line: {line}")

    print()

else: 
    print(f"Invalid Response from {model}: ", response.status_code, end="")