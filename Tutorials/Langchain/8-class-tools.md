# What is a Tool?

A tool is just a Python function (or API) that is packaged in a way the LLM can understand and call when needed.

An LLM is good at understanding questions and generating text, but it cannot independently execute Python code, query your database, access an API, or search the live web unless it has a mechanism to do so.

Tools provide those capabilities.

**Example:**

User asks: "What is the current USD-to-INR rate?" → The agent can use a currency or API tool.

## How Tools fits into the Agent ecosystem

An Al agent is an LLM-powered system that can autonomously think, decide, and take actions using external tools or APIs to achieve a goal.
```
┌────────────────────────────────────────────┐
│                  Agent                     │
│ ─────────────────────────────────────────  │
│      Reasoning & Decision Making           │
│                                            │
│  ┌────────────┐         ┌──────────────┐   │
│  │   LLM      │ <─────> │    Tools     │   │
│  └────────────┘         └──────────────┘   │
│   (Thinks, plans)      (Acts, executes)    │
└────────────────────────────────────────────┘
```

# Types of tools

There are two useful categories to start with.

## A. Built-in / prebuilt tools

Tools or integrations that already exist in a library or ecosystem.

Examples: web search integrations, Wikipedia search, calculator, database integrations.

## B. Custom tools

Functions you create for your application's specific requirements, then expose to the agent as tools.

Examples: `get_employee_leave_balance()`, `search_internal_policies()`, or `get_order_status()`.

**One important distinction:** in LangChain, many tools come from `separate integration packages` rather than the core library itself. Also, a Python function is not automatically an agent tool; it needs to be exposed or registered in a way the agent can call.
vant documents; you can wrap that retriever in a tool so an agent can decide when to use it.

## Widely used tools in the LangChain ecosystem

| Tool / integration                             | What it does                                                                                                                                   |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Web search — Tavily, DuckDuckGo, Google Search | Searches the web for relevant information. Useful for current events, recent facts, and information outside the LLM's knowledge.               |
| Wikipedia                                      | Searches Wikipedia for general knowledge about people, places, historical events, and other topics.                                            |
| Python REPL                                    | Executes Python code dynamically. Useful for calculations, data processing, and tasks requiring code execution.                                |
| Calculator / Wolfram Alpha                     | Performs mathematical calculations or answers computational and scientific questions. Availability depends on the integration used.            |
| Web page fetching — Requests or browser tools  | Fetches web page content or interacts with websites, depending on the tool. Useful for reading specific pages or automating browser workflows. |
| SQL database tools                             | Inspect database schemas and execute queries to retrieve structured information. Write operations should be restricted appropriately.          |
| Vector store / retriever tools                 | Search your embedded documents for relevant chunks. Useful for company-document assistants and RAG-based agents.                               |
| File system tools                              | Read, search, create, or edit files, depending on the implementation and permissions.                                                          |
| GitHub tools                                   | Access repository files, issues, and pull requests, depending on the integration's supported operations.                                       |
| API / HTTP tools                               | Call external APIs to retrieve data or perform actions in other systems. Often used to build custom integrations.                              |

For the current Python integration catalogue, see the [official LangChain integrations reference](https://reference.langchain.com/python/integrations/overview?utm_source=chatgpt.com).

-----

#  DuckDuckGo search tool in Python

## 1. Install the required packages

Run this in your existing Python virtual environment:

```
pip install -U langchain-community ddgs
```

- `langchain-community` provides LangChain's community integrations.
- `ddgs` provides the DuckDuckGo search functionality.

## 2. Create the search tool

```py
from langchain_community.tools import DuckDuckGoSearchRun

search_tool = DuckDuckGoSearchRun()

result = search_tool.invoke("Latest developments in LangChain")

print(result)
```

This is the simplest implementation. No LLM API key is required just to invoke this search tool, although internet access and the search service must be available.

## Steps 

1. Your Python code passes "Today's news in Delhi" to DuckDuckGoSearchRun.
2. The DuckDuckGoSearchRun tool accepts the input and passes it to the underlying `DuckDuckGo search integration`.
3. The underlying ddgs library communicates with its configured search backend to perform the search. It does not need an LLM to do this.
4. DuckDuckGo searches for relevant web pages and returns available results, which may include titles, snippets, and URLs.
5. The integration collects the results and returns them to LangChain.

------

# Google Search tool

LangChain provides a `Google Search tool`, similar to the DuckDuckGo search tool we just implemented. The main difference is that the standard Google Search integration uses Google's Custom Search API and requires credentials.

## 1. Install the package

```
pip install -U langchain-google-community
```

## 2. Configure Google Search

You need two values in env files. These are used by the Google Custom Search integration.

- `GOOGLE_API_KEY` — your Google API key.
- `GOOGLE_CSE_ID` —  Google Custom Search Engine ID

Note - Sign in with your Google account. Create a new search engine if you don't have one, or select an existing engine.

## 3. Implement the search tool

```py
from langchain_google_community import GoogleSearchRun
from langchain_google_community import GoogleSearchAPIWrapper

search = GoogleSearchAPIWrapper()

search_tool = GoogleSearchRun(api_wrapper=search)

result = search_tool.invoke("Today's news in Delhi")

print(result)
```
-------

# LangChain: Custom Tools

A custom tool is a function that you create to give an AI system a capability specific to your application.

get_order_status() — retrieves an e-commerce order's status.

## create custom tools

There are `three` main approaches commonly taught for creating custom tool.

**Method 1: @tool decorator**

Write a normal Python function and decorate it with @tool. LangChain infers its name, description, and input schema from the function and its type hints.

**Method 2: StructuredTool.from_function()**

Converts a regular Python function into a `structured` LangChain tool using a factory method. You can explicitly configure the tool's name, description, input schema, and other options.

**Method 3: Subclass BaseTool**

Create a Python class that inherits from LangChain's BaseTool and implement its execution logic, typically through _run().

## Create tools with @tool

```py

from langchain_core.tools import tool

@tool
def create_fabanaccri_series(n: int) -> list[int]:
    '''This tool returns a Fibonacci series up to n'''
    a, b = 0, 1
    result = [0]
    for _ in range(n):
        a, b = b, a + b
        result.append(a)
    return result

'''
- @tool decorator is used to convert a Python function into a LangChain tool.
- type hints are used to specify the type of the input and output of the function.
- function description is used to describe the function.
'''

result = create_fabanaccri_series.invoke({"n": 7})
print(result) # [0, 1, 1, 2, 3, 5, 8, 13]
```

In LangChain, a tool created using `@tool` has three important properties:

1. `name` — The tool's name, which the LLM uses to identify the tool it wants to call.
2. `description` — Explains what the tool does and when it should be used. The LLM uses this information to decide whether the tool is appropriate.
3. `args` — Describes the tool's input arguments, including their names, types, and schema.

```py
print(create_fabanaccri_series.name)
print(create_fabanaccri_series.description)
print(create_fabanaccri_series.args)

create_fabanaccri_series
This tool returns a Fibonacci series up to n
{'n': {'title': 'N', 'type': 'integer'}}
```
-----

## What LLM actually recieves from these tools?

The LLM receives the tool's definition (name, description, and input schema), not the Python function's source code. The framework sends the tool definition in the format supported by the selected model/provider.

You can print the tool's schema directly using `multiply.args_schema.model_json_schema()`.

```py
{
 'description': 'This tool returns a Fibonacci series up to n',
 'properties': {'n': {'title': 'N', 'type': 'integer'}}, 
 'required': ['n'],
 'title': 'create_fabanaccri_series', 
 'type': 'object'
 }
 ```

 ---------

 # Method 2: StructuredTool.from_function() with Pydantic Model

 A LangChain method used to convert a Python function into a structured tool, where a Pydantic model defines the input parameters, data types, default values, and validation rules.

 When to use: When a tool accepts multiple named arguments and requires structured input validation.

 ```py
 # Lets Create a Income TAX Calculator tool

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

# Ceate Pydantic Model for the tool
class IncomeTaxCalculatorSchema(BaseModel):
    salary: float = Field(description="The salary of the employee", required=True, ge=0)
    slab1_rate: float = Field(description="The tax rate for the first slab", ge=0, le=1, default=0.10) # 10%
    slab2_rate: float = Field(description="The tax rate for the second slab", ge=0, le=1, default=0.20) # 20%
    slab3_rate: float = Field(description="The tax rate for the third slab", ge=0, le=1, default=0.30) # 30%

# Define the business logic
def income_tax_calculator(salary: float, slab1_rate: float, slab2_rate: float, slab3_rate: float) -> float:
    '''This tool calculates the progressive income tax for the given salary based on the given slab rates'''
    tax_amount = 0

    if salary > 500000:
        tax_amount += min(salary - 500000, 500000) * slab1_rate
    if salary > 1000000:
        tax_amount += min(salary - 1000000, 1000000) * slab2_rate
    if salary > 2000000:
        tax_amount += (salary - 2000000) * slab3_rate

    return tax_amount
    
# Convert the function into a LangChain tool
income_tax_calculator_tool: StructuredTool = StructuredTool.from_function(
    func=income_tax_calculator,
    name="income_tax_calculator",
    description=(
        "This tool calculates the progressive income tax for the given salary based on the given slab rates"
        "If salary <= 5 lakhs no tax"
        "if salary 5 to 10 lakhs = 10%"
        "if salary 10 to 20 lakhs = 20%"
        "if salary > 20 lakhs = 30%"
        "Return the tax amount"
        "Note - This tax percentages must be configurable by the user with its default values."
    ),
    args_schema=IncomeTaxCalculatorSchema
)

result = income_tax_calculator_tool.invoke({"salary": 1100000})
print('Tax amount for salary 11 lakhs is:', result) # 70000.0

print('name', income_tax_calculator_tool.name)
print('description', income_tax_calculator_tool.description)

# print LLM schema
print('LLM will receive the following schema:')
print(income_tax_calculator_tool.args_schema.model_json_schema())

```

**Remember:** `args_schema.model_json_schema()` alone is not the complete tool definition. Your overall description is still available through `income_tax_calculator_tool.description` and is included when LangChain formats the tool for the model.

------------

### 3. `BaseTool` (Custom Tool by Subclassing)

An advanced way to create a custom LangChain tool by defining a class that inherits from `BaseTool` and implementing its required methods and properties.

**Key points:**

- `name`: Defines the tool's name.
- `description`: Explains the tool's purpose to the LLM.
- `args_schema`: Optionally defines and validates structured inputs using a Pydantic model.
- `_run()`: Implements the tool's synchronous execution logic.
- `_arun()`: Can implement asynchronous execution logic when needed.

When to use: When you need greater control over a tool's execution, input validation, or synchronous and asynchronous behavior.

Note: For simple tools, `@tool` or `StructuredTool.from_function()` is usually easier. Subclassing `BaseTool` is useful for more complex custom tools.

```py

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

# create schema
class GradeToolSchema(BaseModel):
    obtained_marks: float = Field(description='optained marks in the exam', ge=0, required=True)
    total_exam_marks: int = Field(description='total exam marks', default=500, gt=0)
    
class GradeTool(BaseTool):
    name: str = 'Grade Calculator'
    description: str = '''
    Create a tool to get a Grade in exams 
    If total obtained number >= 75% then grade A+
    If number >= 60% then grade A
    If number >= 50% then grade B
    If number >= 35% then grade C
    Below 35% = Fail
    '''
    args_schema: Type[BaseModel] = GradeToolSchema
    
    def _run(self, obtained_marks: float, total_exam_marks: int  = 500) -> dict:
        grade = ''
        percentage = (obtained_marks / total_exam_marks) * 100
        if percentage >= 75:
            grade = 'A+'
        elif percentage >= 60:
            grade = 'A'
        elif percentage >= 50:
            grade = 'B'
        elif percentage >= 35:
            grade = 'C'
        else:
            grade = 'Fail'
        return { 'percentage': percentage, 'grade': grade }
        #return f"Percentage: {percentage:.2f}%, Grade: {grade}"

                    
grade_tool_obj = GradeTool()

print(grade_tool_obj.name) # Grade Calculator

result = grade_tool_obj.invoke({'obtained_marks': 100})
print(result) # {'percentage': 20.0, 'grade': 'Fail'}

result = grade_tool_obj.invoke({'obtained_marks': 300})
print(result) # {'percentage': 60.0, 'grade': 'A'}
```

# What is a Toolkit in LangChain?

A toolkit is a `collection of related tools` grouped together so an agent can use them to perform a particular type of task.

## Built-in or integration-provided toolkits

1. SQL Database Toolkit	Query databases, inspect tables and understand database schemas.
2. GitHub Toolkit	Interact with GitHub repositories and work with code or issues.
3. Playwright Browser Toolkit	Navigate websites, click elements and extract webpage content.
4. File Management Toolkit	Perform file operations such as listing, reading, writing and copying files.
5. Gmail Toolkit	Work with email, such as searching messages and managing email-related actions.
6. Slack Toolkit	Integrate agents with Slack for messaging and workspace tasks.
7. Jira Toolkit	Work with Jira issues and project-management tasks.
8. Office 365 Toolkit	Integrate with supported Office 365 services.

## Lets Create another tool - Scholarship Calculator tool

- When grade A+, student is eligible for 50k scholarship.
- When grade A, then 30K
- No scholorship below grade A.

```py
from langchain_core.tools import tool

@tool
def scholarship_calculator_tool(grade: str) -> dict:
    '''Calculate scholarship eligibility and amount based on the student's grade.'''
    scholarship = {}
    if (grade == 'A+'):
        scholarship = {'eligible': True, 'scholarship_amount': 50000}
    elif (grade == 'A'):
        scholarship = {'eligible': True, 'scholarship_amount': 30000}
    else:
        scholarship = {'eligible': False, 'scholarship_amount': 0}
    return scholarship
    
result =  scholarship_calculator_tool.invoke({'grade': 'A'})
print('scholarship ', result)  
# {'eligible': True, 'scholarship_amount': 30000}
```

## Create Toolkit

**We'll combine existing Grade Calculator Tool with a new Scholarship Calculator Tool using a LangChain toolkit.**

The workflow will be:

1. The grade tool calculates the student's percentage and grade.
2. The scholarship tool checks the grade and returns the eligible scholarship amount.
3. The toolkit groups both tools together so they can be provided to an agent.

LangChain provides `BaseToolkit` for creating a custom toolkit. Its `get_tools() method` returns the collection of tools.

```py
from langchain_core.tools import BaseToolkit

class StudentToolkit(BaseToolkit):
    '''Toolkit for student grading and scholarship calculations.'''
    
    def get_tools(self) -> list[BaseTool]:
        return [grade_tool_obj, scholarship_calculator_tool]
    

# Now get all tools from toolkit
student_toolkit = StudentToolkit()

tools = student_toolkit.get_tools()
for tool in student_toolkit.get_tools():
    print(tool.name)
    
# Grade Calculator
# scholarship_calculator_tool
```
**Notes -**

- If we create tools using class (Method 2 & 3) then we pass object of that class into get_tools method.
- If we create tools using @tool decorator, we can pass that tool function into get_tools method.
- The toolkit groups the tools, but it does not automatically execute them in sequence.

## How to use that toolkit?

```py
tools = student_toolkit.get_tools()

grade = tools[0].invoke({'obtained_marks': 350})
scholorship = tools[1].invoke({'grade': grade.get('grade')})
print(scholorship)
```

-----------

#  Tool Binding in LangChain

Tool binding is the process of `connecting tools to LLMs (chat model)` so the model knows which tools are available, what each tool does, and what input arguments it accepts.

Tool binding does not itself execute the tool. Tool binding makes tools available to the LLM so it can `request their execution` when appropriate.

## How do we bind tools?

The standard method is `.bind_tools()` on LLMs that supports tool calling.

For your student example:

```py
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="your-supported-model")

tools = student_toolkit.get_tools() # get all tools from Student Toolkit
model_with_tools = model.bind_tools(tools)
```

Here, `model_with_tools` is the model with both student tools bound to it.

# Tool Calling in LangChain

Tool calling is the process in which an LLM decides that a tool is needed, generates a structured request containing the tool's name and input arguments, and asks the application to execute it.

Tool calling is when the model requests a particular tool with specific arguments.

## Implement tool calling

### Step 1: Bind the tool to the model

```py
model_with_tools = model.bind_tools(tools)
```

### Step 2: Ask a question

```py
response = model_with_tools.invoke(
    "Use the grade calculator to calculate the grade for 300 marks."
)
print(response.tool_calls)
```

**If the model analized that for this query, any tool is required, the response will contain that tool call similar to this.**

```py
[
    {
        "name": "grade_calculator",
        "args": {
            "obtained_marks": 300,
            "total_exam_marks": 500
        },
        "id": "call_123"
    }
]
```

--------

# Tools Execution 

Tool execution is the process of `running the selected tool` with the `arguments provided by the LLM `and returning the tool's result.

Tool execution performs the actual operation; the LLM can then use the result to formulate its final response.

Use `.invoke()` to execute a tool by passing its required input arguments.

```py
# Execute the existing grade tool
result = grade_tool.invoke({
    "obtained_marks": 400,
    "total_exam_marks": 500
})

print(result)
```

-----

# InjectedToolArg

InjectedToolArg in LangChain marks a tool argument that should be supplied or injected by your application, not generated by the LLM.

```py
from typing import Annotated
from langchain_core.tools import tool, InjectedToolArg

@tool
def get_refund_status(refund_id: Annotated[str, InjectedToolArg]) -> str:
```