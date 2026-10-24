from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

#Load the environment variables
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Hugging Face Endpoint example
# repo_id: The ID of the model to use
# task: The task to perform
# model_kwargs: The kwargs to pass to the model

# For more details, refer to the Hugging Face documentation: https://huggingface.co/docs/api-inference/python/html/quick-start.html

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

result = model.invoke("Who is prime minister of India?")

print(result.content)