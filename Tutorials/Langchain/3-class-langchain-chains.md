# LangChain: Chains — Complete Learning Guide

A chain is a sequence of components connected together to perform a task. Each component takes some input, performs an operation, and passes its output to the next component.

## Why are chains important in LangChain?

Without chains, you would manually call each component, manage the intermediate results, and pass data between them.

Chains help you:

1. Connect components: Link prompts, models, output parsers, retrievers, and other operations.
2. Reuse logic: Define a workflow once and invoke it with different inputs.
3. Compose workflows: Combine smaller chains into larger applications.
4. Run tasks in parallel: Execute independent operations concurrently.
5. Standardize execution: Use common methods such as `.invoke()`, `.batch()`, and `.stream()` where supported.
6. Build AI applications: Implement summarization, RAG, document processing, classification, and multi-step generation.

The key idea is that LangChain lets you treat many components as composable units with a common interface.

## 3. Types of chains in LangChain

One important point: LangChain does not have one fixed, universal list of chain types. You will see two ways of learning them:

- Traditional LangChain: named classes such as `LLMChain`, `SimpleSequentialChain`, `SequentialChain`, and `RetrievalQA`.
- Modern LangChain: composable Runnables connected using `|`, `RunnableParallel`, `RunnablePassthrough`, and other components.

## Below are chains which are used 

1. Basic chain: `prompt | model | parser`
2. Sequential chain: pass one step's output to the next.
3. Parallel chain: run independent prompts or operations concurrently.
4. Merge chain: combine outputs with `RunnablePassthrough.assign()`.
5. Conditional chain: use `RunnableBranch`.
6. RAG chain: connect a retriever with a prompt and model.
7. LangGraph: learn stateful, multi-step workflows when you need loops, checkpoints, or human-in-the-loop control.

The main takeaway: A chain is a composable workflow, not necessarily a special class. In modern LangChain, you build workflows by connecting Runnables. Once you understand sequential, parallel, merge, and conditional patterns, you can combine them to create much more complex AI applications.

## Basic Chain

```py
chain =  prompt | model | parser
result = chain.invoke()
```
## Sequential chain

One step's output becomes the next step's input.

Ex - Generate a product description, then translate that description into Hindi.

This pattern is useful when a later step depends on the output of an earlier step.

```py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

parser = StrOutputParser()

# First prompt
description_prompt = ChatPromptTemplate.from_template(
    "Write a short product description for {product}."
)

# Second prompt
translation_prompt = ChatPromptTemplate.from_template(
    "Translate this product description into Hindi:\n{description}"
)

# Create the first chain
description_chain = description_prompt | model | parser

# Create the second chain
translation_chain = (
    {
        "description": description_chain
    }
    | translation_prompt
    | model
    | parser
)

result = translation_chain.invoke({
    "product": "Wireless headphones"
})

print(result)

```

## Parallel chain — multiple tasks at the same time

Scenario: Generate a description and list product features independently.

```py
from langchain_core.runnables import RunnableParallel

description_chain = (
    ChatPromptTemplate.from_template(
        "Describe this product briefly: {product}"
    )
    | model
    | parser
)

features_chain = (
    ChatPromptTemplate.from_template(
        "List three features of: {product}"
    )
    | model
    | parser
)

# we use RunnableParallel class to run chains in Parallel.
parallel_chain = RunnableParallel(
    description=description_chain,
    features=features_chain,
)

result = parallel_chain.invoke({
    "product": "Wireless headphones"
})

print(result["description"])
print(result["features"])
```

Output is a dictionary containing both results.

Use parallel execution when tasks are independent. It can reduce overall waiting time, although model latency and API rate limits affect the actual speed.

## Merge chain — combine results before the next step

Merge is an important concept, it is not type or a separate, dedicated chain class in modern LangChain.

Suppose you have the original product name, its description, and its features. You want to preserve all three values in one dictionary.

You can see all Chain's Code in file - ChatModels\chain.py

```py
from langchain_core.runnables import RunnablePassthrough

merge_chain = RunnablePassthrough.assign(
    description=description_chain,
    features=features_chain,
)

result = merge_chain.invoke({
    "product": "Wireless headphones"
})

print(result.keys())
```

The result contains these keys:

```
dict_keys(["product", "description", "features"])
```

`RunnablePassthrough.assign()` preserves the original input and adds the generated outputs. The assigned chains receive the original input dictionary and can run concurrently.

You can then feed that merged dictionary into a final chain:

```py
final_prompt = ChatPromptTemplate.from_template("""
Write a marketing summary for {product}.

Description:
{description}

Features:
{features}
""")

final_chain = final_prompt | model | parser

workflow = merge_chain | final_chain

result = workflow.invoke({
    "product": "Wireless headphones"
})

print(result)
```

This is a practical example of composing smaller chains into a larger workflow. 

## Conditional chain — choose a path dynamically

Sometimes you need different processing logic based on the input. LangChain provides `RunnableBranch` for conditional routing.

Let's create a conditional chain for sentiment analysis using RunnableBranch.


Requirement:

- If feedback is positive → thank the customer and encourage them to share more feedback.
- If feedback is negative → apologize and offer help resolving the issue.

## Python code

```py

from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from typing import Literal  #Literal comes in typing package

# Why definding this schema
# Because - We dont want LLM return anything else positive or negative (just single word) because further chains are totally depend on this word.
class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field("This is sentiment of feedback")

# Create structured output using parser
pydanticParser = PydanticOutputParser(pydantic_object=Feedback)

# Now pass output instruction with this prompt template
prompt7 = PromptTemplate(
    template= """
    Classify the following customer feedback as either positive or negative.
    Feedback: {feedback}
    {format_instruction}
    """,
    input_variables=["feedback"],
    partial_variables={'format_instruction': pydanticParser.get_format_instructions()}
)

# prompt7 required this parser - pydanticParser
chain7 = prompt7 | model | pydanticParser

# below run chain7 to test only what will be the output
'''
result = chain7.invoke({'feedback': 'This smartphone is very poor and does not work properly, Dont buy this.'})


print('Sentiment is ', result)
# sentiment='negative'
'''

# positive feedback reply prompt
prompt8 = PromptTemplate(
    template="""
    The customer gave positive feedback: {feedback}
    Thank the customer warmly and encourage them to share
    their experience with others.
    """,
    input_variables=["feedback"]
    )

# negative feedback reply prompt
prompt9 = PromptTemplate(
    template="""
    The customer gave negative feedback: {feedback}
    Apologize politely and offer help resolving the issue.
    """,
    input_variables=["feedback"]
    )

conditional_chain = RunnableBranch(
        (lambda x: x.sentiment == 'positive', prompt8 | model | parser),
        (lambda x: x.sentiment == 'negative', prompt9 | model | parser),
        RunnableLambda(lambda x: "No sentiment found.")
)

# this default - (lambda x: "No sentiment found.") is not a chain and RunnableBranch only need chains so we can covert this to a chain using RunnableLambda.

final_chain = chain7 | conditional_chain

result = final_chain.invoke({'feedback': 'This smartphone is very poor and does not work properly, Dont buy this.'})

print('Feedback result ', result)
```
