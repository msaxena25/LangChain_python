from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.",
    input_variables=["yourName","companyName", "profileName"],
    partial_variables={"companyName": "Nagarro"},
    validate_template=True
)

print("Required Input variables:", prompt.input_variables) # ['profileName', 'yourName']
print("Default variables", prompt.partial_variables) #  {'companyName': 'Nagarro'}
print("Template format:", prompt.template_format) # Template format: f-string

# print(prompt)
'''
input_variables=['profileName', 'yourName'] input_types={} partial_variables={'companyName': 'Nagarro'} template='Hello, I am {yourName}. I work in company {companyName}. My Current profile is {profileName}. Based on my current profile, explain my next career roadmap.'validate_template=True
'''

print(type(prompt)) # <class 'langchain_core.prompts.prompt.PromptTemplate'>