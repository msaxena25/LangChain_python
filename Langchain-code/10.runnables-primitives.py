from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# RunnableSequence is a primitive Runnable that executes components sequentially.
# It is a subclass of Runnable.
# It is used to execute components sequentially.

prompt1 = PromptTemplate.from_template("Hello {name}")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = RunnableSequence(prompt1, model)

'''
RunnableSequence is same as =>

chain = prompt1 | model
'''

#result = chain.invoke({"name": "John"})
#print(result)

#------------------------------------------------------------------------------------------------

# RunnableParallel is a primitive Runnable that executes components in parallel.
# It is a subclass of Runnable.
# It is used to execute components in parallel.

prompt1 = PromptTemplate.from_template("Write a summary of the following text: {text}")

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

summary_chain = RunnableSequence(prompt1, model)

prompt2 = PromptTemplate.from_template("Write a sentiment analysis of the following text: {text}")

sentiment_chain = RunnableSequence(prompt2, model)

'''
We can arguments into RunnableParallel in two ways:
1. Keyword arguments
2. Dictionary arguments

Keyword arguments are more readable and easier to understand.
Dictionary arguments are more flexible and can be used to build dynamic chains.
'''


# 1. Keyword arguments
#summary and sentiment are keyword argument names.
# Each keyword argument name becomes a key in the output dictionary.

parallel_chain = RunnableParallel(
    summary=summary_chain,
    sentiment=sentiment_chain
)

# We can also write the same above with passing a dictionary into RunnableParallel - but it's not recommended.

# 2. Dictionary arguments

#You explicitly pass a dictionary.
#The dictionary keys become the output keys.

# parallel_chain = RunnableParallel({"summary": summary_chain, "sentiment": sentiment_chain})

'''
There is no difference in functionality or output between these two approaches. 
Both pass a mapping of keys to Runnables into RunnableParallel.

My recommendation: Use keyword arguments when the keys are fixed and known in advance. Use a dictionary when the mapping is already stored in a variable or needs to be built dynamically.
'''


# uncomment to run
#result = parallel_chain.invoke({"text": "I love the product!"})
#print(result)
# {    "summary": "...",    "sentiment": "..."}

#------------------------------------------------------------------------------------------------

# RunnablePassThrough is a primitive Runnable that preserves the input as it is with the final output.

from langchain_core.output_parsers import StrOutputParser

chain = RunnableParallel(
    original=RunnablePassthrough(),
    lowercase=lambda text: text.lower()
)

result = chain.invoke("HELLO LANGCHAIN")

print(result)
# {    "original": "HELLO LANGCHAIN",    "lowercase": "hello langchain"}


# another working example

print('Test RunnablePassthrough with RunnableParallel...')

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=100, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )


prompt3 = PromptTemplate.from_template("Explain following topic: {topic}")

prompt4 = PromptTemplate.from_template("Write a summary of the following explanation: {explanation}")

parser = StrOutputParser()

# explaination generator chain
explanation_generator_chain = RunnableSequence(prompt3, model, parser)

# summary generator chain with preserve explanation_chain output as it is
parellel_chain = RunnableParallel(
    explanation=RunnablePassthrough(),
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

#result = final_chain.invoke({"topic": "AI"})

# print(result)
# {    "explanation": "AI is a technology that allows machines to learn from data and make decisions.",    "summary": "..."}

#------------------------------------------------------------------------------------------------

# RunnablePassthrough.assign()

# RunnablePassthrough.assign() is a method that assigns a value to a key in the output dictionary.

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

# uncomment to run
#result = chain.invoke({"topic": "Cricket"})

#print(result)
# {    "explanation": "Cricket is a sport that is played between two teams of 11 players each. The game is played on a field with a rectangular shape and a target called the wicket. The objective of the game is to score runs by hitting the ball with a bat and running between the wickets. The team with the most runs at the end of the game wins.",    "summary": "..."}

#------------------------------------------------------------------------------------------------

# RunnableBranch

'''
Suppose LLM generated report on any topic. You want to:

- If report's total words count are > 500 then again call LLM to write summary fo that report.
- If report's total words count are with in 500 then print report as it is.

'''

from langchain_core.runnables import RunnableBranch

print('Test RunnableBranch...')

# report generator prompt
report_generator_prompt = PromptTemplate.from_template("Generate a report on the following topic: {topic}")

# report generator chain
report_generator_chain = RunnableSequence(report_generator_prompt, model, parser)

# summary generator prompt
summary_generator_prompt = PromptTemplate.from_template("Write a summary of the following report: {report}")

# summary generator chain
summary_generator_chain = RunnableSequence(summary_generator_prompt, model, parser)

# Now create a branch chain

branch_chain = RunnableBranch(
    (lambda report: len(report.split()) > 500, summary_generator_chain),
    RunnablePassthrough() # if report's total words count are with in 500 then print report as it is.
)

# uncomment to run
#result = branch_chain.invoke({"topic": "Pollution in Delhi"})
#print(result)
# {    "summary": "...", "report": "..."}

#------------------------------------------------------------------------------------------------


# RunnableBranch - another example

'''

company's email-routing system. You want to:

The workflow will classify the incoming email into one of four departments:

- Complaint → Customer Support
- Refund or payment → Payment Team
- Technical issue → Technical Team
- General query → Chatbot handles it directly
'''

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

# test the final workflow chain

# uncomment to run
#result = final_workflow_chain.invoke({
#    "email": "I have a complaint about the product. Please refund the extra payment."
#})

#print(result)
# Customer Support Team

result = final_workflow_chain.invoke({"email": "Could you please tell me, how can I order the product?"})
print(result)
'''
 {'email': 'Could you please tell me, how can I order the product?', 'result': "Hello! Thank you for reaching out to us. \n\nI am our automated customer support assistant, and I'd be happy to help you today. Since your message falls under a general query, could you please provide a few more details or let me know what specific question you have about our products, services, or policies? \n\nOnce you share the details, I'll get you the right information right away!"}
'''

# Now understand steps one by one

'''
1. Creted email classification prompt and chain
    - with email input and standard format instructions
    - standard format instructions is used to parse the output into Pydantic Schema.
2. Created customer support team chain
3. Created payment team chain
4. Created technical team chain
5. 2,3,4 are the routing chains, we have to redirect that email to the respective team.
6. For general queries, we have to handle it directly & handle with llm chatbot.
    - created with same input email as it is.
    - it will handle the general query with llm chatbot.
7. So Created general query prompt and chain.
8. Now we created runnable branch chain, it will route the email to the respective team based on the email classification.
9. Finally we created final workflow chain with three components:
    - Used RunnablePassthrough.assign() to preserve the email input as it is.
    - email_classification_chain - it will classify the email into one of the four categories.
    - runnable_branch_chain - it will route the email to the respective team based on the email classification.
10. We tested the final workflow chain with a general query email.


'''