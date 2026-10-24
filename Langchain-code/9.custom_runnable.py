# Lets Break idea of runnables (Why LangChain introduced Runnables?) and problems which were earlier.

# Create Our Own Prompt Template, Runnable Class and Chain

from typing import Any
import random

# Lets Create Custom Prompt template same as langchain prompttemplate

'''
First Understand how LangChain PromptTemplate works:

LangChain PromptTemplate is called with `template` and `input_variables` and it has `format` method to 
format the template with input values.

`format` - Initially PromptTemplate only have this method.

So lets design same Our own Class.
'''

class MyPromptTemplate():
    def __init__(self, template: str, input_variables: list[str]):
            self.template = template
            self.input_variables = input_variables
            
    def format(self, input_values: list[str]):
        final_template = self.template.format(**input_values) # unpacking input values
        return final_template

prompt1 = MyPromptTemplate(template="Hello India, I live in {city}.", input_variables=["name"])
result2 = prompt1.format({'city':'Lucknow'})
print(result2)


# lets create a simple LLM Class

# this class have predict method that generate llm answer.

'''
Understand how LangChain LLM works:

LangChain LLM is called with prompt and it has predict method to generate llm answer.

`predict` - Initially LLM only have this method.

LangChain LLM Class called large language model (LLM) like OpenAI, GPT-4, etc and Get response from it.

So on same approach, lets design Our own LLM Class with static response.
'''

class MyCustomLLm():
    def __init__(self):
        print('My custom class called')
    
    def predict(self, prompt: MyPromptTemplate):
        return self.__getAnswer()
    
    def __getAnswer(self):
        answers_list = [
            'Delhi is capital of India',
            'Lucknow is capital of Uttar Pradesh',
            'Narendra Modi is prime minister of India.',
            'Bangloure is big IT tech city of India.'
        ]
        return {'content': random.choice(answers_list)}
    
myCustomLLmObj =  MyCustomLLm()
result1 = myCustomLLmObj.predict("Tell me about India.")
print(result1)


# Now lets pass prompt template to our custom LLM

result3 = myCustomLLmObj.predict(prompt1)
print(result3)

# Lets Create Chain class with above LLM or Model and Prompt template

# This Class will take MyPromptTemplate and MyCustomLLm as an arguments

'''
What Chain Class do?

Chain Class take prompt template and LLM as an arguments and it has run method to execute the chain.

`run` - Initially Chain only have this method.

'''

class MyCustomLLMChain():
    def __init__(self, prompt_template: MyPromptTemplate, llm: MyCustomLLm):
         self.prompt = prompt_template
         self.llm = llm
    
    def run(self, input_dict: list[str]):
        prompt = self.prompt.format(input_dict)
        result = self.llm.predict(prompt)
        return result['content']

llmObj = MyCustomLLm() # create LLM object
prompt2 = MyPromptTemplate(
            template="Hello India, I live in {city} and my name is {name}.",
            input_variables=["city", "name"]
            )
myChainObj = MyCustomLLMChain(prompt2, llmObj)
result4 = myChainObj.run({'city': 'Mumbai', 'name': 'Masava'})
print('output of chain - ', result4)

# _____________________________________

'''
So far, we've built an LLM class, a PromptTemplate class, and a Chain class. 

However, there's a lack of standardization — each component exposes different method names like `predict`
or `run`, making it difficult to sequence them together smoothly.

This inconsistency was an issue in older versions of LangChain too, since components were
developed independently and didn't adhere to a common interface. 

The result was that chaining different parts became difficult and confusing, especially 
as more chains and components were introduced and the framework grew more complex.

To address this and bring greater flexibility, the LangChain team decided to redesign 
the framework so that all parts follow a shared pattern with clear guidelines and similar interfaces.

This led to the introduction of "Runnables." 

Runnables standardize the structure and execution of these components.

Let's look at the basic idea behind a Runnable by defining a custom Runnable class. 

As a step toward standardization, we'll create an abstract base class called `Runnable`. 

All our main components—LLMs, prompt templates, and chains—will inherit from this, ensuring a 
consistent structure and interface.
'''

#------------------------------------------------

# Now - lets create Runnables Abstract class

from abc import ABC, abstractmethod

class Runnable(ABC):
    @abstractmethod
    def invoke(self, input_data: dict[str, Any]):
        pass
   

# Now lets inherit this Runnable Abstract Class into our LLM Class

'''
If we inherit Runnable Abstract Class into our LLM Class and not implement invoke method, we will get error - 

TypeError: Can't instantiate abstract class MyCustomLLm without an implementation for 
`invoke` abstract method.

So abstract method `invoke` is compulsory now.
'''

# Our Custom LLM Class that will inherit Runnable Abstract Class

class MyCustomLLm(Runnable):
    def __init__(self):
        print('My custom class called')
    
    def invoke(self, prompt):
            return self.__getAnswer()
    
    # Initially we can not remove this predict method because engineers who are using this predict method in their code, that will break
    # But we can print a depreciated warning message to developers.
    def predict(self, prompt):
        print('Warning: This predict method is now depreciated. use invoke() instead of this.')
        return self.__getAnswer()
    
    def __getAnswer(self):
        answers_list = [
            'Delhi is capital of India',
            'Lucknow is capital of Uttar Pradesh',
            'Narendra Modi is prime minister of India.',
            'Bangloure is big IT tech city of India.'
        ]
        return {'content': random.choice(answers_list)}
    

# PromptTemplate Class that will inherit Runnable Abstract Class

class MyPromptTemplate(Runnable):
    def __init__(self, template: str, input_variables: list[str]):
            self.template = template
            self.input_variables = input_variables
            
    def invoke(self, input_values: list[str]):
            final_template = self.template.format(**input_values)
            return final_template
    
    # Same here, we will print warning depreciated message to existing developer
    def format(self, input_values: list[str]):
        print('Warning: This predict method is now depreciated. use invoke() instead of this.')
        final_template = self.template.format(**input_values)
        return final_template

# Lets Create Runnable Connector Class - It will execute all runnables in a list

class RunnableConnector(Runnable):
    def __init__(self, runnable_list: list[Runnable]):
        print('Runnable Connector class created')
        self.runnable_list = runnable_list
    
    def invoke(self, input_data: dict[str, Any]):
        # Now loop on runnable_list and call invoke method of each runnable
        # Input of next runnable will be output of previous runnable, so we are updating input_data in each iteration.
        for runnable in self.runnable_list:
            input_data = runnable.invoke(input_data)
        return input_data     

# Now lets create object of our custom LLM and PromptTemplate and pass it to RunnableConnector

prompt_template1 = MyPromptTemplate(
            template="Hello India, I live in {city} and my name is {name}.",
            input_variables=["city", "name"]
            )

llmObj1 = MyCustomLLm()

runnable_chain = RunnableConnector([prompt_template1, llmObj1])

result5 = runnable_chain.invoke({'city': 'Mumbai', 'name': 'Masava'})

print('Runnable chain output ', result5)
# Runnable chain output  {'content': 'Delhi is capital of India'}

#------------------------------------------------

# Custom Parser Class that will inherit Runnable Abstract Class

'''
Now Lets Create our custom parser component

Its Job -  it will take input, parse its properties and return output in plain text format.

That Parser class will also inherit Runnable abstract class.
'''

class MyParser(Runnable):
    def __init__(self):
        pass
    def invoke(self, input_data: dict[str, Any]):
        return input_data.get('response') or input_data.get('content')

parser =  MyParser()

runnable_chain_2 = RunnableConnector([prompt_template1, llmObj1, parser])

result6 = runnable_chain_2.invoke({'city': 'Mumbai', 'name': 'Masava'})

print('Parsed output with parser ', result6)

# _____________________________________

# Now combine multiple chains with this RunnableConnector class

prompt_template2 = MyPromptTemplate(
    template="Hello, Write a poem about {topic}.",
    input_variables=["topic"]
    )
    
prompt_template3 = MyPromptTemplate(
    template="Now, based on above poem {content}.",
    input_variables=["content"]
    )

llmObj2 = MyCustomLLm()

runnable_chain_3 = RunnableConnector([prompt_template2, llmObj2])

runnable_chain_4 = RunnableConnector([prompt_template3, llmObj2])

# Now combine these two chains

final_chain = RunnableConnector([runnable_chain_3, runnable_chain_4, parser])

result7 = final_chain.invoke({'topic': 'Love'})
print('Combined chain output ', result7)