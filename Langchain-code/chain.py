
# Chain

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

import time

start = time.perf_counter()

from dotenv import load_dotenv
import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

prompt = PromptTemplate(
    template="Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.",
    input_variables=["yourName","companyName", "profileName"],
    partial_variables={"companyName": "Nagarro"},
    validate_template=True
)

# print("Prompt creation time:", round(time.perf_counter() - start, 2), "seconds")

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=100, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )

# timeout=20: limits how long the request can wait, where supported by the integration.
# max_retries=0: disables automatic retries, helping reveal failures sooner.

parser = StrOutputParser() # parser takes the AI message and returns plain text.

print("Sending request to Gemini...", flush=True)
'''
Key takeaway: StrOutputParser is useful when you want plain text. For structured data, such as a JSON object with name, skills, and experience, you can use structured output or a suitable JSON parser instead.
'''

# Example of simple chain

chain =  prompt | model | parser

# Uncomment below to test 

# try:
#     response = chain.invoke({
#     "yourName": "Ashish",
#     "profileName": "Senior Frontend developer"
#     })
#     print(response) # we dont need to do response.content because we used parser in chain already.
# except Exception as error:
#     print("Error:", repr(error))
# finally:
#     print("Elapsed:", round(time.perf_counter() - start, 2), "seconds")

# below response is not full becasue max token limit is 100. But no worries, Chain is working.

'''
Hello Ashish! It’s great to connect with a fellow Nagarrian (or someone in the Nagarro ecosystem). Nagarro is known for its "fluidic" enterprise culture, which offers fantastic opportunities for growth, especially in technical and leadership tracks. 

As a **Senior Frontend Developer** at a company like Nagarro, you are already past the mid-level execution phase. You understand component lifecycles, state management, web performance, and modern frameworks (
'''
#_________________________________________________________________________________________________

# Sequental Chain

prompt1 = PromptTemplate.from_template("Write a short description of produt {productName}")

promp2 = PromptTemplate.from_template("Write 2 key points for me on why should buy based on this description {description}")

chain1 =  prompt1 | model | parser

# print('chain 1 structure > ', chain1)

'''
first=PromptTemplate(input_variables=['productName'], input_types={}, partial_variables={}, template='Write a short description of produt {productName}') middle=[ChatGoogleGenerativeAI(metadata={'lc_versions': {'langchain-core': '1.6.9', 'langchain': '1.4.4', 'langchain-google-genai': '4.4.1'}}, profile={'name': 'Gemini 3.5 Flash Lite', 'release_date': '2026-07-21', 'last_updated': '2026-07-21', 'open_weights': False, 'max_input_tokens': 1048576, 'max_output_tokens': 65536, 'text_inputs': True, 'image_inputs': True, 'audio_inputs': True, 'pdf_inputs': True, 'video_inputs': True, 'text_outputs': True, 'image_outputs': False, 'audio_outputs': False, 'video_outputs': False, 'reasoning_output': True, 'tool_calling': True, 'structured_output': True, 'attachment': True, 'temperature': True, 'image_url_inputs': True, 'image_tool_message': True, 'tool_choice': True, 'reasoning_effort_levels': ['minimal', 'low', 'medium', 'high'], 'reasoning_effort_default': 'minimal'}, google_api_key=SecretStr('**********'), model='gemini-3.5-flash-lite', temperature=None, max_output_tokens=100, max_retries=0, timeout=20.0, client=<google.genai.client.Client object at 0x00000224F5A58440>, default_metadata=(), model_kwargs={})] last=StrOutputParser()
'''

# Chain 2 is depend on chain1 output - thats why we are using Seqential Chain

chain2 =  {'description' : chain1} | promp2 | model | parser

# print('chain 2 ', chain2)

# uncomment to test
# result = chain2.invoke({'productName': 'LG Compact size frize under 300 Litre for small home'})

# print(result)

'''
Based on the description provided, here are 2 key reasons to buy:

1. **Space-Saving Design:** Perfectly sized for under 300 liters, making it ideal for compact living spaces like small apartments, studios, and small kitchens.
2. **Hassle-Free Maintenance:** Features frost-free technology, meaning you never have to manually defrost the freezer.
'''

#_________________________________________________________________________________________________

# Parellel Chain

from langchain_core.runnables import RunnableParallel

prompt3 =  PromptTemplate(
    template="Write 2 key benifits or pros of produt {productName}",
    input_variables=["productName"]
)

prompt4 =  PromptTemplate(
    template="Write 2 disadvantages or cons of same produt {productName}",
    input_variables=["productName"]
)

# prompt 3 and prompt 4 are independent so we can execute both in parallel.

chain3 = prompt3 | model | parser
chain4 = prompt4 | model | parser

# Now lets combine both chains in Parellel using RunnableParallel class

runnable_parellel = RunnableParallel(
    pros = chain3,
    cons = chain4
)

# uncomment to test 
#output = runnable_parellel.invoke({'productName', 'LG Compact size frize under 300 Litre for small home'})

#print('RunnableParellel output > ', output)

'''
{'pros': 'Here are 2 key benefits of the **LG Compact Size Fridge (Under 300 Litres)**:\n\n1. **Space-Saving Compact Design:** Its smaller footprint is specially engineered for small homes, apartments, or studio kitchens, allowing you to maximize your floor space without sacrificing essential food storage.\n2. **Energy Efficiency for Lower Bills:** With a capacity under 300 litres, this fridge typically consumes less electricity compared to large-capacity models, helping', 'cons': 'Here are 2 common disadvantages or cons of an LG compact-size fridge (under 300 liters) for a small home:\n\n1. **Limited Storage and Freezer Capacity:** \n   Because of its compact dimensions, the interior space—especially the freezer compartment—is quite limited. It may struggle to store bulk groceries, large meal-prep containers, or tall bottles, making it less suitable if you like to stock up on food for the week or frequently host'}
'''

# Output is a dictionary containing both results.

# print(output['pros'])

'''
Here are 2 key benefits of the **LG Compact Size Fridge (Under 300 Litres)**:

1. **Space-Saving Compact Design:** Its smaller footprint is specially engineered for small homes, apartments, or studio kitchens, allowing you to maximize your floor space without sacrificing essential food storage.
2. **Energy Efficiency for Lower Bills:** With a capacity under 300 litres, this fridge typically consumes less electricity compared to large-capacity models, helping
'''

# print(output['cons'])

'''
Here are 2 common disadvantages or cons of an LG compact-size fridge (under 300 liters) for a small home:

1. **Limited Storage and Freezer Capacity:** 
   Because of its compact dimensions, the interior space—especially the freezer compartment—is quite limited. It may struggle to store bulk groceries, large meal-prep containers, or tall bottles, making it less suitable if you like to stock up on food for the week or frequently host
'''

#_________________________________________________________________________________________________

# Merge Chain with | operator

prompt5 =  PromptTemplate(template="I have small family of 3 members and small house, now based on pros and cons, simply suggest me, do I need to buy or not in 1 line")

chain5 =  prompt5 | model | parser

# Now lets merge simply these two runnale_parellel and this chain5

chain6 = runnable_parellel | chain5

# chain6.invoke({''})


#_________________________________________________________________________________________________

# Conditional Chain

# Let's create a conditional chain for sentiment analysis using RunnableBranch.


# Requirement:

#- If feedback is positive → thank the customer and encourage them to share more feedback.
#- If feedback is negative → apologize and offer help resolving the issue.

from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import Literal  #Literal comes in typing package

# Why definding this schema
# Because - We dont want LLM return anything else positive or negative (just single word) because further chains are totally depend on this word.
class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field("This is sentiment of feedback")

# Create structured output using parser
pydanticParser = PydanticOutputParser(pydantic_object=Feedback)

# Now pass output instruction with this prompt template
prompt7 = PromptTemplate(
    template= """
    Classify the following customer feedback as either positive or negative.
    Feedback: {feedback}
    {format_instruction}
    """,
    input_variables=["feedback"],
    partial_variables={'format_instruction': pydanticParser.get_format_instructions()}
)

# prompt7 required this parser - pydanticParser
chain7 = prompt7 | model | pydanticParser

# below run chain7 to test only what will be the output
'''
result = chain7.invoke({'feedback': 'This smartphone is very poor and does not work properly, Dont buy this.'})


print('Sentiment is ', result)
# sentiment='negative'
'''

# positive feedback reply prompt
prompt8 = PromptTemplate(
    template="""
    The customer gave positive feedback: {feedback}
    Thank the customer warmly and encourage them to share
    their experience with others.
    """,
    input_variables=["feedback"]
    )

# negative feedback reply prompt
prompt9 = PromptTemplate(
    template="""
    The customer gave negative feedback: {feedback}
    Apologize politely and offer help resolving the issue.
    """,
    input_variables=["feedback"]
    )

conditional_chain = RunnableBranch(
        (lambda x: x.sentiment == 'positive', prompt8 | model | parser),
        (lambda x: x.sentiment == 'negative', prompt9 | model | parser),
        RunnableLambda(lambda x: "No sentiment found.")
)

# this default - (lambda x: "No sentiment found.") is not a chain and RunnableBranch only need chains so we can covert this to a chain using RunnableLambda.

final_chain = chain7 | conditional_chain

result = final_chain.invoke({'feedback': 'This smartphone is very poor and does not work properly, Dont buy this.'})

print('Feedback result ', result)
'''
Feedback result  Dear Customer,

We are truly sorry to hear that you had a negative experience with us, and we completely understand your frustration. We always strive to provide the best possible service, and it is clear we fell short this time. 

We would love the opportunity to make things right for you. Please let us know the details of the issue you experienced, and our team will jump right in to help resolve it as quickly as possible. 
'''
