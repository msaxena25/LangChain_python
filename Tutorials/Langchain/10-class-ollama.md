# What is Ollama?

Ollama is a `tool` that lets you `download and run AI models` `locally` on your own computer, instead of sending every prompt to a cloud-based API such as Gemini or OpenAI.

For example, you can run models such as Llama, Gemma, or Qwen on your computer and interact with them through a command line, an API, or frameworks such as LangChain.

Ollama exposes a local API, usually at `http://localhost:11434`, which your application can call.

## Download

Install Ollama from the official website: [Download Ollama](https://ollama.com/download?utm_source=chatgpt.com).

**You can also download (4 gb) and install with command from powershell -** (I did this) 

```
> irm https://ollama.com/install.ps1 | iex
```

**irm: Invoke-RestMethod**: Downloads the content from a URL. Here, it retrieves Ollama's PowerShell installation script.

**| — Pipe operator:** Passes the downloaded script content to the next command.

**iex: Invoke-Expression**: Executes the PowerShell code it receives as input.

```
>>> Downloading Ollama for Windows...
######################################## 100.0%
>>> Installing Ollama...
>>> Install complete. Run 'ollama' from the command line.
PS C:\Windows\System32> ollama

 Welcome to Ollama!

> ollama --version (Check version)
```
----

## Install a Model

ollama run [model_name]

```py
> ollama run llama3.1:8b

# Locally downloaded models
> ollama list

NAME           ID              SIZE      MODIFIED
llama3.1:8b    46e0c10c039e    4.9 GB    51 minutes ago

# see the full model configuration
ollama show llama3.1:8b --modelfile

# You will also get in full configuration - 
Cutting Knowledge Date: December 2023
```

## See a model's default parameters

```py
# ollama show --parameters shows configured parameter values only, not all.
ollama show llama3.1:8b --parameters

# See model information
ollama show llama3.1:8b
```

| Parameter           | What it controls                                       | Example                            |
| ------------------- | ------------------------------------------------------ | ---------------------------------- |
| `temperature`       | Randomness/creativity                                  | `0.2` for more predictable answers |
| `num_predict`       | Maximum generated tokens                               | `200`                              |
| `num_ctx`           | Context window size                                    | `4096`                             |
| `top_k`             | Number of high-probability token candidates considered | `40`                               |
| `top_p`             | Probability-based token sampling                       | `0.9`                              |

**Set Parameters**

```
/set parameter temperature 0.3
/set parameter num_predict 200
/set parameter num_ctx 4096
```

These set the temperature, maximum generated tokens, and context-window size for the current session.

----

### Quick diff from Huggingface

**Hugging Face** = A platform where you can find and download AI models, Download datasets for machine learning,Experiment with a wide variety of pretrained models.

**Ollama** = A tool to run a chat model locally on your computer, and can Use a local model with LangChain.

------

# Several ways to Run Ollama

## 1. Method 1 — CLI

First, download a model:

```py
ollama pull llama3.2 # pull model
ollama run llama3.2 # run model

# after run, you can direct start chat into terminal.
```

## 2. Method 2 — Python library

Install the official Python package:

```py
pip install -U ollama
```

### A. `generate()` method

Use this when you want to provide a prompt and generate a response.

```py
import ollama
response = ollama.generate(
    model="llama3.2",
    prompt="Explain machine learning in simple words."
)
print(response["response"])
```

### B. `chat()` method

Use this when working with chat messages and conversation history.

```py
import ollama
response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ]
)
print(response.message.content)
```

The key difference is that `generate()` accepts a single prompt, while `chat()` accepts a list of role-based messages, such as `system`, `user`, and `assistant`

## 3. Method 3 — REST API

Ollama `runs a local HTTP server`, usually at `http://localhost:11434`. Your application sends an HTTP request, and Ollama returns the model's response.

### A. Generate API

Endpoint: `POST http://localhost:11434/api/generate`

```py
import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "llama3.2",
    "prompt": "Explain machine learning in simple words.",
    "stream": False #  return the completed response in one JSON object instead of streaming chunks
}
response = requests.post(url, json=payload) # POST method
print(response.json()["response"])
```

### B. Chat API

Endpoint: `POST http://localhost:11434/api/chat`

```PY
import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "llama3.2",
    "messages": [
        {
            "role": "user",
            "content": "What is machine learning?"
        }
    ],
    "stream": False
}
response = requests.post(url, json=payload)
print(response.json()["message"]["content"])
```

## 4. Method 4 — JavaScript / Node.js

You can use Ollama directly from a Node.js application.

Install the package:

```JS
npm install ollama
```

Example:

```js
import ollama from "ollama";

const response = await ollama.generate({
  model: "llama3.2",
  prompt: "Explain machine learning in simple words."
});

console.log(response.response);
```

## 5. Method 5 — LangChain integration

Install the integration:

```
pip install -U langchain-ollama
```

Use `ChatOllama` to connect a local Ollama model to LangChain:

```js
from langchain_ollama import ChatOllama
model = ChatOllama(
    model="llama3.2"
)
response = model.invoke(
    "Explain machine learning in simple words."
)
print(response.content)
```
------

# Important parameters of `ollama.generate()`

```PY
import ollama #python package

response = ollama.generate(
    model="llama3.2",
    prompt="Explain RAG in simple words.",
    system="You are a Python and AI tutor.", #  Instructions defining the model's role or behavior    
    stream=False,
    format="json" #  Request JSON or output matching a JSON schema  
    options={
        "temperature": 0.2, # Lower values generally produce more predictable responses
        "num_predict": 100 #  limits the number of tokens generated.
    },
    keep_alive="5m" # Control how long the model stays loaded in memory
    images = '' #  Supply images to compatible multimodal models        
)
print(response.response)
```
----

# Model interaction methods

These are the most important methods to learn first.

| Method              | Purpose                               |
| ------------------- | ------------------------------------- |
| `ollama.generate()` | Generate text from a prompt           |
| `ollama.chat()`     | Generate responses from chat messages |
| `ollama.embed()`    | Convert text into embedding vectors   |

# Model management methods

These methods help you manage models programmatically, without manually running every CLI command.

| Method            | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| `ollama.list()`   | List models available locally                          |
| `ollama.show()`   | Get details about a model                              |
| `ollama.pull()`   | Download a model                                       |
| `ollama.create()` | Create a model from an existing model or configuration |
| `ollama.copy()`   | Copy a model under another name                        |
| `ollama.delete()` | Delete a local model                                   |
| `ollama.ps()`     | List models currently loaded in memory                 |
| `ollama.push()`   | Upload a model to a registry                           |


# Important response properties

When you call `generate()` or `chat()`, the response contains more than just the answer.

### With `generate()`

```py
response = ollama.generate(
    model="llama3.2",
    prompt="Explain Python in one sentence."
)

print(response.response) # Generated text
print(response.model) # Model used
print(response.done) # Whether generation is complete
print(response.total_duration) # Total processing time, in nanoseconds
print(response.eval_count) # Number of generated tokens  
```

# Some useful Models

1\. **Qwen3** - A good model family to explore tool calling, reasoning, and agent workflows.

2\. **Llama 3.1 (8B)** - A well-known model with explicit tool-calling support. Useful for following established tutorials and understanding how models return tool calls.

3\. **Qwen2.5-Coder** - Worth exploring when your tools involve code generation, code analysis, or developer workflows. Tool-calling behavior depends on the specific model variant.

4\. **Qwen3-VL** & **Gemma 3**- Good for image understanding, screenshots, visual reasoning, and OCR-style tasks.

-------

# Ollama with tools 

Full Code - Langchain_Code\7-ollama\1_ollama_tool_calling_with_sqllite.py

```py
def check_stock(product_name: str) -> int:
def check_price(product_name: str) -> int:

messages = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant that can check the stock and price of a product.'
    },
    {
        'role': 'user',
        'content': 'What is the stock of iPhone 15? And what is the price of iPhone 15?'
    }
]

# Give the tools to an Ollama model
tools = [check_stock, check_price]
result = ollama.chat(model="llama3.1:8b", messages=messages, tools=tools)

print(result.message.tool_calls)
'''
[ToolCall(function=Function(name='check_stock', arguments={'product_name': 'iPhone 15'})), 
ToolCall(function=Function(name='check_price', arguments={'product_name': 'iPhone 15'}))]
'''

available_functions = {
    'check_stock': check_stock,
    'check_price': check_price,
}

for tool_call in result.message.tool_calls:
    tool_name = tool_call.function.name
    result = available_functions[tool_name](**tool_call.function.arguments)
    messages.append({
        'role': 'tool',
        'content': f"Result: {result}"
    })

# Now finally called Model with the updated messages
final_result = ollama.chat(model="llama3.1:8b", messages=messages)
print(final_result.message.content)
```

