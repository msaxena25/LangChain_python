# What is an AI agent?

An AI agent is an `LLM-powered system` that can decide what action to take, use tools, observe the results, and continue taking actions until it reaches a goal or decides to stop.

# Thought–Action–Observation loop

The `Thought–Action–Observation loop` is a pattern used to explain how an AI agent solves a problem through repeated decisions and tool interactions. It is commonly `associated with the ReAct (Reasoning and Acting) approach`.

## Three main steps

1. Thought: The LLM decides what information it needs or what to do next.
2. Action: The agent requests a tool, and the application executes it.
3. Observation: The tool's result is returned to the LLM so it can decide the next step.
 
## How does the loop end?

The loop repeats until the LLM determines that it has enough information to provide a final answer, or a configured stopping limit is reached.

------

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

## Is this the ReAct design pattern?

Yes. The cycle you described follows the `ReAct (Reasoning and Acting)` pattern.

**ReAct combines two capabilities:**

- `Reasoning`: The LLM decides what information it needs and what to do next.
- `Acting`: The system uses tools to obtain information or perform actions.

--------