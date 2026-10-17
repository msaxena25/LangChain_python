# Python f-string vs Langchain PromptTemplate

In LangChain, both f-strings and `PromptTemplate` let you insert dynamic values into text. The main difference is that `PromptTemplate` provides additional features useful for building LLM applications.

## 1. f-string vs PromptTemplate

### Using a Python f-string

```py
topic = "Angular"
level = "beginner"

prompt = f"Explain {topic} for a {level} developer."

print(prompt)
# Output: Explain Angular for a beginner developer.
```

### Using LangChain `PromptTemplate`

```py
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Explain {topic} for a {level} developer."
)

result = prompt_template.format(
    topic="Angular",
    level="beginner"
)

print(result)
# Output: Explain Angular for a beginner developer.
```

Both produce the same text. So, why use `PromptTemplate`?

## 2. Key benefits of PromptTemplate

| Benefit                                | f-string               | PromptTemplate               |
| -------------------------------------- | ---------------------- | ---------------------------- |
| Insert dynamic values                  | Yes                    | Yes                          |
| Reusable template                      | Possible, but manual   | Built in                     |
| Automatically identify input variables | No                     | Yes                          |
| Validate expected variables            | No built-in validation | Supports template validation |
| Set default values                     | Manual                 | Supports `partial_variables` |
| Connect directly to LangChain chains   | No, not by itself      | Yes                          |
| Compose with models using LCEL (`\\|`) | No, not by itself      | Yes                          |

## 3. Important benefits with examples

A. Reusability

Define the template once and use it for different topics.

```py
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} in simple language."
)

print(template.format(topic="Angular"))
# Output: Explain Angular in simple language.

print(template.format(topic="RAG"))
# Output: Explain RAG in simple language.
```

Note: Reusability is not an exclusive benefit of PromptTemplate. Python f-strings can also be reusable if you store the template in a variable or function. You can see that in file Tutorials\Python\3-class-python.md

B. Identify required variables

```py
template = PromptTemplate.from_template(
    "Explain {topic} for a {level} developer."
)

print(template.input_variables)
# Output: ['level', 'topic']
```

LangChain identifies which values the template expects.

C. Set default values with partial_variables prop

```py
template = PromptTemplate(
    template="Explain {topic} for a {level} developer.",
    input_variables=["topic"],
    partial_variables={"level": "beginner"}
)

print(template.format(topic="Angular"))
# Output: Explain Angular for a beginner developer.
```

You no longer need to supply `level` every time.

D. Integrate with an LLM

This is one of the most important advantages.

```py
chain = template | model

response = chain.invoke({
    "topic": "Angular",
    "level": "beginner"
})
```

The prompt template and model become a connected pipeline using LangChain Expression Language (LCEL).

-----

# Diff between `PromptTemplate()` and `PromptTemplate.from_template()`

The main difference is: `PromptTemplate()` lets you configure the template explicitly, while `PromptTemplate.from_template()` creates a template directly from a string and automatically detects its variables.

## 1. Using `PromptTemplate()`

You explicitly provide the template and its input variables.

```py
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Explain {topic} for a {level} developer.",
    input_variables=["topic", "level"]
)

result = prompt.format(topic="Angular", level="beginner")
print(result)

# Output:
# Explain Angular for a beginner developer.
```

## 2. Using `PromptTemplate.from_template()`

LangChain automatically identifies the variables inside `{}`.

```py
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} for a {level} developer."
).partial(level="beginner")

result = prompt.format(topic="Angular")

print(result)
# Output: Explain Angular for a beginner developer.
```

## 3. Key differences

| Feature                           | `PromptTemplate()`     | `from_template()`                |
| --------------------------------- | ---------------------- | -------------------------------- |
| Template string                   | Required               | Required                         |
| Define `input_variables` manually | Typically yes          | No, inferred automatically       |
| Control configuration explicitly  | Yes                    | Yes, through supported arguments |
| Best for                          | Explicit configuration | Quick, convenient creation       |

Remember: `from_template()` is a class method that creates and returns a `PromptTemplate` object. Both approaches produce the same type of object and can be used in LangChain chains.

---

# Seperate File for Prompttemplate and load 

LangChain provides a `save()` method to save a `PromptTemplate` to a separate file. You can then load it later instead of defining the prompt again.

One important detail: `prompt.save()` expects a file path string, and LangChain's prompt serialization typically uses a `.json` file.

## 1. Save the prompt — `save_prompt.py`

```py
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} for a {level} developer."
)

prompt.save("template.json")
```

This saves the prompt configuration to `template.json`.

## 2. Load it later — `main.py`

### load_prompt method older way (deprecated now)

```py
from langchain_core.prompts import load_prompt
prompt = load_prompt("template.json")
```

However, according to the current LangChain documentation, `load_prompt()` is deprecated in `langchain-core` 1.2.21 and scheduled for removal in version 2.0.0.&#x20;

### dumps and loads method

For modern LangChain, serialize and deserialize the prompt using `dumps()` and `loads()`:

```py
from pathlib import Path
from langchain_core.load import dumps, loads

# Save the prompt
Path("template.json").write_text(dumps(prompt), encoding="utf-8")

# Load the prompt
loaded_prompt = loads(
    Path("template.json").read_text(encoding="utf-8")
)

print(loaded_prompt.format(topic="Angular", level="beginner"))
# Output: Explain Angular for a beginner developer.
```

Key takeaway: `prompt.save("template.json")` is valid in older/current compatible versions, but it's deprecated in newer LangChain releases. For new code, prefer `dumps()` and `loads()`.&#x20;

----------

# Messages

In LangChain, messages are used to structure conversations with an LLM. Let's create a simple Gemini chatbot using messages.

### 1. Types of messages

- `SystemMessage` — defines the chatbot's behavior.
- `HumanMessage` — represents the user's message.
- `AIMessage` — represents the model's response.

### 2. Chatbot code using messages

```py
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages = [
    SystemMessage(content="You are a helpful Python tutor."),
    HumanMessage(content="What is a Python variable?")
]

response = model.invoke(messages)

print(response.text)
```

### 3. How it works

1. `SystemMessage` sets the chatbot's behavior.
2. `HumanMessage` contains the user's question.
3. `model.invoke(messages)` sends the conversation to Gemini.
4. `response.text` returns only the generated text.

--------

## Before learning `ChatPromptTemplate`, let's connect it with what you have already learned.

### 1. What we have learned so far

A. Single text prompt — `PromptTemplate`

You create one text prompt with dynamic variables.

B. List of messages — `SystemMessage`, `HumanMessage`, `AIMessage`

You create a list of messages with different roles.

Here, the messages are static because their content is written directly in the code.

### 2. What if we want dynamic messages in Category B?

Suppose you want to build a reusable chatbot where:

- The system instruction changes depending on the subject.
- The user's question changes every time.
- The user's experience level also changes.

You could manually create each message using Python variables, but that becomes less convenient when prompts grow or need to be reused.

This is where `ChatPromptTemplate` comes in.

It combines the two concepts you have already learned:

- Chat messages: `SystemMessage`, `HumanMessage`, and `AIMessage`.
- Dynamic variables: placeholders such as `{subject}`, `{topic}`, and `{level}`.

-----

# ChatPromptTemplate

### Dynamic System message 

SystemMessage(content= "You have good knowledge in {domain}. Lets drive that.");

HumenMessage(content="Explain topic {topic}")

### ChatPromptTemplate example

```py
from langchain_core.prompts import ChatPromptTemplate

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {subject} tutor."),
    ("human", "Explain {topic} for a {level} developer.")
])

'''
OR 

chat_template = ChatPromptTemplate([
  ("system", "You are a helpful {subject} tutor."),
    ("human", "Explain {topic} for a {level} developer.")
])

OR

chat_template = ChatPromptTemplate([
   SystemMessage(content= "You have good knowledge in {domain}. Lets drive that."),
   HumenMessage(content="Explain topic {topic}")
])
'''

messages = chat_template.invoke({
    "subject": "Python",
    "topic": "variables",
    "level": "beginner"
})

print(messages)
```

Here, `ChatPromptTemplate` replaces the dynamic variables and generates a list of messages containing a `SystemMessage` and a `HumanMessage`.

To send those messages to Gemini:

```
response = model.invoke(messages)
print(response.text)
```

Key difference:

- `PromptTemplate` — creates a dynamic text prompt.
- `ChatPromptTemplate` — creates a dynamic list of chat messages, including system, human, and AI messages.

----

| `PromptTemplate`                    | `ChatPromptTemplate`                                                       |
| ----------------------------------- | -------------------------------------------------------------------------- |
| Creates a single text prompt.       | Creates a list of chat messages.                                           |
| Uses placeholders like `{topic}`.   | Uses placeholders in messages with roles like `system`, `human`, and `ai`. |
| Best for simple text-based prompts. | Best for chatbots and role-based conversations.                            |
| Example: `"Explain {topic}"`        | Example: `("human", "Explain {topic}")`                                    |

When to use which?

- `PromptTemplate` — when you need a simple, single text prompt to send to an LLM.
- `ChatPromptTemplate` — when you need structured messages, different roles, system instructions, or conversational prompts for a chat model like Gemini.

Both support dynamic variables. The main difference is the output structure: text versus chat messages.

----

# MessagePlaceholder in LangChain

`MessagesPlaceholder` lets you insert a dynamic list of messages or chat history into a `ChatPromptTemplate`.

Instead of hardcoding every conversation message, you pass the messages at runtime.

### 1. Example

```py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

messages = chat_template.invoke({
    "history": [
        HumanMessage(content="My name is Mohit."),
        AIMessage(content="Hello Mohit!"),
    ],
    "question": "What is my name?"
})

print(messages)
```

Here, `MessagesPlaceholder(variable_name="history")` inserts the messages provided through the `history` variable into the template.

### 2. Common use cases

- Chatbot memory: Include previous user and AI messages so the model can use conversation context.
- Conversation history: Pass a changing list of messages without rebuilding the template.
- Agent workflows: Insert messages from previous steps or tool interactions.

Important: `MessagesPlaceholder` does not store conversation history itself. Your application must maintain the history and pass it into the template.

**`MessagesPlaceholder` is designed to work with `ChatPromptTemplate`, not `PromptTemplate`.**

----

# Structured Output in LangChain

Structured output means asking the LLM to return data in a predefined format, such as a Python dictionary or JSON, instead of free-form text.


## 1. Example without structured output

```py
response = model.invoke("Tell me about Python.")

print(response.text)
# Output: Python is a popular programming language...
```

The response is plain text, so extracting specific fields can be difficult.

## Four ways to create this structured output 

1. TypedDict — defines the expected structure using Python type hints, without Pydantic validation.
2. pydantic - Is a data validation an data parsing library, defines the expected structure using Python type hints and ensures that data is correct, type safe, and structured.
3. JSON Schema — defines the output structure using a JSON schema dictionary.
4. Raw JSON / dictionary — ask the model for JSON and parse it yourself, though this is less reliable.


## Example with structured output using Gemini - pydantic

```py
from pydantic import BaseModel, Field

class Language(BaseModel):
    name: str = Field(description="Programming language name")
    year: int = Field(description="Year it was created")
    creator: str = Field(description="Creator's name")

structured_model = model.with_structured_output(Language)

response = structured_model.invoke(
    "Tell me about Python programming language."
)

print(response)
print(response.name)
print(response.year)
print(response.creator)
```

Example output (values may vary):

```
# name = "Python"
# year = 1991
# creator = "Guido van Rossum"
```

### 3. How it works

1. `BaseModel` defines the expected data structure.
2. `Field` describes each field.
3. `with_structured_output(Language)` configures the model to return data matching the schema.
4. `invoke()` returns a validated Pydantic object, so you can access fields using dot notation.

### 4. When to use structured output

- Extracting information from text.
- Building APIs that need predictable response fields.
- Classifying customer queries into categories.
- Returning structured data for applications and databases.

Remember: `response.text` is for text responses. With this example, `response` is a Pydantic object, so use `response.name`, `response.year`, or `response.model_dump()` to access the data.

Example using `TypedDict`:

```py
from typing_extensions import TypedDict

class Language(TypedDict):
    name: str
    year: int
    creator: str

structured_model = model.with_structured_output(Language)

response = structured_model.invoke(
    "Tell me about Python programming language."
)

print(response["name"])
print(response["year"])
print(response["creator"])
```

Which should you use?

- `Pydantic` — when you need validation and type constraints.
- `TypedDict` — when you need a simple typed structure.
- `JSON Schema` — when you want to define the schema directly as JSON.
- Manual JSON parsing — when you want to handle parsing yourself.

For most applications, Pydantic is a good default when validation matters; `TypedDict` is a lightweight alternative.

-----

# Annotated in TypedDist

`Annotated` lets you attach extra information or metadata to a Python type without changing the type itself.

In LangChain, it can be used with `TypedDict` to describe what a field means.

```py
from typing import Annotated
from typing_extensions import TypedDict

class Language(TypedDict):
    name: Annotated[str, "Programming language name"]
    year: Annotated[int, "Year it was created"]

- `str` and `int` define the field types.
- `"Programming language name"` and `"Year it was created"` are metadata descriptions.

# another example -

class Review(TypedDict):
    summary: Annotated[str, "A breif summary of the review"]
    year: Annotated[int, "Year it was created"]
```

Important: `Annotated` itself does not validate data. It attaches metadata that tools such as LangChain can use when defining structured output schemas.

----

# LangChain: Output Parsers in Python

An Output Parser converts the response generated by an LLM (Large Language Model) into a structured format that your Python application can understand and use.

By default, an LLM may return plain text. But your application might need a Python dictionary, a list of products, a validated object, or a specific data type.

### Why do we need output parsers?

- Convert LLM text into usable Python data.
- Extract lists, numbers, or structured fields.
- Enforce an expected output format.
- Connect LLM responses to APIs, databases, and application logic.

For example, an e-commerce application can use an LLM to extract product details from a customer's message and then pass those details to a Python function.

A typical chain looks like this:

```py
prompt | model | output_parser
```

## 3. Types of output parsers in LangChain

**Below four are most used parser with langhchain.**

- StrOutputParser
- JsonOutputParser
- PydanticOutputParser
- StructuredOutputParser

**Below are less used parsers -**

- CommaSeparatedListOutputParser
- ListOutputParser
- NumberedListOutputParser
- EnumOutputParser
- BooleanOutputParser
- DatetimeOutputParser
- XMLOutputParser
- OutputFixingParser
- RetryOutputParser

## StrOutputParser — plain text

Purpose: Convert a model's response into a regular Python string.

```py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in two sentences."
)

model = ChatOpenAI(model="gpt-4.1-mini")

# embed parser in chain.
chain = prompt | model | StrOutputParser()

result = chain.invoke({"topic": "Python decorators"})

print(result)
```
Without StrOutputParser, a chat model normally returns an AIMessage object. With it, you get the message's text content as a string.

## JsonOutputParser

`JsonOutputParser.get_format_instructions()` provides instructions that you can include in your prompt so the LLM knows to return JSON. 

### Example 1: Without a schema

```py
from langchain_core.output_parsers import JsonOutputParser
parser = JsonOutputParser()
format_instructions = parser.get_format_instructions()
print(format_instructions)
```

The instructions tell the LLM to return a JSON value without extra explanatory text or Markdown formatting.

### Example 2: Use it in a chain

```py
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
Extract the product details from this text.

Text: {text}

{format_instructions}
""",
    input_variables=["text"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
)

model = ChatOpenAI(model="gpt-4.1-mini")

chain = prompt | model | parser

result = chain.invoke({
    "text": "Laptop costs 75000 rupees and is in stock."
})

print(result)
print(type(result))
```

Expected output:

```
{    "name": "Laptop",    "price": 75000,    "in_stock": True}
```

The exact fields depend on the instructions you give the LLM.

Important: Without a schema, `get_format_instructions()` does not define the `name`, `price`, or `in_stock` fields. It only requests JSON output.

### Example 3: Provide a Pydantic schema

```py
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    in_stock: bool

parser = JsonOutputParser(pydantic_object=Product)

print(parser.get_format_instructions())
```

Now the format instructions include a JSON schema describing the product fields.

Key distinction: `JsonOutputParser(pydantic_object=Product)` uses the Pydantic schema to guide the LLM's output format, but it does not validate the parsed result against all Pydantic constraints. Use `PydanticOutputParser` or `model.with_structured_output(Product)` when you need schema validation.

---


## StructuredOutputParser — schema-described JSON

This parser appears frequently in older LangChain tutorials. It uses `ResponseSchema` definitions to describe the expected fields and parses the response into a dictionary.

Note - StructuredOutputParser is in langchain main package not in langchain_core package. langchain_core is primary for very core feature of langchain that are mostly used.

```py
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

response_schemas = [
    ResponseSchema( name="name", description="Product name"),
    ResponseSchema(name="price", description="Product price"),
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

template = PromptTemplate() # give ur template

chain = template | model | parser

result = chain.invoke()

print(result)
```

For new applications, Pydantic-based structured output is generally a better choice when field types and validation matter.

---

## PydanticOutputParser — structured and validated data

Purpose: Parse an LLM response into a Pydantic model, validating the fields against a defined schema.

This is especially useful when your Python application depends on specific field types and constraints.

Benefits - 

- Strict schema enforcement
- Type safety
- Easy validation
- Seamless integration

```py
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Name of person"),
    age: int = Field(gt=18),
    city: str = Field(description="name of city")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template:  "Generate name, city and age of fictional {place} person \n
    {format_instruction}",
    input_variables=['place'],
    partial_variables={'format_instruction' : parser.get_format_instructions()}
)

chain = template | model | parser

chain.invoke({'place': 'indian'})

```

`pydanticParser.get_format_instructions()` 

- generates instructions describing the expected output format for the LLM.
- describes the expected JSON structure, defined in schema.
- Pass this in the template's {format_instruction} variable and that is automatically populated.

----