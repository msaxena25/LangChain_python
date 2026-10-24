# Prompt Template

from langchain_core.prompts import PromptTemplate

# Create a prompt template with input variables, partial variables and validate template

prompt = PromptTemplate(
    template="Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.",
    input_variables=["yourName","companyName", "profileName"],
    partial_variables={"companyName": "Nagarro"},
    validate_template=True
)

print("Required Input variables:", prompt.input_variables) # ['profileName', 'yourName']
print("Default variables", prompt.partial_variables) #  {'companyName': 'Nagarro'}
print("Template format:", prompt.template_format) # Template format: f-string

print(prompt)
'''
input_variables=['profileName', 'yourName'] 
input_types={} 
partial_variables={'companyName': 'Nagarro'}
template='Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.'
validate_template=True
'''

print(type(prompt)) # <class 'langchain_core.prompts.prompt.PromptTemplate'>

#---------------------------------------------------------

# Create Prompt Template using from_template method

prompt_template = PromptTemplate.from_template("Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.")

# Prompt Template : invoke method

response = prompt_template.invoke({"yourName": "John", "companyName": "Nagarro", "profileName": "Software Engineer"})

print(response)

'''
text='Hello, I am John. I work in company Nagarro. My Current profile is Software Engineer. Based on my current profile, explain my next career roadmap.'
'''

# Prompt Template : format method - 

response: str = prompt_template.format(yourName="John", companyName="Nagarro", profileName="Software Engineer")
print(response)

'''
Use format() when you only need the final formatted string.

Use invoke() when working with LangChain's Runnable interface, such as passing a prompt into a model:
'''

#---------------------------------------------------------

# ChatPromptTemplate

# In ChatPromptTemplate, you generally need to define a message type or role for each message.

# ChatPromptTemplate — list of message templates

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate(
    messages=[
        ("system", "You are an expert in {technology}."),
        ("human", "Explain {topic}.")
    ],
    input_variables=["technology", "topic"],
    partial_variables={"technology": "web technologies"},
    validate_template=True
)

result = prompt.invoke({"topic": "React JS"})
print(result)

'''
Can you omit the role?

Not when using the tuple format ("role", "content"), because the first element defines the message type.

If you want a prompt without defining a chat role, use PromptTemplate instead:
'''

#---------------------------------------------------------

# ChatPromptTemplate — using from_messages() method

from langchain_core.prompts import ChatPromptTemplate

prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
    ("system", "You are expert in web technologies."),
    ("human", "Tell me about {technology}")
])

response = prompt.invoke({
    "technology": "React JS"
})


'''
ChatPromptTemplate([...]) is the direct constructor, while ChatPromptTemplate.from_messages([...]) is a named class method. 

Both can create the same kind of chat prompt.
'''


# When to use which template?

'''

- PromptTemplate: Use when you need a single text prompt. Commonly used with traditional text-completion LLMs.

- ChatPromptTemplate: Use when you need multiple messages with roles such as system, human, and assistant. Commonly used with chat models like Gemini, ChatGPT, and Claude.

Simple rule: For chat models, prefer ChatPromptTemplate. For a single text prompt, use PromptTemplate

'''

# Code Level Differeces - 

'''
PromptTemplate → from_template()
ChatPromptTemplate → from_messages()

PromptTemplate: have template property which is a string.
ChatPromptTemplate: have messages property which is a list of tuples.
'''