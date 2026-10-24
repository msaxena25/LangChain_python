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