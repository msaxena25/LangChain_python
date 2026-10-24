from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OpenAI example

llm = OpenAI(model='gpt-3.5-turbo-instruct')
result = llm.invoke("Who is prime minister of India?")
print(result) # This will print the response in string format from the LLM


#-----------------------------------------------------------

# ChatOpenAI example

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model='gpt-3.5-turbo-instruct')
result = model.invoke("Who is prime minister of India?")

print(result) # This will print the response from the LLM (content with additional information like tokens, uses etc.)
print(result.content) # This will print the response from the LLM (content only)

# Additional parameters while initializing the model

model = ChatOpenAI(model='gpt-3.5-turbo-instruct', temperature=0.5, max_completion_tokens=100)

#-----------------------------------------------------------

# Anthropic example

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model='claude-3-5-sonnet-20241022')
result = model.invoke("Who is prime minister of India?")
print(result.content) # This will print the response from the LLM

#-----------------------------------------------------------

# Google Gemini example

from langchain_google_genai import ChatGoogleGenerativeAI
model = ChatGoogleGenerativeAI(model='gemini-3.8-flash')
result = model.invoke("Who is prime minister of India?")
print(result.content) # This will print the response from the LLM

#-----------------------------------------------------------

# Use of Gemini embedding Model

from langchain_google_genai import GoogleGenerativeEmbedding

model = GoogleGenerativeEmbedding(model='gemini-3.8-flash', google_api_key="")
result = model.embed_query("Who is prime minister of India?")
print(result) # This will print the response from the LLM