from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=100, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )

# Defined System message and Humen Message
messages = [
    SystemMessage(content = "You are expert in web technologies."),
    HumanMessage(content = "Tell me about React JS")
]

result = model.invoke(messages)

# result that returns from LLM is called as AI Messsage so covert that to AI message format.
messages.append(AIMessage(result))

print(messages)

'''
HumanMessage — user's message.

AIMessage — AI model's response.

SystemMessage — instructions that define the AI's behavior.
'''