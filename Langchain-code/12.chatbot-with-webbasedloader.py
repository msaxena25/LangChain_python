# Create Chatbot with document loader
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import WebBaseLoader

from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=100, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )

# First load a web page for which user want to ask some question

url = "https://www.flipkart.com/realme-p4x-5g-matte-silver-128-gb/p/itm575b1540859e4?pid=MOBHN7A8HYC9BPAU&param=098654&BU=Mobile&pageUID=1792410552143"
loader = WebBaseLoader(url)

docs = loader.load() # it will return list

doc_content = docs[0].page_content

# create prompt template

prompt_template = PromptTemplate(
    template="""You are good to provide answers based on provided content.
     So Answer the following question {question} from the following content.
     Content: {content}
    """,
    input_variables=['question', 'content']
)

parser = StrOutputParser()

# create chain

# RunnablePassthrough.assign() keeps the input dictionary and adds the model answer as a new key.
#  Put it around the existing chain so the prompt still receives both question and content.

chain = RunnablePassthrough.assign(
    answer=prompt_template | model | parser
)

# NOTE - You cannot preserve only single input like 'question' from input values 
# content stays too, because assign() keeps every key from the input. 


# invoke

output = chain.invoke({
    'question': 'What is product name and its price?',
    'content': doc_content
})

# To print only the question and the answer:

print(output["question"])
# What is product name and its price?

print(output["answer"])
'''
Based on the provided content, here is the product name and its price:

* **Product Name:** realme P4x 5G (Matte Silver, 128 GB)
* **Price:** 
  * BBD price: ₹22,999*
  * Listed prices also include: ₹29,999 (with various promotional/discounted prices shown such as ₹28,499 depending on
'''

