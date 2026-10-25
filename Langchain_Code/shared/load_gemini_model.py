# This file is used to load the Gemini model.

'''
We required model to test each peice of code.

So We have created this file in a shared folder to avoid duplication of code.

We canot keep this file inside our folder '1-models' because it is not a valid import path.

A normal import cannot reach that file, because 1-models starts with a number and contains a hyphen, so it is not a valid Python package name.
'''

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