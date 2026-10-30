# Lets Create our First AI Agent using `create_tool_calling_agent`, `AgentExecutor`.

# This is Older apprach of Langchain 0.X Versions, while modern LangChain provides a higher-level API named create_agent(). 

'''
User Query: What is the capital of India, and what is its population?
'''

# Required Packages -

'''
pip install -U langchain langchain-google-genai langchain-community ddgs
'''

from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun

# Load shared Gemini model
from Langchain_Code.shared.load_gemini_model import model

serch_tool = DuckDuckGoSearchRun()

# Create a Prompt

prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ('system', 
     "You are a helpful research assistant. "
     "Use web search to answer factual questions. "
     ),
    ('human', '{user_query}'),
    ('placeholder', '{agent_scratchpad}')
])

'''
What is the meaning of ('placeholder', '{agent_scratched}')?

This adds a special placeholder to the prompt template, which allows the agent's internal scratchpad (thoughts and reasoning steps) to be shown to the LLM at each step. 

This helps the agent remember its previous thoughts/actions during the reasoning and action-taking loop.

If you miss this, You will get ValueError: Prompt missing required variables: {'agent_scratchpad'}
'''

agent = create_tool_calling_agent(
    llm = model,
    tools = [serch_tool],
    prompt = prompt,
)

# Agent executor is wrapper class that wraps the agent and tools together.

agent_executor = AgentExecutor(
    agent = agent,
    tools = [serch_tool],
    verbose = True,
    return_intermediate_steps=True
)

'''
verbose = true ?

Displays execution logs while the agent runs.

return_intermediate_steps=True	?

Returns the agent's tool actions and observations as part of the result dictionary.	result["intermediate_steps"]

'''

# result = agent_executor.invoke({"user_query": "What is the capital of India, and what is its population?"})

# print("Query:", result["user_query"])
# print("Answer:", result["output"])

'''
Query: What is the capital of India, and what is its population?

Answer: [{'type': 'text', 'text': 'The capital of India is **New Delhi**. \n\nIts population varies depending on how thearea is measured:\n* **New Delhi (the specific municipal district):** Has a smaller population of around 140,000 to 300,000 people.\n* **Delhi (the National Capital Territory and metropolitan area):** Serves as the wider urban capital regionand has a massive population estimated to be over **33 million** people', 'index': 0, 'extras': {'signature': 'EmAKXgFpFH0TlEz2btWPWiTxcWeptMZ4ZKAfRuc0YUBRTZehSt0DcHZmChXfi8GHYQ+pOT4Fu7uh+9WRWheIGlz4JO97F8aEuno+/2rYNfLO4SXvYaTCSAeKQJx/dEQm0fs='}}]

'''

# Intermediate Stes Log on Console

'''
Entering new AgentExecutor chain...

Invoking: `duckduckgo_search` with `{'query': 'capital of India population'}`

Generate Answer..

Invoking: `duckduckgo_search` with `{'query': 'New Delhi population 2024 or latest'}`

Generate Answer..

'''

'''
An Agent is the `decision-making component.` It cannot execute tool by itself.

`AgentExecutor` is the execution loop manager that manages, runs entire loop cycle - Thought – Action – Observation.
'''

#-------------------------------------------------------------

# Lets use ReAct prompt instead of our own Prompt template

'''
ReAct prompt is a predefined prompt template designed to guide an LLM through the ReAct pattern: Thought → Action → Observation → repeat.

Instead of writing this detailed prompt yourself, you can pull a reusable template from LangChain Hub. The classic ReAct prompt is published under the identifier `hwchase17/react`.

# Below way does not support pulling public prompts, It is older and deprecated.

from langchain_classic import hub
prompt = hub.pull("hwchase17/react")

hub.pull is also deprecated. Call the LangSmith client directly, which is the function that actually accepts dangerously_pull_public_prompt flag.

# Correct way to pull prompt - (using langsmith client)

from langsmith import Client
prompt = Client().pull_prompt(
    "hwchase17/react",
    dangerously_pull_public_prompt=True,
)

'''

# Agent - `create_react_agent` while in above code we have used `create_tool_calling_agent`

from langchain_classic.agents import (
    AgentExecutor,
    create_react_agent,
)

from langsmith import Client

prompt = Client().pull_prompt(
    "hwchase17/react",
    dangerously_pull_public_prompt=True,
)

# Create the agent
agent = create_react_agent(
    llm=model,
    tools = [serch_tool],
    prompt=prompt,
)

# Create the executor
agent_executor = AgentExecutor(
    agent=agent,
    tools = [serch_tool],
    verbose=True,
    return_intermediate_steps=True
)

result = agent_executor.invoke({
    "input": "What is the capital of India, and what is its population?"
})

print(result["output"])
'''
The capital of India is New Delhi (often referred to simply as Delhi), and its population is over 33 million people.
'''

# Intermediate Steps

'''
> Entering new AgentExecutor chain...
Thought: I need to find the capital of India and its population.
Action: duckduckgo_search
Action Input: capital of India and its population 2023 2024
Thought: I now know the final answer
Final Answer: The capital of India is New Delhi (often referred to simply as Delhi), and its population is over 33 million people.
> Finished chain.
'''


'''
If pull public prompt without prop `dangerously_pull_public_prompt`

You will get ERROR:

ValueError: Pulling a public prompt by owner/name is disabled by default because prompts may contain untrusted serialized LangChain objects. If you trust this prompt, set `dangerously_pull_public_prompt=True` to acknowledge the risk.
'''
