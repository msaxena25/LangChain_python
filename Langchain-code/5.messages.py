
import langchain_core.prompts.chat
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
messages: list[HumanMessage | SystemMessage] = [
    SystemMessage(content = "You are expert in web technologies."),
    HumanMessage(content = "Tell me about React JS")
]

result: AIMessage = model.invoke(messages)

# you don't need to convert 'result' to AIMessage if 'model.invoke' already returns an AIMessage instance.
# messages.append(AIMessage(result))

messages.append(result)

print(messages)

'''
HumanMessage — user's message.

AIMessage — AI model's response.

SystemMessage — instructions that define the AI's behavior.
'''

#-------------------------------------

# Using tuple-based messages

# Tuple-based syntax is the concise, recommended option for most everyday use cases.

messages = [
    ("system", "You are expert in web technologies."),
    ("human", "Tell me about React JS")
]

response = model.invoke(messages)

'''
This is concise and commonly used with ChatPromptTemplate.

Supported roles commonly include system, human, and assistant. 

Tool interactions can also involve tool messages.
'''

#------------------------------------

# Using ChatPromptTemplate

# This approach is useful when messages contain dynamic variables or reusable instructions.

from langchain_core.prompts import ChatPromptTemplate

prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ("system", "You are expert in web technologies."),
    ("human", "Tell me about {technology}")
])

response = (prompt | model).invoke({
    "technology": "React JS"
})

#------------------------------------

# Use SystemMessage, HumanMessage way inside the ChatPromptTemplate

# But, these are fixed messages. You can't use template variables inside these messages.
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are an expert in web technologies."),
    HumanMessage(content="Tell me about React JS.")
])

#---------------------------------------------

# SystemMessagePromptTemplate & HumanMessagePromptTemplate

# SystemMessagePromptTemplate and HumanMessagePromptTemplate are templates that generate messages using dynamic variables.

from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are an expert in {technology}."
    ),
    HumanMessagePromptTemplate.from_template(
        "Explain {topic} to me."
    )
])

messages = prompt.invoke({
    "technology": "web technologies",
    "topic": "React JS"
})
