
# Google Gemini example
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
import os

load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(model='gemini-3.8-flash', google_api_key=GOOGLE_API_KEY)

result = model.invoke("Who is prime minister of India?")

print(result) # This will print the response from the LLM

'''
content=[{'type': 'text', 'text': 'The Prime Minister of India is **Narendra Modi**. He has been in office since May 2014.', 
'extras': {'signature': 'EocECoQEAWkUfROmLTIlE0dG4sGSUFdGrQuOlUmoMmkMfUBvpFdEv3FqBBTJ7eh6BGkAwVBgsyaVidvZWXfsjr78TZqM0FIN50dJqVpFfFBhO97flVAuPqoHCVWhvbrAoiHacj1dTNCt5PbniUO4diyeEJPvYuaf+wCBda3ifT9+kyUJGd9PJTa8bWw2hv5M2lvybafvMR0akaA3O1QZh3vluxxldancTvsZnYXguCwqez/EC/Rf/burg0G5Qm9tXBSbHuEX8thRIS47t/urKBCuXTsEY5ATXx9Qqj9KbjwuK2o1Gsv0zNA6axRfKURGLeOqhpXtHRaQ4JWg7VgcqhrcB1qvsfDwFTF3WlN5taMpcbBmt5FLFGlMCdj6717rXjexK+LYOifeYojIuHtEzdu4SUw3b6MXDNqf7H8eHfcn9NYyZAatyDi84nFqwLlfHGhOn4LAx65ZQLbzG7Y4Wi4166KvsOyaIroCedp16SM79g37CLcMSgqmLgz8Up7KKP/HOo5Xe62GnObTtXZRj3/JkYWOtrfSN8edxdY6yBQ/X3CFI4TYWSL+gKddeqXABfvHhbsKluhI2ifen7SwK8K8Z2V/FnksVj7hPQ1ecNRnDoz5cFPFu+IB2jEnR1HtuvT0EBQnsZQg08U8WcgCLVlm9Fbxb5T4o7H79INaX25MfqnNwr2SJaPH'}}] 
additional_kwargs={} response_metadata={'finish_reason': 'STOP', 'model_name': 'gemini-3.8-flash', 'safety_ratings': [], 
'model_provider': 'google_genai'} id='lc_run--01a12f71-b0d0-7540-b5c3-a227630b2bec-0' tool_calls=[] invalid_tool_calls=[] 
usage_metadata={'input_tokens': 8, 'output_tokens': 134, 'total_tokens': 142, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 110}}
'''

#-----------------------------------------------------------

# Use of embedding Model ( model.embed_query )

from langchain_google_genai import GoogleGenerativeAIEmbeddings

model = GoogleGenerativeAIEmbeddings(model='gemini-3.8-flash', google_api_key=GOOGLE_API_KEY)

result = model.embed_query("Who is prime minister of India?")

print(result) # This will print the Embedding of above query

#-----------------------------------------------------------

# Use of embedding Model with dimensions

model = GoogleGenerativeAIEmbeddings(
    model='gemini-3.8-flash',
    dimensions=32,
    google_api_key=GOOGLE_API_KEY)

result = model.embed_query("Who is prime minister of India?")

print(result)

#-----------------------------------------------------------

# Use of embedding Model with documents (model.embed_documents)

documents = [
    "Angular is a frontend framework.",
    "React is a JavaScript UI library.",
    "RAG retrieves relevant information for an LLM."
]

vectors = model.embed_documents(documents)

print(vectors) # This will print the vector response

#-----------------------------------------------------------

# output_dimensionality

# output_dimensionality is the number of dimensions to return for each document.

model = GoogleGenerativeAIEmbeddings(
    model='gemini-3.8-flash',
    output_dimensionality=32,
    google_api_key=GOOGLE_API_KEY)

result = model.embed_query("Who is prime minister of India?")

print(result) 

#-----------------------------------------------------------

# use of coshine similarity

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


documents = [
    "Angular is a frontend framework.",
    "React is a JavaScript UI library.",
    "RAG retrieves relevant information for an LLM."
]

user_query = "What is Angular?"

vectors = model.embed_documents(documents)
print(vectors)

user_vector = model.embed_query(user_query)
print(user_vector)

# use of cosine similarity

similarity = cosine_similarity([user_vector], vectors)

print(similarity)
# output = [[0.99999994, 0.767888, 0.22517]]
# This is like array inside array means list so we can take [0] here.

# Pair each score with its index
results = list(enumerate(similarity[0]))
# output = [(0, 0.767888), (1, 0.22517), (2, 0.767888)]

# Sort by score in descending order
sorted_results = sorted(
    results,
    key=lambda item: item[1],
    reverse=True
)
# output = [(0, 0.767888), (1, 0.22517), (2, 0.767888)]

# Fetch the most relevant item
best_index, best_score = sorted_results[0]
# output: best_index = 0, best_score = 0.767888

print(best_index)

print('Similarity Score: ', best_score)
print('Most relevant item: ', documents[best_index])
