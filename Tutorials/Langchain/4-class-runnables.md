# Runnables

## 1. What is a Runnable?

Runnables are one of the most important concepts in modern LangChain. 

They let you connect prompts, models, parsers, Python functions, retrievers, and other components into a single workflow called a chain.

Technically - A Runnable is a component that follows a common interface so it can be executed, combined with other components, and used in different execution modes.

## Two Important Categories of Runnables

In LangChain, it is useful to distinguish between `task-specific Runnables` and `Runnable primitives`.

## 1. Task-specific Runnables

These perform a particular job in a LangChain application.

Examples:

- `ChatPromptTemplate` — prepares chat messages.
- `ChatOpenAI` — calls a chat model.
- `StrOutputParser` — converts model output to text.
- `PydanticOutputParser` — parses and validates structured output.
- `Retriever` — retrieves relevant documents.

## 2. Runnable primitives

These are general-purpose building blocks used to compose, transform, route, or control workflows.

Examples:

- `RunnableSequence`
- `RunnableParallel`
- `RunnableLambda`
- `RunnableBranch`
- `RunnablePassthrough`

-----

## 1. `RunnableSequence` — execute sequentially

Runs components one after another. You usually create it using the `|` operator.

```
from langchain_core.runnables import RunnableSequence

chain = RunnableSequence(
    prompt,
    model,
    parser
)
```

Equivalent to `prompt | model | parser`.

---

## 2. `RunnableParallel` — run multiple tasks

Sends the same input to multiple Runnables and returns a dictionary containing their results.

```py
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)

result = chain.invoke({"feedback": "Excellent product!"})
```

We can pass arguments into RunnableParallel in two ways:

1. Keyword arguments
2. Dictionary arguments

Keyword arguments are more readable and easier to understand.

Dictionary arguments are more flexible and can be used to build dynamic chains.

```py
# Keyword arguments
parallel_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)

# Dictionary arguments
parallel_chain = RunnableParallel({"summary": summary_chain, "sentiment": sentiment_chain})
```

Output shape:

```
{    "summary": "...",    "sentiment": "..."}
```
---

## `RunnablePassthrough` — preserve the input

RunnablePassthrough solves a common problem in chain composition: how do you keep the original input available while performing additional processing?

```py
from langchain_core.runnables import RunnablePassthrough

chain = RunnablePassthrough()

result = chain.invoke({"text": "I love the product!"})
print(result)
# {'text': 'I love the product!'}
```

Suppose you want to process a piece of text in two ways:

- Keep the original text.
- Convert it to lowercase.

```py
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

chain = RunnableParallel(
    original=RunnablePassthrough(),
    lowercase=lambda text: text.lower()
)

result = chain.invoke("HELLO LANGCHAIN")

print(result)

{
    "original": "HELLO LANGCHAIN",
    "lowercase": "hello langchain"
}
```

**Another example**

```py

prompt3 = PromptTemplate.from_template("Explain following topic: {topic}")

prompt4 = PromptTemplate.from_template("Write a summary of the following explanation: {explanation}")

parser = StrOutputParser()

# explaination generator chain
explanation_generator_chain = RunnableSequence(prompt3, model, parser)

# summary generator chain with preserve explanation_chain output as it is
parellel_chain = RunnableParallel(
    explanation=RunnablePassThrough(),
    summary=RunnableSequence(prompt4, model, parser)
)

# combine both chains
final_chain = RunnableSequence(explanation_generator_chain, parellel_chain)
'''
1. final_chain will be run first with the input {"topic": "AI"}
2. explanation_generator_chain will be run with the input {"topic": "AI"} and output the explanation
3. parellel_chain will be run with the input {"explanation": "AI is a technology that allows machines to learn from data and make decisions."} and output the summary
4. final_chain will output the result {"explanation": "AI is a technology that allows machines to learn from data and make decisions.", "summary": "..."}
'''

result = final_chain.invoke({"topic": "AI"})

print(result)
# {    "explanation": "AI is a technology that allows machines to learn from data and make decisions.",    "summary": "..."}

```

## `RunnablePassthrough` with .assign() method —

- RunnablePassthrough.assign() expects a dictionary input.
- .assign() preserves the existing dictionary fields and adds the other field.

```py

print('Test RunnablePassthrough.assign()...')

# explaination generator chain
explanation_generator_chain = RunnableSequence(prompt3, model, parser)

# summary generator chain
summary_generator_chain = RunnableSequence(prompt4, model, parser)

'''
RunnablePassthrough.assign() takes a dictionary of key-value pairs and assigns them to the output dictionary.
It will throw error in case input is not a dictionary.

explanation_generator_chain will output the explanation as a string.
We need to convert it to a dictionary with key "explanation" using lambda function.
Then we can assign the summary to the output dictionary using RunnablePassthrough.assign().

'''


chain =  RunnableSequence(
    explanation_generator_chain,
    lambda text: {"explanation": text}, # coverting the explanation to a dictionary with key "explanation"
    RunnablePassthrough.assign(summary=summary_generator_chain))

result = chain.invoke({"topic": "Cricket"})

print(result)
# {    "explanation": "Cricket is a sport that is played between two teams of 11 players each. The game is played on a field with a rectangular shape and a target called the wicket. The objective of the game is to score runs by hitting the ball with a bat and running between the wickets. The team with the most runs at the end of the game wins.",    "summary": "..."}

```

---

## RunnableLambda

In real applications, many times we need to clean text, calculate values, transform data, validate input, or prepare information for the next prompt.

That's where `RunnableLambda` comes in.

###  real-world problems it solves

| Problem                   | Example use                         |
| ------------------------- | ----------------------------------- |
| Clean input               | Remove extra spaces, normalize text |
| Transform data            | Convert a string into a dictionary  |
| Calculate values          | Count words, calculate scores       |
| Apply business rules      | Set a category based on a threshold |
| Prepare model input       | Rename or reshape fields            |
| Post-process model output | Extract a value or format a result  |

**For example, you could use a Python function to classify a score without asking an LLM:**

Note: Calculations which can be done easily, should not be done with LLMs because LLms are expensive.

```py
from langchain_core.runnables import RunnableLambda

def classify_score(score):
    if score >= 80:
        return "high"
    elif score >= 50:
        return "medium"
    return "low"

score_chain = RunnableLambda(classify_score)

print(score_chain.invoke(90))
```

**Clean up a messy text containing emojis, special characters, extra spaces**

```
text = "   🚀 Hello!!!   LangChain @AI #Python 😊   is   awesome... 💡 \n\t Let's learn!!! $$$  "
```

```py
import re # regular expression
from langchain_core.runnables import RunnableLambda

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # Remove emojis and special characters
    text = re.sub(r"_", "", text)        # Remove underscores
    text = re.sub(r"\s+", " ", text)     # Replace multiple spaces/newlines with one space
    return text.strip()                  # Remove leading/trailing spaces

clean_chain = RunnableLambda(clean_text)

result = clean_chain.invoke(text)

print(result)
# Hello LangChain AI Python is awesome Lets learn
```

----

## `RunnableBranch`

You can think of `RunnableBranch` as the `if / elif / else` of the LangChain world. That's a very good mental model.

It lets you choose which Runnable or chain to execute based on a condition.

### 1. What problem does it solve?

**Suppose you are building a customer-feedback application. You want to:**

- If feedback is positive, generate a thank-you message.
- If feedback is negative, generate an apology and offer help.
- Otherwise, generate a general response.

Without `RunnableBranch`, you might write ordinary Python `if/else` logic outside your LangChain chain and call the appropriate chain manually.

`RunnableBranch` lets you put that routing logic inside the LangChain workflow, so the entire process can be invoked as one chain.

**Suppose LLM generated report on any topic. You want to:**

- If report's total words count are > 500 then again call LLM to write summary fo that report.
- If report's total words count are with in 500 then print report as it is.

**company's email-routing system. You want to:**

The workflow will classify the incoming email into one of four departments:

- Complaint → Customer Support
- Refund or payment → Payment Team
- Technical issue → Technical Team
- General query → Chatbot handles it directly

```py

print('Test RunnableBranch - company email-routing system...')

from pydantic import BaseModel, Field
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda

# Lets create Pydantic Schema for email classification

class EmailClassification(BaseModel):
    emailCategories: Literal["Complaint", "Refund or payment", "Technical issue", "General query"] = Field(description="The category to which the email belongs")

# Now create Pydantic Output Parser for email classification
email_classification_parser = PydanticOutputParser(pydantic_object=EmailClassification)

# email classification prompt with email input and standard format instructions
# used standard format instruction because we need exact output in the form of Pydantic Schema
# Because further in RunnableBranch, we will route based on that exact output.

email_classification_prompt = PromptTemplate(
    template="""
    Classify the following email into one of four categories:
    - Complaint: Customer dissatisfaction or complaints
    - Refund or payment: Refunds or payments related issues
    - Technical issue: Technical issues or problems
    - General query: General queries or questions

    Email: {email}
    {format_instructions}
    """,
    input_variables=["email"],
    partial_variables={"format_instructions": email_classification_parser.get_format_instructions()}
)

# email classification chain
email_classification_chain = RunnableSequence(email_classification_prompt, model, email_classification_parser)

# email routing chains
customer_support_team_chain = RunnableLambda(lambda email: "Customer Support Team") # This is a dummy chain for demonstration purposes.

# payment team chain
payment_team_chain = RunnableLambda(lambda email: "Payment Team") # This is a dummy chain for demonstration purposes.

# technical team chain
technical_team_chain = RunnableLambda(lambda email: "Technical Team") # This is a dummy chain for demonstration purposes.

# general query prompt - for this we need LLM to response and handle the general query email.
general_query_prompt = PromptTemplate.from_template(
    "You are the company's customer support chatbot. Handle the following general query email: {email}")

# general query chain
general_query_chain = RunnableSequence(general_query_prompt, model, parser)

# Now create a RunnableBranch chain

# RunnableBranch takes a list of tuples.
# Each tuple contains a condition and a chain.
# The condition is a lambda function that takes the email and returns a boolean value.
# The chain is the chain to execute if the condition is true.

runnable_branch_chain = RunnableBranch(
    (lambda email: email.emailCategories.lower() == "complaint", customer_support_team_chain),
    (lambda email: email.emailCategories.lower() == "refund or payment", payment_team_chain),
    (lambda email: email.emailCategories.lower() == "technical issue", technical_team_chain),
    general_query_chain # If not in above three then treat as general query
)

# final chain
# RunnablePassthrough.assign - it will preserve the email input as it is.

final_workflow_chain = RunnablePassthrough.assign(
    result = RunnableSequence(email_classification_chain, runnable_branch_chain)
)

result = final_workflow_chain.invoke({"email": "Could you please tell me, how can I order the product?"})
print(result)
'''
 {'email': 'Could you please tell me, how can I order the product?', 'result': "Hello! Thank you for reaching out to us. \n\nI am our automated customer support assistant, and I'd be happy to help you today. Since your message falls under a general query, could you please provide a few more details or let me know what specific question you have about our products, services, or policies? \n\nOnce you share the details, I'll get you the right information right away!"}
'''
```

---


# LCEL (LangChain Expression Language)

LCEL is one of the most important concepts to understand after learning Runnables.

**LCEL is the way LangChain lets you compose multiple components into a chain using a declarative, pipe-based syntax.**

LangChain has different Runnable primitives, such as RunnableSequence, RunnableParallel, RunnableLambda, RunnableBranch, and RunnablePassthrough. Each helps us build a particular kind of workflow.

RunnableSequence connects components sequentially. So instead of creating RunnableSequence class, we can use newer syntex now.

```py
chain = RunnableSequence(prompt, model, parser)

can we written as with LCEL - 

chain = prompt | model | parser

# | - this syntax is called as pipe.

```

**By LCEL - You can compose Runnable components simpler and more consistent.**

-----

# LangChain Runnable methods

LangChain provides several other methods to handle multiple inputs, streaming output, asynchronous execution, and configuration.


The easiest way to learn them is to understand the use case for each method.

## 1. Main Runnable methods

| Method              | Purpose                                 | When to use                                   |
| ------------------- | --------------------------------------- | --------------------------------------------- |
| `.invoke()`         | Executes a Runnable for one input       | One question or one request                   |
| `.batch()`          | Executes a Runnable for multiple inputs | Processing many questions                     |
| `.stream()`         | Yields output chunks progressively      | Showing a response as it is generated         |
| `.ainvoke()`        | Asynchronous version of `.invoke()`     | Non-blocking execution in async code          |
| `.abatch()`         | Asynchronous version of `.batch()`      | Processing multiple inputs asynchronously     |
| `.astream()`        | Asynchronous streaming                  | Streaming in an async application             |
| `.astream_events()` | Streams execution events from a chain   | Monitoring or building detailed streaming UIs |

These are the main execution methods. There are also helper methods, such as `.with_retry()`, `.with_fallbacks()`, and `.with_config()`, which we'll cover next.

### A. `.invoke()` — one  input and one response

```py
result = chain.invoke({"topic": "Python"})
lprint(result)
```

Use when: You need one response, such as answering a user's question.


### B. `.batch()` — multiple inputs & multiple response

```py
results = chain.batch([
    {"topic": "Python"},
    {"topic": "LangChain"},
    {"topic": "RAG"}
])

for result in results:
    print(result)
```

Use when: You need to process many independent inputs, such as summarizing 100 documents.

By default, LangChain runs batch inputs concurrently using a thread pool. Results are returned in the same order as the inputs. Actual speed depends on the model, API limits, and configuration.

### C. `.stream()` — receive output progressively

```py
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```

Use when: You want to display a response as it is generated instead of waiting for the entire answer.

This is useful for chat interfaces, where the user sees text appearing progressively. The exact chunks depend on the Runnable and whether its components support streaming.

----