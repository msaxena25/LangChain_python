# Dashboard URL - https://weatherstack.com/dashboard

# Query URL - https://api.weatherstack.com/current?access_key=your_key&query=Delhi

'''
USER Query - What is the current weather in Delhi?
'''

import requests
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_react_agent
from Langchain_Code.shared.load_gemini_model import model
from langsmith import Client


# First Create a Tool that will fetch current weather based on provided City 

base_url = 'https://api.weatherstack.com/current?access_key=your_key'

# Define custom tool get current weather data for given city based on weatherstack API
@tool
def weather_tool(city: str) -> str:
    '''This tool fetches current weather data for given city'''
    api_url = f'{base_url}&query={city}'
    response = requests.get(api_url)
    return response.json()
    

# Pull the reusable ReAct prompt
prompt = Client().pull_prompt('hwchase17/react', dangerously_pull_public_prompt=True)

agent = create_react_agent(
    llm = model,
    tools= [weather_tool],
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=[weather_tool]
)

result = agent_executor.invoke({'input': 'What is the current weather in Delhi, India?'})
print(result)

# Intermediate Steps Log on Console

'''
> Entering new AgentExecutor chain...
Thought: I need to find the current weather in Delhi, India. I will use the weather_tool for this.
Action: weather_tool
Action Input: Delhi, India
Thought: I now know the final answer
Final Answer: The current weather in Delhi, India is clear with a temperature of 25°C, humidity at 52%, and a wind speed of 5 km/h from the North.
> Finished chain.
'''

# Final result

'''
{'input': 'What is the current weather in Delhi, India?', 'output': 'The current weather in Delhi, India is clear with a temperature of 25°C, humidity at 52%, and a wind speed of 5 km/h from the North.'}
'''
