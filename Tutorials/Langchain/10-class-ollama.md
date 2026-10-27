# What is Ollama?

Ollama is a `tool` that lets you `download and run AI models` `locally` on your own computer, instead of sending every prompt to a cloud-based API such as Gemini or OpenAI.

For example, you can run models such as Llama, Gemma, or Qwen on your computer and interact with them through a command line, an API, or frameworks such as LangChain.

Ollama exposes a local API, usually at `http://localhost:11434`, which your application can call.

Install Ollama from the official website: [Download Ollama](https://ollama.com/download?utm_source=chatgpt.com).

### Quick diff from Huggingface

**Hugging Face** = A platform where you can find and download AI models, Download datasets for machine learning,Experiment with a wide variety of pretrained models.

**Ollama** = A tool to run a chat model locally on your computer, and can Use a local model with LangChain.

------

# Several ways to Run Ollama

## 1. The main ways to use Ollama

| Method                   | Example                | Best use                            |
| ------------------------ | ---------------------- | ----------------------------------- |
| 1. CLI                   | `ollama run llama3.2`  | Interact directly in the terminal   |
| 2. Python library        | `ollama.generate(...)` | Use the model in Python             |
| 3. REST API              | `POST /api/generate`   | Connect any language or application |
| 4. JavaScript library    | `ollama.generate(...)` | Use it from Node.js                 |
| 5. LangChain integration | `ChatOllama`           | Build chains, RAG and agents        |

**Let's understand them one by one.**

## 2. Method 1 — CLI

First, download a model:

```py
ollama pull llama3.2 # pull model

ollama run llama3.2 # run model

# after run, you can direct start chat into terminal.

```

## 3. Method 2 — Python library

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

## 4. Method 3 — REST API

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

## 5. Method 4 — JavaScript / Node.js

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

## 6. Method 5 — LangChain integration

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
import ollama
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

# Ollama 

## 1. Model interaction methods

These are the most important methods to learn first.

| Method              | Purpose                               |
| ------------------- | ------------------------------------- |
| `ollama.generate()` | Generate text from a prompt           |
| `ollama.chat()`     | Generate responses from chat messages |
| `ollama.embed()`    | Convert text into embedding vectors   |

## 2. Model management methods

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


## 3. Important response properties

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