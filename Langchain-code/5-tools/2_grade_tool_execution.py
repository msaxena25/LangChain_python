# Bind Tools with LLM, Call Tools and Generate response

'''
MY Question  - 

Tell me two top IITs in India? And how much scholarship can I get if I achieve 400 marks out of 500.
'''


# Python module names should generally use letters, numbers, and underscores, and should not start with a number.
# Thats why below is Invalid import
# from 1_custom_tools import StudentToolkit


# Dynamically load Module with importlib

import importlib.util

spec = importlib.util.spec_from_file_location(
    "StudentToolkit",
    r"Langchain-code\5-tools\1_custom_tools.py"
)

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

StudentToolkit = module.StudentToolkit
# print(StudentToolkit)
# <class 'StudentToolkit.StudentToolkit'>

# Now lets implement complete tool-calling loop - 

'''
We'll implement the complete tool-calling loop for your example. The LLM will answer the general-knowledge question about two top IITs and use your student tools to calculate the grade and scholarship for 400 out of 500.

The key is that the LLM should receive the tool results back before generating its final answer. We'll also let it answer the IIT part using its own knowledge; the grade and scholarship calculations will come from your Python tools.
'''

print('Complete tool-calling loop............')

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_core.output_parsers  import StrOutputParser
from dotenv import load_dotenv
import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# We need LLM to implement complete tool calling
model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=200, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )


# Get all tools from Student Toolkit
student_toolkit = StudentToolkit()
toolkit_tools = student_toolkit.get_tools()
print('fetched tools', len(toolkit_tools))

# Bind our tools with above model
model_with_tools = model.bind_tools(toolkit_tools)

'''
Prompt template vs messages

Prompt template creates the messages sent to the LLM, while messages stores the conversation history during the tool-calling loop.

Why use messages - 

1. The prompt creates the initial messages.
2. The LLM returns a tool-call request.
3. The application executes the tool and adds its result as a ToolMessage.
4. The updated conversation is sent back to the LLM.
5. The LLM generates the final answer.
'''

tool_selection = {
    'Grade_Calculator': toolkit_tools[0],
    'scholarship_calculator_tool':  toolkit_tools[1]
}

messages  = [] # store all conversation history


system_message = SystemMessage("Answer the User's question based on provided tools")

messages.append(system_message) # push system message

# Converted Query to HumanMessage Object
query = HumanMessage('Tell me top 2 IITs in India? And how much scholarship can I get if I achieve 400 marks out of 500 in my entrance exam?')

# Push this into messages
messages.append(query)

#print('Messages:', messages)
'''
[SystemMessage(content="Answer the User's question based on provided tools", additional_kwargs={},response_metadata={}), HumanMessage(content='Tell me top 2 IITs in India? And how much scholarship can I get if I achieve 400 marks out of 500 in my entrance exam?', additional_kwargs={}, response_metadata={})]
'''

"""

# now invoke our model -  LLM Models return AIMessage 

response: AIMessage = model_with_tools.invoke(messages)

#print('Tool Calls analised by LLM for this request..')

# print(response.tool_calls)
'''
[{'name': 'Grade_Calculator', 'args': {'total_exam_marks': 500, 'obtained_marks': 400}, 'id': 'call_668761', 'type': 'tool_call'}]
'''

# NOTE  - Here single tool returned by LLM and that is Grade Calculator.

# Now push this AI Message as well into our messages list
messages.append(response)

# print('Messages:', messages)
'''
Messages: [
    SystemMessage(content="Answer the User's question based on provided tools", additional_kwargs={},response_metadata={}), 
    HumanMessage(content='Tell me top 2 IITs in India? And how much scholarship can I getif I achieve 400 marks out of 500 in my entrance exam?', additional_kwargs={}, response_metadata={}), 
    AIMessage(content=[], additional_kwargs={'function_call': {'name': 'Grade_Calculator', 'arguments': '{"total_exam_marks": 500, "obtained_marks": 400}'}, '__gemini_function_call_thought_signatures__': {'call_668761': 'EmAKXgFpFH0TT4O4PhYC0SOt7+pbx9q/oMhVp8JmQs22QktmnX2lfU8jsy2GoAZUHcN/ysLidYf+dDIEZJ2ypzHiqEU5EtN05123w8npiDeD8FAUXYbjWpu0ur1QykP95dU='}},
    response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-3.5-flash-lite', 'safety_ratings': [], 'model_provider': 'google_genai'}, id='lc_run--01a16d9d-01e5-7c10-8bdc-fcb5963960cb-0', 
    tool_calls=[{'name': 'Grade_Calculator', 'args': {'total_exam_marks': 500, 'obtained_marks': 400}, 'id': 'call_668761', 'type': 'tool_call'}], 
    invalid_tool_calls=[], usage_metadata={'input_tokens': 246, 'output_tokens': 28, 'total_tokens': 274, 'input_token_details': {'cache_read': 0}})]
'''

'''
Important -

LLM usually makes one tool-calling decision per response in this workflow. It can request the grade calculator first, then decide to call the scholarship calculator after receiving the grade result.

'''

# Now execute grade Tool first

grade_response: ToolMessage = tool_selection[response.tool_calls[0]['name']].invoke(response.tool_calls[0])
print('Grade tool response', grade_response)
'''
Grade tool response content='{"percentage": 80.0, "grade": "A+"}' name='Grade_Calculator' tool_call_id='call_1094227'
'''
messages.append(grade_response) # push grade tool response into messages

# Now call again LLM with messages
response: AIMessage = model_with_tools.invoke(messages)

messages.append(response)

print('Second tool request..')
#print(response.tool_calls)
'''
[{'name': 'scholarship_calculator_tool', 'args': {'grade': 'A+'}, 'id': 'call_519376', 'type': 'tool_call'}]
'''

# Call second requested tool now..
scholarship_response: ToolMessage = tool_selection[response.tool_calls[0]['name']].invoke(response.tool_calls[0])
print('Scholarship tool response', scholarship_response)
'''
Scholarship tool response content='{"eligible": true, "scholarship_amount": 50000}' name='scholarship_calculator_tool' tool_call_id='call_519376'
'''

messages.append(scholarship_response)

chain = model_with_tools | StrOutputParser()

# Now we need to do final LLM Call
final_response = chain.invoke(messages)

print('Final response')
print(final_response)
'''
Final response

The top 2 IITs in India are generally considered to be:
1. **IIT Bombay**
2. **IIT Delhi**

Regarding your entrance exam:
* You obtained **400 marks out of 500**, which is **80%**.
* Based on your percentage, you achieved a **Grade: A+**.
* With an **A+** grade, you are **eligible for a scholarship amount of ₹50,000**.
'''

"""

#------------------------------------------------------

# In above code we have called manually requested tools step by step, appended messages etc.

# Lets Refactor above code and make that dynamic using while loop - 

print('Optimized version of tool calling with while loop.............')

# First Call to get required tools
response: AIMessage = model_with_tools.invoke(messages)

# Now check until tools exists
while response.tool_calls:
    messages.append(response)
    selected_tool = tool_selection[response.tool_calls[0]['name']]
    tool_response: ToolMessage = selected_tool.invoke(response.tool_calls[0])
    messages.append(tool_response)
    response: AIMessage = model_with_tools.invoke(messages)

# final answer 
parser = StrOutputParser()
print(parser.invoke(response))
'''
Here are the answers to your questions:

1. **Top 2 IITs in India:**
   * **IIT Bombay** (Consistently ranked among the top institutes in India for engineering and technology)
   * **IIT Delhi** (Renowned for its academic excellence, research, and placement records)

2. **Scholarship Details based on your Exam Score:**
   * **Marks Obtained:** 400 out of 500 (80%)
   * **Grade:** A+
   * **Scholarship Eligibility:** Eligible
   * **Scholarship Amount:** ₹50,000
'''



#-------------------------------------------------------

# We have seen in above code that we actually required 2 tools to process our query but LLM returned single tool at a time. It did not returned both tool in first call.

# Lets try to change our system message and Human message - 

"""
system_message = SystemMessage(
    "Answer the User's question based on provided tools. "
    "To Calculate Grade: Use grade calculator tool first to calculate the student's grade. "
    "To Calculate Scholarship amount: Use scholarship Calculator tool with the grade returned by the first tool. "
    "Finally, explain the result to the user. "
    )

query = HumanMessage(
    "Tell me the top 2 IITs in India. If I score 400 out of 500, what grade will I get? Also, how much scholarship am I eligible for with that grade?")

messages.append(system_message)
messages.append(query)

response = model_with_tools.invoke(messages)
print(response.tool_calls)
# Still it returns only one tool at a time
'''
[{'name': 'Grade_Calculator', 'args': {'total_exam_marks': 500, 'obtained_marks': 400}, 'id': 'call_725038', 'type': 'tool_call'}]
'''

# NOTE  - It also returns all required tools but might be with free model, it is processing single tool at one time.

"""