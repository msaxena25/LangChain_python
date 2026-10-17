# Lets Break idea of runnables and problems which were earlier.

# lets create a simple LLM Class
# this class have predict method that generate llm answer.

import random

class MyCustomLLm():
    def __init__(self):
        print('My custom class called')
    
    def predict(self, prompt):
        return self.__getAnswer()
    
    def __getAnswer(self):
        answers_list = [
            'Delhi is capital of India',
            'Lucknow is capital of Uttar Pradesh',
            'Narendra Modi is prime minister of India.'
            'Bangloure is big IT tech city of India.'
        ]
        return {'content': random.choice(answers_list)}
    
myCustomLLmObj =  MyCustomLLm()
result1 = myCustomLLmObj.predict("Tell me about India.")
print(result1)

# Lets Create Custom Prompt template same as langchain prompttemplate
class MyPromptTemplate():
    def __init__(self, template: str, input_variables: list[str]):
            self.template = template
            self.input_variables = input_variables
            
    def format(self, input_values: list[str]):
        final_template = self.template.format(**input_values)
        return final_template

prompt1 = MyPromptTemplate(template="Hello India, I live in {city}.", input_variables=["name"])
result2 = prompt1.format({'city':'Lucknow'})
print(result2)

# Now lets pass this prompt to our custom LLM
result3 = myCustomLLmObj.predict(prompt1)
print(result3)

# Lets Create now Chain class with above LLM or Model and Prompt template
# This Class will take MyPromptTemplate and MyCustomLLm as an arguments

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
Till Now we have created LLM, PromtTemplate and Chain class, But if we see, all these 3 are not standarised,
We cannot call chain multiple times in sequence because We have different different methods like predict, run etc..

And that was a problem in older langchain code as well because every part or class of Lang Chain is created by different different developers or teams and that's why for each class and components, methods are different, they are not accepted from a single structure.

And by that time when Langchain Introduced multiple chains, its code became very complex For AI engineer.

To solve this problem and to make flexible of Lang Chain framework, Its team decided to restructure its complete code base that will follow a same structure, common guidelines and a common pattern.

And then they introdcued Runnables.

So now, Lets see basic idea of runnable by creating Custom Runnable Class.

So First we need to make our above solution more standarised so that It could be Flexible enough and follow a common structure.

And for that we will create a Abstract Class named Runnable that will be inherited by all these classes.
'''

# Now - lets create Runnables Abstract class

from abc import ABC, abstractmethod

class Runnable(ABC):
    @abstractmethod
    def invoke(input_data: list[str]):
        pass
    

# Now lets inherit this Runnable Abstract Class into our LLM Class

'''
And now If we create object with initializing abstract method, we will get error - 

TypeError: Can't instantiate abstract class MyCustomLLm without an implementation for abstract method 'invoke'

So abstract method invoke is compulary now.
'''

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
            'Narendra Modi is prime minister of India.'
            'Bangloure is big IT tech city of India.'
        ]
        return {'content': random.choice(answers_list)}
    

# Now Inherit this Runnable abstract class into PromptTemplate class as well to follow a common structure.

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
    
# Now the heart part of this - Create a Runnable Connector Class
# This will take all runnables in its parameter which we need to execute in a list

class RunnableConnector(Runnable):
    def __init__(self, runnable_list):
        print('Runnable class created')
        self.runnable_list = runnable_list
    
    def invoke(self, input_data):
        # Now loop on runnable_list and call invoke method of each
        # Second important thing - Input of next runnable will be output of previous runnable, so we are updating input_data in each iteration.
        for runnable in self.runnable_list:
            input_data = runnable.invoke(input_data)
        
        return input_data     
    
llmObj1 = MyCustomLLm()
prompt_template1 = MyPromptTemplate(
            template="Hello India, I live in {city} and my name is {name}.",
            input_variables=["city", "name"]
            )
runnable_chain = RunnableConnector([prompt_template1, llmObj1])

result5 = runnable_chain.invoke({'city': 'Mumbai', 'name': 'Masava'})
print('Runnable chain output ', result5)