# What is an AI agent?

An AI agent is an `LLM-powered system` that can decide what action to take, use tools, observe the results, and continue taking actions until it reaches a goal or decides to stop.

---

# Agent and AgentExecutor

**Notes** - Creating seperate Agent and AgentExecutor is older apprach of Langchain 0.X Versions, while modern LangChain provides a higher-level API named create_agent().  We will learn both one by one.

## 1. What is an Agent?

An Agent is the `decision-making component.` It uses an LLM to decide which tool to call, what arguments to provide, or whether it has enough information to return a final answer.

For example, your student scholarship system has two tools:

- `grade_calculator`
- `scholarship_calculator`

The agent decides that it should calculate the grade first and then use that grade to check scholarship eligibility.

## 2. What is AgentExecutor?

`AgentExecutor` is the execution loop manager that manages, runs entire loop cycle - Thought–Action–Observation.

It takes the agent's requested action, executes the corresponding tool, returns the tool's result to the agent, and continues until the agent finishes or a stopping limit is reached.

## 3. How do they work together?

- User request: Calculate grade and scholarship for 400/500 marks.
- Agent: Decides which tool to call next.
- AgentExecutor: Executes the requested tool and returns its result.
- Agent: Uses the grade result to request the scholarship tool.
- AgentExecutor: Executes the requested tool and returns its result (if any).

The cycle repeats as needed. The agent makes decisions; the executor manages their execution.

## 4. Key differences

| Feature                             | Agent                      | AgentExecutor                          |
| ----------------------------------- | -------------------------- | -------------------------------------- |
| Main role                           | Decide what to do          | Run the decisions                      |
| Selects tools                       | Yes, through the LLM       | Executes the selected tools            |
| Executes tools                      | Not by itself              | Yes                                    |
| Manages the action-observation loop | Defines the next action    | Runs the loop                          |
| Stops the process                   | Can request a final answer | Handles stopping conditions and limits |

## 5. What about modern LangChain?

In the traditional API, you might see an `AgentExecutor` wrapping an agent.

In modern LangChain, the commonly recommended high-level API is `create_agent`. It provides an agent runtime that handles the tool-calling loop, so you generally don't need to create a separate `AgentExecutor`.

Remember this simple distinction:

- Agent = decision-maker.
- AgentExecutor = execution-loop manager.
- Modern `create_agent` = the higher-level API that brings agent behavior and execution together.

------

# Agent and AgentExecutor cycle

**Step 1: User submits a query**

The user sends a request to the agent system. For example, “Calculate my grade and check my scholarship eligibility.”

**Step 2: AgentExecutor prepares the input**

The AgentExecutor passes the user query and the available conversation or `intermediate-step context` to the agent. Initially, there may be no previous intermediate steps.

**Step 3: Agent decides what to do**

The agent uses the LLM to `interpret the query` and `decide` whether it needs a tool or can answer directly. If a tool is needed, it returns an action containing the tool name and its input.

**Step 4: AgentExecutor executes the action**

The executor identifies the requested tool, passes it the required input, and executes it. For example, it calls `grade_calculator` with the student's marks.

**Step 5: Tool result becomes the observation**

The tool returns its result. For example, `Grade: A+`. This result is called the `observation`.

**Step 6: Executor records the intermediate step (means its conversation history or context or thought-trace)**

The executor keeps track of the action and its observation. This becomes part of the context available for the next agent decision.

**Step 7: The cycle repeats**

The agent receives the updated context and decides what to do next. It may call another tool, use the previous result, or decide that it has enough information to answer.

**Step 8: The agent returns the final answer**

The loop stops when the agent produces a final answer or a stopping condition is reached, such as an iteration limit or an execution error.

-------

# ReAct Design Pattern

ReAct `(Reasoning and Acting)` is an AI agent design pattern in which an LLM reasons about what to do next, takes an action using a tool, observes the result, and repeats this cycle until it can provide the final answer.

**Cycle:** `Thought → Action → Observation → Repeat → Final Answer`

**ReAct combines two capabilities:**

- `Reasoning`: The LLM decides what information it needs and what to do next.
- `Acting`: The system uses tools to obtain information or perform actions.

## Thought–Action–Observation loop

The `Thought–Action–Observation loop` is a pattern used to explain how an AI agent solves a problem through repeated decisions and tool interactions. It is commonly `associated with the ReAct (Reasoning and Acting) approach`.

## Three main steps

1. Thought: The LLM decides what information it needs or what to do next.
2. Action: The agent requests a tool, and the application executes it.
3. Observation: The tool's result is returned to the LLM so it can decide the next step.
 
## How does the loop end?

The loop repeats until the LLM determines that it has enough information to provide a final answer, or a configured stopping limit is reached.

--------

# Create First AI Agent 

**Full Code file path** = Langchain_Code\6-agents\1_ai_agents.py

## Method - create_react_agent

Creates a `classic text-based ReAct agent` that follows the `Thought → Action → Action → Input → Observation` format to decide which tool to use and when to return the final answer.

## Method - create_tool_calling_agent

Creates an agent that uses the chat model's `native tool-calling capability` to request tools through structured tool calls, rather than generating the classic text-based ReAct format.

## Public Prompt hwchase17/react

`hwchase17/react` this is a publicly shared, classic ReAct prompt template available through LangChain Hub. It defines the instructions and format for tool usage, including Thought, Action, Action Input, Observation, and Final Answer.

**How to load this public prompt?**

```py
from langsmith import Client
prompt = Client().pull_prompt(
    "hwchase17/react",
    dangerously_pull_public_prompt=True,
)
```

**Below older way is deprecated now.**

```py
from langchain_classic import hub
prompt = hub.pull("hwchase17/react")

hub.pull is deprecated. Call the LangSmith client directly, which is the function that actually accepts dangerously_pull_public_prompt flag.
```

## Full Code example 

```py
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langsmith import Client    

serch_tool = DuckDuckGoSearchRun()

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
```

### verbose = True

Displays execution logs while the agent runs.

### return_intermediate_steps = True

Returns the agent's tool actions and observations as part of the result dictionary.	result["intermediate_steps"]

-------------

# hwchase17/react prompt

The hwchase17/react prompt contains `instructions` that tell the LLM how to interact with tools using the `ReAct` pattern. Here is the template retrieved from LangChain Hub.

```
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
```