# Package required

'''
pip install -U langchain-ollama
'''

# Requirement - 

'''
Query - Know the refund status of my returned item.

1. Find the order status based on order Id 2233 in the database.
2. Find refund amount of that order Id.
3. Check for refund status of that refund order Id.
4. Return the refund status and refund amount.

'''

from langchain_core.tools import tool, InjectedToolArg
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
import json
from langchain_core.output_parsers import StrOutputParser
from typing import Annotated


# prepare static data for order

returned_orders = [
    {
        'refund_order_id': 1111,
        'order_id': 2233,
        'refund_amount': 900,
    },
    {
        'refund_order_id': 2222,
        'order_id': 2234,
        'refund_amount': 1200,
    },
    {
        'refund_order_id': 3333,
        'order_id': 2235,
        'refund_amount': 600,
    },
]

refund_status = [
    {
        'refund_order_id': 1111,
        'refund_status': 'Refunded successfully.',
    },
    {
        'refund_order_id': 2222,
        'refund_status': 'In Progress, It will be refunded in 2-3 days.',
    },
    {
        'refund_order_id': 3333,
        'refund_status': 'Once Order arrived to warehouse, it will be refunded in 4-5 business days.',
    },
]

# Now define tool functions to get the order and refund status.

@tool
def get_order_status(order_id: int) -> dict:
    '''Get the order status and refund amount for the given order id.'''
    result = {}
    selected_order = list(filter(lambda x: x['order_id'] == order_id, returned_orders))
    if(len(selected_order) == 0):
        return {'error': 'Order not found'}
    else:
        result = {'refund_order_id': selected_order[0]['refund_order_id'], 'refund_amount': selected_order[0]['refund_amount']}
    
    return result

@tool
def get_refund_status(refund_order_id: Annotated[int, InjectedToolArg]) -> dict:
    '''Get the refund status for the given order id.'''
    result = {}
    selected_refund = list(filter(lambda x: x['refund_order_id'] == refund_order_id, refund_status))
    if(len(selected_refund) == 0):
        return {'error': 'Refund not found'}
    else:
        result = {'refund_status': selected_refund[0]['refund_status']}
    return result

# Now define the tool functions using langchain_core.tools.tool decorator.

tools = [get_order_status, get_refund_status]

# Create Model with ChatOllama.
model = ChatOllama(model="llama3.1:8b", temperature=0.1)

# Bind tools to the model.
model_with_tools = model.bind_tools(tools)

#response = model_with_tools.invoke("What is the refund status of my returned item for order Id 2234.")
#print(response.tool_calls)
'''
[{'name': 'get_refund_status', 'args': {'order_id': 2234}, 'id': 'c9b46353-6add-429b-b122-89836edc3ff3', 'type': 'tool_call'}]

For above query, Model is unable to identify that it needs first get_order_status tool to get the order status.

'''

"""


messages = []
messages.append(SystemMessage(content="You are a helpful assistant that can check the order status and refund status of a returned item."))
messages.append(HumanMessage(content="Check Order status and then check refund status for order Id 2234."))

# Change query
response: AIMessage = model_with_tools.invoke(messages)
messages.append(response)
print(response.tool_calls)
'''
[{'name': 'get_order_status', 'args': {'order_id': 2234}, 'id': '25b7c0cb-8cff-4088-8cef-42dfa08bf171', 'type': 'tool_call'},
 {'name': 'get_refund_status', 'args': {'refund_order_id': 2234}, 'id': '24c3900f-dc79-4b79-915f-b96d70fdf328', 'type': 'tool_call'}]
'''

for tool in response.tool_calls:
    tool_name = tool['name']
    tool_args = tool['args']
    if (tool_name == 'get_order_status'):
        result = get_order_status.invoke(tool_args)
        refund_order_id = result['refund_order_id'] # save the refund order id for next tool call
    elif (tool_name == 'get_refund_status'):
        tool_args['refund_order_id'] = refund_order_id
        result = get_refund_status.invoke(tool_args)
    messages.append(
        ToolMessage(
            content=json.dumps(result),
            tool_call_id=tool['id'], # required prop.
            name=tool_name,
        )
    )

print('Messages: ', messages)
print('--------------------------------')


final_response = model_with_tools.invoke(messages)
print('Final Response: ', StrOutputParser().invoke(final_response))
'''
Final Response:  The order status for order ID 2234 is currently being processed. The refund status for the returned item is in progress and will be refunded within 2-3 days.
'''


#-------------------------------------------------------

"""

print('Try Code Using Chain...')

# Do above Code using Chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Define Prompt with system and human messages.
prompt = ChatPromptTemplate.from_messages([
    ('system', "You are a helpful assistant that can check the order status and refund status of a returned item."),
    ('human', "Check Order status and then check refund status for order Id {order_id}."),
])

# Define messages list to store the history messages and tool calls.
messages = []

# Create First chain to get the tool calls & store the prompts
chain1 = RunnablePassthrough.assign(
    history = prompt, # contains the formatted messages with order_id variable.
    tool_calls = prompt | model_with_tools | RunnableLambda(lambda x: x.tool_calls)) # contains the tool calls.

'''
history:  [SystemMessage(content='You are a helpful assistant that can check the order status and refund status of areturned item.', additional_kwargs={}, response_metadata={}), HumanMessage(content='Check Order status and then check refund status for order Id 2235.', additional_kwargs={}, response_metadata={})]

Tool Calls:  [{'name': 'get_order_status', 'args': {'order_id': 2235}, 'id': 'a3338533-712f-4cc6-9736-0cd28c76a44b', 'type': 'tool_call'}, {'name': 'get_refund_status', 'args': {'order_id': 2235}, 'id': '58a6da49-f044-48b3-8240-cd3865bcb0aa', 'type': 'tool_call'}]
'''


# Define functions to process the tool calls.
def process_tool_calls(chain1_response):
    history = chain1_response["history"].to_messages() # convert the history to messages list.
    messages.extend(history) # add the history to messages list.
    tool_calls = chain1_response["tool_calls"]
    print('Tool Calls: ', tool_calls)
    for tool in tool_calls: 
        tool_name = tool['name']
        tool_args = tool['args']
        if (tool_name == 'get_order_status'):
            result = get_order_status.invoke(tool_args)
            refund_order_id = result['refund_order_id'] # save for next tool call
        elif (tool_name == 'get_refund_status'):
            tool_args['refund_order_id'] = refund_order_id
            result = get_refund_status.invoke(tool_args)
        messages.append(
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool['id'], # required prop.
                name=tool_name,
            )
        )
    print('Messages: ', messages)
    return messages


'''
Messages:

[
SystemMessage(content='You are a helpful assistant that can check the order status and refund status of a returned item.', additional_kwargs={}, response_metadata={}), 
HumanMessage(content='Check Order status and then check refund status for order Id 2235.', additional_kwargs={}, response_metadata={}), ToolMessage(content='{"refund_order_id": 3333, "refund_amount": 600}', name='get_order_status', tool_call_id='d5c1aff1-8239-4329-a65b-5e860097949f'), 
ToolMessage(content='{"refund_status": "Once Order arrived to warehouse, it will be refunded in 4-5 business days."}', name='get_refund_status', tool_call_id='b9728b77-70e7-4a1c-87ba-24f657f098b6')
]
'''


# Create Second chain to process the tool calls.
chain2 = chain1 | RunnableLambda(process_tool_calls)

# Create Final chain to get the final response.
final_chain = chain2 | model_with_tools | StrOutputParser()


result = final_chain.invoke({'order_id': 2235})
print('Result: ', result)
'''
Result:  I've checked the order status and refund status for order ID 2235.

**Order Status:** The order has been received by our warehouse and is currently being processed for refund.

**Refund Status:** Your refund of $600 (refund order ID 3333) will be processed once the order arrives at our warehouse. Please allow 4-5 business days for the refund to be processed.
'''




#-----------------------------------------------------------------------------------------------




#Observations - 

'''
Error - ValueError: Function must have a docstring if description not provided.

If you dont define the description of the tool function, it will give you above error.
'''

'''
@tool turns the function into a LangChain runnable. .invoke() only validates the arguments and calls the function. 

But It does not wrap result to ToolMessage by itself. So we need to wrap the result to ToolMessage by ourselves.

messages.append(
    ToolMessage(
        content=json.dumps(result), # convert to string
        tool_call_id=tool["id"], # required to match the tool call id with the tool call id in the response.
        name=tool_name, # required to match the tool name with the tool name in the response.
    )
)
'''

'''
InjectedToolArg

InjectedToolArg in LangChain marks a tool argument that should be supplied or injected by your application, not generated by the LLM.

from typing import Annotated
from langchain_core.tools import tool, InjectedToolArg


@tool
def get_refund_status(refund_id: Annotated[str, InjectedToolArg]) -> str:

'''