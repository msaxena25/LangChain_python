# from langchain_openai import ChatOpenAI # this is not free available
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

# while True:
#     user_input =  input("You: ")
#     if (user_input == 'exit'):
#         break
#     result = model.invoke(user_input)
#     print("AI:", result)

'''
You: Hello My name is Mohit.
AI: Hello Mohit. How may I help you?
You: What is my Name?
AI: I dont have information of your name.
You: exit

'''

'''
You: Which number is bigger 2 or 4.
AI: 4
You: Ok. Now multiply bigger number with 10.
AI: 'It looks like you forgot to include the number! \n\nPlease tell me the number.
You: exit

'''

# So here AI dont have Context of your earlier conversation, thats why AI is not able to give correct answer based on Chat data. 

# Now Solution is - we need to main Chat History.

# Manual way to create memory
chat_history = []


# while True:
#     user_input =  input("You: ")
#     chat_history.append(user_input)
#     if (user_input == 'exit'):
#         break
#     result = model.invoke(chat_history)
#     chat_history.append(result.text)
#     print("AI:", result.text)

# print("You full chat history:", chat_history)

'''
You: which is bigger 2 or 5 ?.
AI: 5 is bigger than 2.
You: now add 10 to bigger number.
AI: The bigger number is 5. 

Adding 10 to 5 gives you **15**.
You: now multiply 20 with lesser number?
AI: The lesser number is **2**. 

Multiplying 20 by the lesser number (2):
20 × 2 = **40**
You: now which is bigger after 2 operations?
AI: To find out which is bigger after the two operations, let's compare the results:

* Result of the first operation (adding 10 to the bigger number): **15**
* Result of the second operation (multiplying 20 by the lesser number): **40**

Comparing **15** and **40**, **40** is bigger. 

So, the result of the second operation is the bigger number.
You: exit
You full chat history: ['which is bigger 2 or 5 ?', '5 is bigger than 2.', 'now add 10 to bigger number.', 'The bigger number is 5. \n\nAdding 10 to 5 gives you **15**.', 'now multiply 20 with lesser number?', 'The lesser number is **2**. \n\nMultiplying 20 by the lesser number (2):\n20 × 2 = **40**', 'now which is bigger after 2 operations?', "To find out which is bigger after the two operations, let's compare the results:\n\n* Result of the first operation (adding 10 to the bigger number): **15**\n* Result of the second operation (multiplying 20 by the lesser number): **40**\n\nComparing **15** and **40**, **40** is bigger. \n\nSo, the result of the second operation is the bigger number.", 'exit']

'''

# Lets implement Messages now with chatbot

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# lets set System Message first in our chat history list

chat_history.append(SystemMessage(content = "You are expert in web and mobile technologies"))

while True:
    user_input = input("You:" )
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.text))
    print("AI:", result.text)

print("Your Messages chat history", chat_history)

'''
Your Messages chat history 

[SystemMessage(content='You are expert in web and mobile technologies', additional_kwargs={}, response_metadata={}), 
HumanMessage(content='tell me one best feature of react js?', additional_kwargs={}, response_metadata={}), 
AIMessage(content='While React has many incredible attributes, the absolute best feature of React.js is its **Virtual DOM (Document Object Model) combined with its efficient Diffing Algorithm**. \n\n
Here is why this is a game-changer:\n\n### How it works:\nNormally, updating the UI in traditional web development requires directly manipulating the browser’s real DOM, 
which is slow and performance-heavy (causing the page to lag or re-render entirely). \n\nReact solves this by',
 additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]),
 HumanMessage(content='exit', additional_kwargs={}, response_metadata={})]
'''