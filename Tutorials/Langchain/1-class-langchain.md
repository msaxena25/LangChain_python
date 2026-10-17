## What is LangChain?

LangChain is an **open-source framework for building applications powered by Large Language Models (LLMs)**.

The easiest way to understand it is:

> **LangChain provides reusable building blocks to connect an LLM with prompts, data, APIs, tools, memory/state, retrieval, and application workflows.**

It is **not an LLM**.


# 1. Without LangChain

Suppose you want to build an AI e-commerce assistant.

You could directly call an LLM API:

```javascript
const response = await openai.chat.completions.create({
  model: "...",
  messages: [
    {
      role: "user",
      content: "Where is my order?"
    }
  ]
});
```

This works perfectly.

But as the application becomes bigger, you might need:

```text
LLM
+
Prompt templates
+
Conversation state
+
RAG
+
Vector DB
+
Multiple APIs
+
Tools
+
Structured output
+
Agents
+
Streaming
+
Tracing
+
Evaluation
```

Managing all of this yourself becomes more complicated.

# Langchain Intro

LangChain was created by Harrison Chase. It began as his open-source side project in October 2022.

- First version released: October 24, 2022

- Initial release: A Python package for building LLM applications by connecting language models with data and other components.

- Co-founder: Ankush Gola joined Harrison Chase to establish LangChain as a company in early 2023.

# LangChain Versions 

Yes. One small clarification first: **LangChain did not have a clean sequence like v1 → v2 → v3.** It started as `0.x`, evolved through `0.1`, `0.2`, `0.3`, and then made the major jump to **1.0**. [LangChain](https://www.langchain.com/blog/three-years-langchain?utm_source=chatgpt.com)

### LangChain timeline

| Version / phase | When | What changed |
|---|---|---|
| **Initial / 0.x** | **Oct 2022** | Started as a small **Python package** created by **Harrison Chase** as a side project. Focus: connecting LLMs with external data/tools and building LLM applications. [LangChain](https://www.langchain.com/blog/three-years-langchain?utm_source=chatgpt.com) |
| **0.1** | **Jan 2024** | Major architecture cleanup: separated `langchain-core`, `langchain-community`, and the higher-level `langchain` package. **LCEL/Runnables** became an important composition model. [blog.langchain.com](https://www.blog.langchain.com/the-new-langchain-architecture-langchain-core-v0-1-langchain-community-and-a-path-to-langchain-v0-1?utm_source=chatgpt.com) |
| **0.2** | **May 2024** | Documentation and APIs were reorganized around newer mental models; **LangGraph became the recommended approach for building agents**. [LangChain Blog](https://blog.langchain.dev/documentation-refresh-for-langchain-v0-2/?utm_source=chatgpt.com) |
| **0.3** | **Sep 2024** | Continued cleanup and modernization; Python moved to **Pydantic 2**, JS package dependencies were improved, and more integrations were separated into dedicated packages. [LangChain Blog](https://blog.langchain.dev/announcing-langchain-v0-3/?utm_source=chatgpt.com) |
| **1.0** | **Oct 22, 2025** | **Major modern version.** LangChain was substantially redesigned around agents, `createAgent`, middleware, standardized content blocks, and a much smaller/core-focused API surface. Legacy functionality moved to `langchain-classic`. [LangChain](https://www.langchain.com/blog/langchain-langgraph-1dot0?utm_source=chatgpt.com) |


And an important point for your learning:

> **You should learn LangChain 1.x as the primary/current way, but understand 0.x terminology because you'll encounter it everywhere in older tutorials, projects, and interview discussions.**


# Older LangChain (0.x Versions) way

The older LangChain mental model was often:

```text
                    LangChain
                       │
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼
     Models          Chains           Memory
       │               │                │
       ▼               ▼                ▼
     LLMs        SequentialChain   Conversation
                  RetrievalQA       History
                       │
                       ▼
                     Agents
```

## Core Components of langchain - 

- LLMs
- Prompt Templates
- Chains
- Indexes
- Memory
- Agents
- `RetrievalQA`
- `ConversationalRetrievalChain`
- `ConversationBufferMemory`

The fundamental idea was:

> **Connect different AI components together to build an LLM application.**

# Modern LangChain (1.x Version) way


The mental model becomes:

```text
                 Application
                     │
                     ▼
                   Agent
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        Model       Tools    Retriever
          │                     │
          │                     ▼
          │                    RAG
          │
          ▼
         State
          │
          ▼
      Persistence
```

And complex workflows can be built with **LangGraph**.

## Modern LangChain puts more emphasis on:

```text
Models
Messages
Prompts
Runnables
Retrievers
Tools
Agents
Structured Output
State
LangGraph
```

## **Now Lets understand it's Components and Classes -**

# Models

Models are classified in 2 main Categories. 1. Generative Models and 2. Embedding Model


```text
                Model
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  Generative Models      Embeddings
        │
   ┌────┴─────┐
   ▼          ▼
  LLM      Chat Model
```

## 1. LLM — Large Language Model

An **LLM** takes text as input and generates text as output.

## 2. Chat Model

This is extremely important because modern AI applications mostly use **chat models**.

Instead of simply:

```text
String → String
```

you work with messages:

```text
Messages
   ↓
Chat Model
   ↓
AI Message
```
In LangChain you would see things like:

```javascript
ChatOpenAI
ChatAnthropic
ChatGoogleGenerativeAI
```

For example:

```javascript
const model = new ChatOpenAI({
  model: "..."
});

const response = await model.invoke([
  ["system", "You are a frontend expert."],
  ["human", "Explain Angular Signals."]
]);
```

### Model configuration


For example:

```python
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=500,
    timeout=30,
    max_retries=2
)
```

Common model arguments:

| Argument | Purpose |
|---|---|
| `model` | Which LLM/model to use |
| `temperature` | Controls randomness/creativity |
| `max_tokens` | Maximum tokens generated |
| `timeout` | Request timeout |
| `max_retries` | Number of retry attempts |
| `api_key` | Authentication |
| `streaming` | Enable streaming in APIs/versions where supported |

### temperature 

temperature controls how much randomness the model uses when selecting the next token.

Range > 0.0 → 2.0

- Temperature = 0 => output more deterministic and consistent
- Temperature = 0.8 or 1.5 => higher temperature allows more variation and creativity

### Question - temperature 0 - gives exact same answer each time for same prompt with same model configurations?

At temperature=0, you will often see the exact same output for the same prompt, the answer is more deterministic, but not guaranteed to be 100% identical every time.
 

- 0 → most deterministic / consistent
- 0.2–0.5 → low randomness, good for technical tasks
- 0.7–1.0 → more varied/creative
- 1.0–2.0 → increasingly random/creative

---

### max_tokens parameter - 

`max_tokens=100` means the model can generate **up to roughly 100 output tokens**.

#### Important distinction

`max_tokens` is a **limit, not a target**.

```text
max_tokens = 500
```

does **NOT** mean:

> "Generate exactly 500 tokens."

It means:

> "Generate at most the allowed number of output tokens."

Also, **tokens ≠ words**. A token can be a whole word, part of a word, punctuation, etc.

> **`max_tokens` defines the maximum amount of output the model is allowed to generate. It controls the response length, not the quality or intelligence of the response.**

----

### Why Chat Model became important

Modern LLM providers increasingly expose their models through conversational/message-based interfaces.


## 3. Embedding Model

This one is completely different.

An embedding model **doesn't primarily generate an answer**.

Its job is:

> Convert text into a numerical vector representing its semantic meaning.

For example:

```text
"Angular Signals"
        ↓
Embedding Model
        ↓
[0.12, -0.45, 0.87, 0.21, ...]
```

### Where do OpenAI, Gemini and Claude fit?

**OpenAI, Google, Anthropic** are providers. They provide different types of models. LangChain provides integrations to communicate with these providers through standardized interfaces.

# Prompts

## What is a Prompt?

A **prompt is the instruction/input we give to an LLM or Chat Model to tell it what we want it to do.**

# 1. Simple Prompt

Wr give prompt in simple text and get result in simple text.


# 2. Prompt Template

Suppose your application needs to explain many different technologies.


You create one template:

```text
Explain {topic} in simple language.
```


```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple language."
)

result = prompt.invoke({
    "topic": "Angular Signals"
})

print(result)
```

# 3. Prompt Template with Multiple Variables

Real applications usually have several dynamic values.

```text
You are a {role}.

Explain {topic} to a developer
with {experience} years of experience.

Use {style} language.
```


Then:

```javascript
prompt.format({
  role: "Senior Frontend Architect",
  topic: "Angular Signals",
  experience: 5,
  style: "simple"
});
```

# 4. Chat Prompt Template

This becomes more important when working with **Chat Models**.

Instead of one big string, we can define different types of messages.

The model receives these as separate messages.

Older LangChain terminology commonly used:

```text
SystemMessage
HumanMessage
AIMessage
ChatPromptTemplate
```

For example:


```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior frontend architect."),
    ("human", "Explain {topic} in simple language.")
])

messages = prompt.invoke({
    "topic": "Angular Signals"
})

print(messages)
```

# 5. Few Shot Prompting

In **LangChain Python**, there is a dedicated class called **`FewShotPromptTemplate`** in the prompt-template APIs. It is specifically designed to build few-shot prompts.

### Older LangChain approach

```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

example_prompt = PromptTemplate.from_template(
    "Input: {input}\nOutput: {output}"
)

examples = [
    {"input": "I love this product", "output": "Positive"},
    {"input": "This product is okay", "output": "Neutral"},
    {"input": "Very poor quality", "output": "Negative"},
]

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Classify the sentiment:",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
)

result = prompt.invoke({
    "input": "The product is excellent"
})

print(result)
```

Conceptually, LangChain generates:

```text
Classify the sentiment:

Input: I love this product
Output: Positive

Input: This product is okay
Output: Neutral

Input: Very poor quality
Output: Negative

Input: The product is excellent
Output:
```

### Modern approach

You can also construct few-shot chat prompts using `ChatPromptTemplate` and message examples:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the sentiment."),

    ("human", "I love this product."),
    ("ai", "Positive"),

    ("human", "This product is okay."),
    ("ai", "Neutral"),

    ("human", "{input}")
])
```


### Why Prompt Templates?

Because they make prompts:

- reusable prompt 
- dynamic prompt
- maintainable
- configurable
- easier to combine with chains
- Role based prompt
- Few shots Prompting

# 5. Why System / Human / AI messages?

This is important for understanding Agents and Memory later.

Imagine a conversation:

```text
System:
You are an e-commerce support assistant.

Human:
Where is my order?

AI:
Let me check your order.

Human:
Can I change the delivery address?
```

The model can distinguish:

```text
System → Instructions
Human → User input
AI → Previous assistant response
```

# 1. NLU — Natural Language Understanding

NLU means the AI can **understand the meaning/intention behind human language**, rather than just matching keywords.

Example:

> "I want to return the shoes I bought last week."

NLU can identify:

```text
Intent:      Return product
Product:     Shoes
Time:        Last week
```

So:

```text
User language
      ↓
     NLU
      ↓
Intent + entities + meaning
```

In an e-commerce application, NLU could help distinguish:

- "Where is my order?" → **Order tracking**
- "I want to cancel my order." → **Order cancellation**
- "Can I return these shoes?" → **Product return**

Modern LLMs perform much of this understanding implicitly, so you don't necessarily build a separate NLU component anymore.

---

# 2. Context-Aware Text Generation

This means:

> **Generating a response while considering the relevant context available to the model.**

For example:

```text
User: My name is Mohit.
AI: Nice to meet you, Mohit.

User: What should I learn next?
```

The response is **context-aware** because it uses information from the previous conversation.

Context can come from several places:

```text
                Context
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
 Conversation    RAG         User data
   history     documents     /state
       │           │            │
       └───────────┼────────────┘
                   ▼
                  LLM
                   ↓
        Context-aware response
```

### Very important for LangChain

This connects directly to the things we're learning:

- **Prompt** → tells the model what to do
- **Memory/State** → provides conversation context
- **RAG/Retriever** → provides relevant external knowledge
- **Model** → generates the response using that context

So when you see **"context-aware generation"**, think:

> **LLM + relevant context → better/more relevant response.**

# Chains

## What is a Chain?

A **Chain is a sequence of operations where the output of one component becomes the input to another component.**

The key idea is:

> **Chain = connect multiple components into a workflow.**

## 1. Why were Chains introduced?

Imagine you want to build this:

```text
User:
"Explain Angular Signals"

       ↓

Prompt Template
       ↓
"Explain Angular Signals to a beginner"

       ↓

      LLM
       ↓

"Angular Signals are..."

       ↓

Output Parser
       ↓

Clean result
```

Without LangChain, you would manually write the logic connecting every step.

LangChain introduced **Chains** to make this composition easier.

---


## 2. Simple Chain

The classic example is:

```text
Prompt → LLM
```

In older LangChain Python, you might encounter:

```python
from langchain.chains import LLMChain
```

Conceptually:

```python
chain = LLMChain(
    llm=llm,
    prompt=prompt
)
```

Then:

```python
result = chain.invoke({
    "topic": "Angular Signals"
})
```
### Important

`LLMChain` is **older/legacy LangChain terminology**. Don't use it as your primary way of writing new LangChain applications today.

## 3. Sequential Chain

Now suppose you have multiple steps.

For example:

```text
User gives a topic
       ↓
Generate explanation
       ↓
Generate summary
       ↓
Generate quiz
```


Older LangChain provided concepts such as:

```text
SimpleSequentialChain
SequentialChain
```
Implementation - 

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# 1. Model
llm = ChatOpenAI(model="gpt-4o-mini")

# 2. First prompt
explanation_prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    Explain the following topic in simple language
    for a software developer:

    Topic: {topic}
    """
)

# 3. First chain
explanation_chain = LLMChain(
    llm=llm,
    prompt=explanation_prompt,
    output_key="explanation"
)

# 4. Second prompt
summary_prompt = PromptTemplate(
    input_variables=["explanation"],
    template="""
    Summarize the following explanation in 3 short bullet points:

    {explanation}
    """
)

# 5. Second chain
summary_chain = LLMChain(
    llm=llm,
    prompt=summary_prompt,
    output_key="summary"
)

# 6. Connect both chains
overall_chain = SequentialChain(
    chains=[explanation_chain, summary_chain],
    input_variables=["topic"],
    output_variables=["explanation", "summary"]
)

# 7. Run the complete sequential chain
result = overall_chain.invoke({
    "topic": "Angular Signals"
})

print("EXPLANATION:")
print(result["explanation"])

print("\nSUMMARY:")
print(result["summary"])
```

### What actually happens?

When you call:

```python
result = overall_chain.invoke({
    "topic": "Angular Signals"
})
```

LangChain executes:

```text
topic = "Angular Signals"
          │
          ▼
┌──────────────────────────┐
│     Explanation Chain    │
│                          │
│ Prompt + Chat Model      │
└────────────┬─────────────┘
             │
             ▼
      explanation
             │
             ▼
┌──────────────────────────┐
│       Summary Chain      │
│                          │
│ Prompt + Chat Model      │
└────────────┬─────────────┘
             │
             ▼
          summary
```


The **modern equivalent** is much simpler for this example:

```python
chain = explanation_prompt | llm | summary_prompt | llm
```

The key change is:

> **Old:** `LLMChain` → `SequentialChain`  
> **Modern:** `Prompt | Model | Parser`, with runnable composition.

This `|` composition is the modern Runnable/LCEL approach. A sequence can also be represented as a `RunnableSequence`. [LangChain](https://api.python.langchain.com/en/v0.1/output_parsers/langchain.output_parsers.structured.StructuredOutputParser.html?utm_source=chatgpt.com)


### Modern version

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. Model
model = ChatOpenAI(model="gpt-4o-mini")


# 2. Prompt for explanation
explanation_prompt = ChatPromptTemplate.from_template(
    """
    Explain the following topic in simple language
    for a software developer:

    Topic: {topic}
    """
)


# 3. First chain
explanation_chain = (
    explanation_prompt
    | model
    | StrOutputParser()
)


# 4. Prompt for summary
summary_prompt = ChatPromptTemplate.from_template(
    """
    Summarize the following explanation in 3 short bullet points:

    {explanation}
    """
)


# 5. Second chain
summary_chain = (
    summary_prompt
    | model
    | StrOutputParser()
)


# 6. Execute first chain
explanation = explanation_chain.invoke({
    "topic": "Angular Signals"
})


# 7. Execute second chain using first chain's output
summary = summary_chain.invoke({
    "explanation": explanation
})


print("EXPLANATION:")
print(explanation)

print("\nSUMMARY:")
print(summary)
```

### What is happening?

The flow is now:

```text
                 ┌──────────────┐
topic ──────────>│ Explanation  │
                 │ Prompt       │
                 └──────┬───────┘
                        ↓
                    Chat Model
                        ↓
                  String Parser
                        ↓
                   explanation
                        │
                        ↓
                 ┌──────────────┐
                 │ Summary      │
                 │ Prompt       │
                 └──────┬───────┘
                        ↓
                    Chat Model
                        ↓
                  String Parser
                        ↓
                     summary
```

The important thing to understand is that:

```python
explanation_chain = (
    explanation_prompt
    | model
    | StrOutputParser()
)
```

means:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Output
```

### But we can make it even more "chain-like"

Instead of manually invoking twice:


we can compose the two stages:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


model = ChatOpenAI(model="gpt-4o-mini")


explanation_prompt = ChatPromptTemplate.from_template(
    """
    Explain the following topic in simple language
    for a software developer:

    Topic: {topic}
    """
)

summary_prompt = ChatPromptTemplate.from_template(
    """
    Summarize the following explanation in 3 short bullet points:

    {explanation}
    """
)


explanation_chain = (
    explanation_prompt
    | model
    | StrOutputParser()
)


full_chain = (
    explanation_chain
    | (lambda explanation: {"explanation": explanation})
    | summary_prompt
    | model
    | StrOutputParser()
)


result = full_chain.invoke({
    "topic": "Angular Signals"
})

print(result)
```

Here the important part is:

```python
explanation_chain
    | lambda
    | summary_prompt
    | model
    | parser
```

So the output of the first chain becomes the input of the second chain.

We will learn Modern way later as well. This above is Just for quick understanding.

## run() vs invoke() method -  (For understanding)

### The important distinction

`LLMChain` supported **both** `.run()` and `.invoke()` in the older API.

For example, this was possible:

```python
explanation = explanation_chain.run(
    topic="Angular Signals"
)
```

instead of this - 

```python
explanation = explanation_chain.invoke({
    "topic": "Angular Signals"
})
```

With `.run()`: you generally get the final output directly:

```text
"Angular Signals are..."
```

With `.invoke()`: you get a dictionary-like result from the chain, typically something like:

```python
{
    "topic": "Angular Signals",
    "explanation": "Angular Signals are..."
}
```

But we have used .invoke()  method in earlier examples because `SequentialChain` takes structured inputs/outputs, so `.invoke()` makes the data flow clearer.

There are a few additional chain types such as **parallel, conditional/router, and retrieval chains**, but I would **not spend more time on Chains right now**. We'll naturally encounter these concepts when we study Runnables, RAG, and Agents.

# Indexes


**"Indexes" is an older LangChain terminology.** In modern LangChain, this area is primarily discussed through **document loaders → text splitters → embeddings → vector stores → retrievers**, especially for RAG.


So we can focus on:

```text
Documents
   ↓
Document Loaders
   ↓
Text Splitters
   ↓
Embeddings
   ↓
Vector Store / Index
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

We'll first understand **what LangChain meant by "Indexes"**, then map that to the **modern LangChain RAG architecture**, without repeating basic RAG concepts you already know.

An **index** is a structure that organizes your data so that relevant information can be retrieved efficiently later.

Think about Google:

```text
Millions of web pages
        ↓
     Index
        ↓
User searches:
"Angular Signals"
        ↓
Relevant pages
```


In an LLM application:

```text
Your documents
      ↓
   Index them
      ↓
User asks question
      ↓
Find relevant content
      ↓
Send content to LLM
```

This is the foundation of **RAG**.


## 2. Why do we need an Index?

Suppose you have:

```text
company_policy.pdf
employee_handbook.pdf
insurance_document.pdf
product_manual.pdf
```

And each document has hundreds of pages.

If the user asks:

> "What is the maximum insurance coverage?"

You don't want to send all documents to the LLM.

Instead:

```text
All documents
     ↓
Index
     ↓
Search
     ↓
Relevant chunks
     ↓
LLM
     ↓
Answer
```

The index helps us find the relevant information.

---


## 3. So where exactly is the "Index"?

This is the part that can initially be confusing.

When you hear:

> **LangChain Indexes**

don't think:

```text
Index = one specific LangChain class
```

Instead think:

> **Indexing = preparing and organizing external knowledge so that it can be efficiently retrieved later.**

Modern terminology is more explicit:

```text
Document
   ↓
Chunk
   ↓
Embedding
   ↓
Vector Store
   ↓
Retriever
```

The **vector store/index** is the searchable representation of your knowledge.


## 4. The important LangChain Indexes components

For Indexes, you should understand these five things:

### ① Document

Represents a piece of text plus metadata.

Conceptually:

```python
Document(
    page_content="Angular Signals provide...",
    metadata={
        "source": "angular-guide.pdf",
        "page": 10
    }
)
```

So a `Document` is basically:

```text
content + metadata
```

---

### ② Document Loader

Loads data from somewhere.

For example:

```text
PDF
Web page
CSV
Database
Notion
Directory
Text file
```

Conceptually:

```python
loader = SomeLoader("angular-guide.pdf")

documents = loader.load()
```

Output:

```text
[
    Document(...),
    Document(...),
    Document(...)
]
```

---

### ③ Text Splitter

Large documents aren't usually embedded as one giant piece.

So we split them:

```text
Large PDF
   ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
```

For example:

```text
Angular documentation
        ↓
5000-word document
        ↓
500-token chunks
        ↓
Chunk 1
Chunk 2
Chunk 3
...
```

This improves retrieval quality and keeps the context manageable.

---

### ④ Embedding Model

You already know this part.

The embedding model converts:

```text
"Angular Signals are reactive primitives..."
```

into something like:

```text
[0.021, -0.183, 0.742, ...]
```

That vector represents the semantic meaning of the text.

---

### ⑤ Vector Store

The vectors are stored in a vector database/store.

Examples:

```text
FAISS
Chroma
Pinecone
Qdrant
Weaviate
Milvus
PGVector
```

Then:

```text
User question
      ↓
Embedding
      ↓
Vector similarity search
      ↓
Relevant chunks
```

---


## 5. Connect this to your existing RAG

You have already built this manually yourself in Node.js:

```text
Your Documents
      ↓
Chunking
      ↓
Embeddings
      ↓
Vector DB
      ↓
Similarity Search
      ↓
Relevant chunks
      ↓
LLM
      ↓
Answer
```

LangChain doesn't fundamentally change this architecture.

With langChain, It gives you reusable abstractions for those steps & we dont need to do each steps manually.

For example:

```text
             LANGCHAIN

Document Loader
      ↓
Text Splitter
      ↓
Embedding Model
      ↓
Vector Store
      ↓
Retriever
      ↓
Chat Model
```

So instead of writing every integration yourself, LangChain provides components that can be composed.

---

## RAG vs LangChain

```text
2020
RAG (AI architecture/pattern) introduced by FAIR/Meta researchers
        ↓
2022
LangChain created
        ↓
LangChain provided components
to build RAG applications
```

So **RAG existed before LangChain**.  **Indexes were a LangChain-specific abstraction/component**.

> **RAG is an architectural pattern/design pattern that can be implemented manually using techniques such as document chunking, embeddings, vector storage, semantic search, and similarity measures like cosine similarity. LangChain is a framework that provides abstractions and components to simplify these steps. Historically, LangChain had an `Indexes` abstraction for document indexing and retrieval, which helped developers build RAG applications without implementing every part from scratch.**

Note:

❌ **Indexes = one component that provides document upload + scanning + embedding + vector search**

That's a little too broad.

More accurately: (RAG have two major parts One is Indexing and second is Retrieval)

```text
                  RAG
                   │
       ┌───────────┴───────────┐
       │                       │
   Indexing                 Retrieval
       │                       │
 Load documents           Embed query
       ↓                       ↓
 Split chunks             Similarity search
       ↓                       ↓
 Generate embeddings     Relevant chunks
       ↓                       │
 Store vectors            ──────┘
                               ↓
                              LLM
                               ↓
                             Answer
```

LangChain provides components for **each of these steps**, and historically grouped much of the indexing/data-retrieval side under **Indexes**.

# LLM APIs are stateless

An LLM API generally does **not remember your previous API call automatically**.

For example, request 1:

```text
User → "My name is Mohit."
       ↓
     LLM API
       ↓
    "Nice to meet you!"
```

Then request 2:

```text
User → "What is my name?"
       ↓
     LLM API
       ↓
"I don't know."
```

Why?

Because the second request doesn't automatically contain the first conversation. The LLM itself isn't maintaining conversational memory between these independent API calls.


### 2. So how does ChatGPT remember the conversation?

Your application sends the relevant conversation history along with the new request.


### 3. Where LangChain comes in

Historically, LangChain provided **Memory** abstractions to make this easier.

```text
User
 ↓
Application
 ↓
Memory
 ↓
Conversation History
 ↓
Prompt
 ↓
LLM
```

Modern LangChain/LangGraph (LangChain 1.x) uses a more general concept of **State**:

```text
User
 ↓
Application
 ↓
State
 ├── messages
 ├── user information
 ├── intermediate results
 └── workflow data
 ↓
LLM / Tools / Agents
```

This distinction is important:

**Memory** → older LangChain terminology  
**State** → modern workflow/application terminology

## There are Four types of Memory in langchain older way (0.x)

1. ConversationBufferMemory
2. ConversationBufferWindowMemory
3. ConversationSummaryMemory
4. Custom  Memory

### ConversationBufferMemory

It simply kept the conversation history.

Conceptually:

```python
memory = ConversationBufferMemory()
```

But there is a problem of this memory pattern  - 

Imagine 1,000 messages:

```text
Message 1
Message 2
Message 3
...
Message 1000
```

If we send the entire history to the LLM every time, we consume more and more **context window / tokens**.

### ConversationBufferWindowMemory

kept only the **most recent N interactions**.

For example:

```text
Window = 3
```

Then:

```text
Message 1  ❌
Message 2  ❌

Message 3  ✅
Message 4  ✅
Message 5  ✅
```

### ConversationSummaryMemory

Another approach was to summarize older conversation. Instead of keep Conversations as it is 

you might maintain:

```text
Summary:
"User is Mohit, a frontend engineer.
He works primarily with Angular, React and Next.js.
He is currently learning LangChain..."
```

Then recent messages could be kept separately:

```text
Summary of old conversation
+
Recent messages
+
Current question
```

This reduces token usage.

### Custom memory

For advanced use cases, you can store specialized state (e.g. user's preferences or key facts about him) in a Custom memory class.

### In Modern way we have Memory like
```
State
  ↓
Messages
  ↓
Checkpointing
  ↓
Persistence
  ↓
LangGraph
```

Will cover further.

## Can we implement ConversationBufferWindowMemory?

### 1. Without LangChain — you can code it yourself

`ConversationBufferWindowMemory` is not some special capability that only LangChain can provide.

You can implement the same idea yourself:

```python
history = [
    {"role": "user", "content": "My name is Mohit"},
    {"role": "assistant", "content": "Nice to meet you"},
    {"role": "user", "content": "I work with Angular"},
    {"role": "assistant", "content": "Great!"}
]

# Keep only the last N messages
recent_history = history[-4:]
```

Then send `recent_history` along with the new user message to the LLM API.

### 2. With older LangChain

LangChain gave you a ready-made abstraction:

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(k=3)
```

### Full example of how we use this - 


```python
from langchain_openai import ChatOpenAI
from langchain_classic.memory import ConversationBufferWindowMemory
from langchain_classic.chains import ConversationChain

# 1. Create the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# 2. Create memory
# Keep only the latest 3 conversation turns
memory = ConversationBufferWindowMemory(k=3)

# 3. Connect memory with the conversation chain
conversation = ConversationChain(
    llm=llm,
    memory=memory
)
# 4. First interaction
response = conversation.invoke(
    {"input": "My name is Mohit."}
)

print(response["response"])

```

# AI Agent

A normal LLM application follows a **predefined flow**: 

User > Prompt > LLM > Response


An agent is different:

```text
           User
            ↓
       ┌───────────────┐
       │      LLM      │
       │  Think/Decide │
       └───────┬───────┘
               ↓
        What should I do?
          ↙    ↓     ↘
       Tool 1 Tool 2  Tool 3
          ↘    ↓     ↙
       Tool result
           ↓
          LLM
           ↓
   Is the task complete?
       ↙          ↘
     No            Yes
     ↓              ↓
   Tool           Answer
```

The key idea is:

> **An AI agent allows the model to decide what actions/tools to use and in what order, based on the user's goal and the results it receives.**


An agent is different:

```text
User
  ↓
       ┌───────────────┐
       │      LLM      │
       │  Think/Decide │
       └───────┬───────┘
               ↓
        What should I do?
          ↙    ↓     ↘
       Tool 1 Tool 2  Tool 3
          ↘    ↓     ↙
       Tool result
           ↓
          LLM
           ↓
   Is the task complete?
       ↙          ↘
     No            Yes
     ↓              ↓
   Tool           Answer
```

The key idea is:

> **AI Agent have two powers - 1. is Reasoning Capabilities and 2. is Tools**

> **An AI agent allows the model to decide what actions/tools to use and in what order, based on the user's goal and the results it receives.**

---

## 2. Simple example

Suppose you ask:

> **"What's the weather in Delhi and should I carry an umbrella?"**

A normal LLM may simply answer based on what it knows.

An agent could decide:

```text
User question
      ↓
LLM
      ↓
I need current weather information.
      ↓
Weather Tool
      ↓
"Rain expected, 80% probability"
      ↓
LLM
      ↓
"I'd recommend carrying an umbrella."
```

Notice something important:

**You didn't explicitly tell the model to call the weather tool.**

The **agent decided** that the tool was necessary.

---

##  Agent vs Chain

Chain > You define the sequence: Step 1 → Step 2 → Step 3 → Answer
Agent > The LLM decides the next action.

> **Chain = developer controls the workflow.**  
> **Agent = LLM can dynamically decide the workflow.**

### Some examples of Tools - 


Things the agent can use.

Examples:

```text
Search API
Database
Calculator
Weather API
File system
GitHub
Jira
Browser
Your custom API
MCP tools
```

# Example of Open AI Model implementation

### 1. `.env` file

Create a `.env` file:

```env id="z4x0c2"
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### 2. Install `python-dotenv`

```bash id="zq6p3u"
pip install python-dotenv
```


### 3. Load the environment variables

```python id="k5l4q8"
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
```

### OpenAI

```python id="v5f1c3"
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=500,
    timeout=30,
    max_retries=2,
    api_key=openai_key
)

response = model.invoke(
    "Explain Angular Signals in simple language."
)

print(response.content)
```

Note - You don't have to pass api_key explicitly if you use the provider's expected environment-variable name.
For the two examples:

- OPENAI_API_KEY=your-openai-key (ChatOpenAI automatically looks for)
- ANTHROPIC_API_KEY=your-anthropic-key

---

# Prompt Classification

**at a high level, we can classify prompts in two ways**


### 1. Text-only prompt

The input contains only text.

```text
"Explain Angular Signals in simple language."
```

In LangChain:

```python
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple language."
)
```

---

### 2. Multimodal prompt

The input contains **multiple types of content**, such as:

```text
Text + Image
Text + Audio
Text + Video
```

For example:

```text
"What's wrong with this UI?"
        +
[uploaded screenshot]
```

Or:

```text
"Describe this image."
        +
[image]
```

The model must support the corresponding modality.

# Now Lets explore more on Text based prompt 

## Text based prompt are classified in two Categories Static Prompt and Dynamic Prompt.

## 1. Static Prompt

A **static prompt** is a prompt whose instructions/content are fixed in your code.

```text
User
 ↓
Fixed Prompt
 ↓
LLM
 ↓
Response
```

```python
prompt = """
You are a helpful software assistant.

Explain Angular Signals in simple language.
Keep the answer under 200 words.
"""
```
Every time you call the model, essentially the same prompt is sent.

### Problem with static prompts

- A single fixed prompt doesn't behave differently for different users like beginners , seniors etc..
- Can not fit for different Context or topic.

## 2. Dynamic Prompt

A **dynamic prompt changes based on runtime information**. and thats why dynamic prompts are widely used.


Now:

```text
experience_level = "beginner"
topic = "Angular Signals"
```

> **Static prompts are useful for fixed instructions; dynamic prompts are useful when the prompt needs runtime information.**

And in modern AI applications, **dynamic prompt construction is extremely common** because the LLM needs context about the current user, task, retrieved information, tools, state, etc.

# Open-source vs closed-source AI models

Open Source weight are publicly available, allowing developers to download and run the model themselves, subject to its license.

Examples: Llama, Qwen, Mistral, Falcon, Bloom

Closed-source models - The weights are not publicly released. Developers typically access these models through a provider's API or hosted service.

Examples: OpenAI GPT models, Anthropic Claude.

One important distinction: open-source and open-weight are not exactly the same. A model can have publicly downloadable weights without releasing all its training data, training code, or other components. Licenses can also restrict some uses.

# Embedding Models

Embeddings do not generate answers. They represent text as vectors so you can compare meaning and retrieve relevant content.

```
from langchain_google_genai import GoogleGenerativeEmbedding

model = GoogleGenerativeEmbedding(model='gemini-3.8-flash', google_api_key=GOOGLE_API_KEY)
result = model.embed_query("Who is prime minister of India?")
print(result) # This will print the response from the LLM
```

## Diff between embed_query and embed_document

embed_document - Converts a list of documents into vectors'

embed_query - Covert a single query to vectors

```
documents = [
    "Angular is a frontend framework.",
    "React is a JavaScript UI library.",
    "RAG retrieves relevant information for an LLM."
]

vectors = embeddings.embed_documents(documents)

print("Number of vectors:", len(vectors))
print("Dimensions per vector:", len(vectors[0]))
```

## Understand dimension prop with embedding Model

```
model = GoogleGenerativeEmbedding(model='gemini-3.8-flash', output_dimensionality=32)

OR

model = OpenAIEmbeddings(model='text-embedding-3-large', dimensions=32)
```

Think of dimensions as the size of a list of numbers that represents the meaning of a sentence.

Text = "I love angular";

3 dimensions = 3 Vectors
[0.2, 0.8, 0.5]

500 dimensions = 500 numbers in Vector List

Each Model have different max size of their dimension.

text-embedding-3-large	3,072
text-embedding-3-small	1,536
gemini-embedding-001	3,072


### 2. Why do we need dimensions?

Think of it like image resolution:

- Fewer dimensions: smaller vector, less storage.
- More dimensions: larger vector, potentially more semantic detail.

The trade-off is that more dimensions don't automatically guarantee better results.

Notice the difference:

- Gemini: `output_dimensionality=768`
- OpenAI: `dimensions=768`

| Term                    | Meaning                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| `output_dimensionality` | The configuration parameter used to choose the output vector size. |
| `dimensions`            | The number of values in the resulting embedding vector.            |

# Coshine similarity with scikit-learn Package

`sklearn.metrics.pairwise` is a module inside the scikit-learn Python library that provides functions to calculate similarity or distance between numerical vectors.


scikit-learn - Machine learning Python library

metrics - Tools to evaluate and measure results

pairwise - Functions to compare pairs of vectors

```
pip install scikit-learn
```

Example:

```
from sklearn.metrics.pairwise import cosine_similarity
vector_a = [[1, 2, 3]]
vector_b = [[1, 2, 4]]
score = cosine_similarity(vector_a, vector_b)
print(score)
```