from typing_extensions import TypedDict
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

# Schema
class Response(TypedDict):
    langName: str
    currentVersion: int
    creator: str
    whyPopular: str

# define type Response.
# When you will hover on field , it will give you suggesion of type
# test_response: Response = {"langName": "ABC", "currentVersion": 1, "creator": 'ABC', "whyPopular": 'ABC'}

# Below will also work - 
# test_response: Response = {"langName": "ABC", "currentVersion": '1', "creator": 'ABC', "whyPopular": 'ABC'}




# with_structured_output - method is used to set Typed Schema with Model.
structured_model = model.with_structured_output(Response)

response = structured_model.invoke(
    "Tell me about Python programming language."
)

print(response)
print(response["langName"])
print(response["currentVersion"])
print(response["creator"])
print(response["whyPopular"])

'''
{'langName': 'Python', 'currentVersion': 3, 'creator': 'Guido van Rossum', 
'whyPopular': 'Python is popular due to its readable syntax, extensive standard library, 
and strong community support, making it ideal for beginners and experts alike across fields 
like web development, data science, and artificial intelligence.'}

Python
3
Guido van Rossum
Python is popular due to its readable syntax, extensive standard library, and strong community support, making it ideal for beginners and experts alike across fields like web development, data science, and artificial intelligence.
'''

# use Annotated with TypedDist

# add metadata or extra information with schema so that Model can easily identify what is purpose of which field

from typing_extensions import TypedDict, Annotated

class Response(TypedDict):
    langName: Annotated[str, "What is Language name which user is asking"]
    currentVersion: int
    creator: str
    whyPopular: Annotated[str, "2 lines why that language is so popular now a days"]

