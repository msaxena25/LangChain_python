
# Requirement

'''
Objective: Build a YouTube chatbot using `Retrieval-Augmented Generation (RAG)` that answers user questions based on a YouTube video's transcript.

The application will follow these steps:

1. Fetch transcript: Extract the transcript using a YouTube video ID.
2. Text splitting: Use `RecursiveCharacterTextSplitter` with a chunk size of 1,000 characters and a chunk overlap of 200 characters.
3. Create vector store: Generate embeddings for the transcript chunks and store them in FAISS.
4. Create retriever: Configure a retriever to find relevant transcript chunks.
5. Retrieve context: Accept a user question and retrieve the closest matching chunks.
6. Initialize the LLM: Create a Gemini chat model object.
7. Prompt construction: Create a prompt template containing the retrieved context and user's question.
8. Generation: Pass the constructed prompt to Gemini to generate an answer grounded in the transcript.
9. Single invocation: Connect the steps into a LangChain chain so the complete RAG workflow can be executed using a single `.invoke()` call.

Expected result: The user asks a question about the video and receives an answer based on its transcript, without manually invoking each step separately.
'''

# Required packages -

'''
```
pip install -U langchain langchain-community langchain-google-genai langchain-text-splitters faiss-cpu youtube-transcript-api python-dotenv
```
'''

# We'll use:

'''
- `YouTubeTranscriptApi` to fetch the transcript.
- `RecursiveCharacterTextSplitter` to split the transcript.
- `GoogleGenerativeAIEmbeddings` to convert chunks into vectors.
- `FAISS` to store and search those vectors.
- `as_retriever()` to retrieve relevant chunks.
- `ChatGoogleGenerativeAI` and `PromptTemplate` to generate the answer.
- LangChain's Runnable components to connect everything into one chain.
'''

from langchain_core.documents.base import Document
from youtube_transcript_api._transcripts import FetchedTranscript
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
import os

load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# embedding model
embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001", google_api_key=GOOGLE_API_KEY)

# LLM Model

llm_model = ChatGoogleGenerativeAI(
     model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    max_output_tokens=500,
    max_retries=2,
    timeout=20
)


# Fetch the YouTube transcript

# Wr are using direct YouTubeTranscriptApi to load transcript instead of youtube loader

# https://www.youtube.com/watch?v=7aEAS5E5vjg
VIDEO_ID = "7aEAS5E5vjg"

try:
    youtube_api_obj = YouTubeTranscriptApi()
    video_transcipt: FetchedTranscript = youtube_api_obj.fetch(VIDEO_ID)
    print('Video transcript..')
    # print(video_transcipt.snippets)
    
except TranscriptsDisabled:
    print('Error: Transcript disabled for this Video OR no caption found.')

# Transcript Full response -    

'''
[FetchedTranscriptSnippet(text='Once upon a time there lived a man in a', start=0.4, duration=5.04), FetchedTranscriptSnippet(text='small village. He was very worried about', start=2.879, duration=6.081), FetchedTranscriptSnippet(text='his son. His son was lazy and careless.', start=5.44, duration=6.159), FetchedTranscriptSnippet(text='He never worked. He just wandered here', start=8.96, duration=5.12), FetchedTranscriptSnippet(text='and there in the village all day long.', start=11.599, duration=5.201), FetchedTranscriptSnippet(text='Oneday the man decided to teach his son', start=14.08, duration=6.16), FetchedTranscriptSnippet(text='a lesson.He called his son to him. He', start=16.8, duration=7.04), FetchedTranscriptSnippet(text='said gently, "Son,there is a watch kept', start=20.24, duration=6.32), FetchedTranscriptSnippet(text='inside the cupboard. Bring it to me."', start=23.84, duration=5.199), FetchedTranscriptSnippet(text='The boy went and opened the cupboard. He', start=26.56, duration=4.559), FetchedTranscriptSnippet(text='took out the watch and came back to his', start=29.039, duration=4.401), FetchedTranscriptSnippet(text='father. The father looked at the watch', start=31.119, duration=5.201), FetchedTranscriptSnippet(text='and then said, "Now take this watch to', start=33.44, duration=5.76), FetchedTranscriptSnippet(text='the market. Ask everyone you meet how', start=36.32, duration=5.36), FetchedTranscriptSnippet(text='much they think it is worth." The boy', start=39.2, duration=4.56), FetchedTranscriptSnippet(text='nodded and went to the market with the', start=41.68, duration=4.64), FetchedTranscriptSnippet(text='watch. He showed the watch to different', start=43.76, duration=5.92), FetchedTranscriptSnippet(text='people. One man said it was worth 500', start=46.32, duration=7.44), FetchedTranscriptSnippet(text='rupees. Another said 1,000. Someone else', start=49.68, duration=7.12), FetchedTranscriptSnippet(text='said 800. Everyone gave a different', start=53.76, duration=6.0), FetchedTranscriptSnippet(text='price. Some people even gave the same', start=56.8, duration=6.399), FetchedTranscriptSnippet(text='price, but no oneagreed completely. The', start=59.76, duration=6.399), FetchedTranscriptSnippet(text='boy came back home andsaid, "Father,', start=63.199, duration=4.881), FetchedTranscriptSnippet(text='everyone told me a different price for', start=66.159, duration=6.081), FetchedTranscriptSnippet(text='the watch." Some said 500, some said', start=68.08, duration=8.399), FetchedTranscriptSnippet(text='800, and some said 1,000. The man smiled', start=72.24, duration=7.28), FetchedTranscriptSnippet(text='and said, "All right, put the watch back', start=76.479, duration=5.761), FetchedTranscriptSnippet(text='in the cupboard." The next day, the man', start=79.52,duration=5.12), FetchedTranscriptSnippet(text='called his son again. He asked him to', start=82.24, duration=4.96), FetchedTranscriptSnippet(text='bring the same watch. The boy brought it', start=84.64, duration=4.799), FetchedTranscriptSnippet(text='and gave it to his father. Then the', start=87.2, duration=4.559), FetchedTranscriptSnippet(text='father said, "Now go to the market', start=89.439, duration=5.521), FetchedTranscriptSnippet(text="again. This time don't ask the price of", start=91.759, duration=5.68), FetchedTranscriptSnippet(text='the watch. Ask people the price of the', start=94.96, duration=5.44), FetchedTranscriptSnippet(text='time inside this watch." The boy was', start=97.439, duration=5.521), FetchedTranscriptSnippet(text="confused.He didn't understand what his", start=100.4, duration=5.6), FetchedTranscriptSnippet(text='father really meant. Still, he obeyed', start=102.96, duration=5.439), FetchedTranscriptSnippet(text='and went to the market again. He asked', start=106.0, duration=4.88), FetchedTranscriptSnippet(text='the people he met, "How much is the time', start=108.399, duration=4.881), FetchedTranscriptSnippet(text='inside this watch worth?" People looked', start=110.88, duration=5.519), FetchedTranscriptSnippet(text='at him strangely. Some laughed at him.',start=113.28, duration=6.159), FetchedTranscriptSnippet(text='Some told him to go away. Some said,', start=116.399, duration=5.921), FetchedTranscriptSnippet(text='"What a foolish question." The boy felt', start=119.439, duration=5.921), FetchedTranscriptSnippet(text='embarrassed and sad. Finally, he stopped', start=122.32, duration=5.2), FetchedTranscriptSnippet(text='at a small shop where an old man was', start=125.36, duration=4.959), FetchedTranscriptSnippet(text='working. The old shopkeeper was busy', start=127.52, duration=5.2), FetchedTranscriptSnippet(text='repairing watches. When the boy asked', start=130.319, duration=4.56), FetchedTranscriptSnippet(text='him the same question, the old man', start=132.72, duration=4.4), FetchedTranscriptSnippet(text='paused his work. He looked at the boy', start=134.879, duration=5.121), FetchedTranscriptSnippet(text='with a kind smile. He understood what', start=137.12, duration=5.36), FetchedTranscriptSnippet(text='the boy was trying to ask. He said', start=140.0, duration=6.16), FetchedTranscriptSnippet(text='softly, "Son, youcannot put a price on', start=142.48, duration=6.479), FetchedTranscriptSnippet(text='time. You can give millions of rupees,', start=146.16, duration=5.12), FetchedTranscriptSnippet(text='but you cannot buy back even one second', start=148.959, duration=5.121), FetchedTranscriptSnippet(text='of your life. That is why you must use', start=151.28, duration=5.44), FetchedTranscriptSnippet(text='your time wisely." The boy listened', start=154.08, duration=6.0), FetchedTranscriptSnippet(text='carefully. The old man continued, "Time', start=156.72, duration=6.0), FetchedTranscriptSnippet(text='has one bad thing and one good thing.', start=160.08, duration=5.68), FetchedTranscriptSnippet(text='The bad thing is it passes. The good', start=162.72, duration=6.32), FetchedTranscriptSnippet(text='thing is you can choose how to spend it.', start=165.76, duration=5.92), FetchedTranscriptSnippet(text='Everyone in this world has 24 hours in a', start=169.04, duration=5.52), FetchedTranscriptSnippet(text='day. The rich and the poor both. The', start=171.68, duration=5.279), FetchedTranscriptSnippet(text='difference is how they use those hours.', start=174.56, duration=4.16), FetchedTranscriptSnippet(text="The boy's eyes filled with", start=176.959, duration=4.721), FetchedTranscriptSnippet(text='understanding. Something changed inside', start=178.72, duration=5.76), FetchedTranscriptSnippet(text='him. He thanked the old man and went', start=181.68, duration=5.279), FetchedTranscriptSnippet(text='home quickly. He toldhis father', start=184.48, duration=4.24), FetchedTranscriptSnippet(text='everything that had happened in the', start=186.959, duration=4.961), FetchedTranscriptSnippet(text='market. The man smiled with pride and', start=188.72, duration=5.92), FetchedTranscriptSnippet(text="placed his hand on his son's shoulder.", start=191.92, duration=6.08), FetchedTranscriptSnippet(text="From that day on, the boy's life changed", start=194.64, duration=6.64), FetchedTranscriptSnippet(text='completely. He started working hard. He', start=198.0, duration=6.4), FetchedTranscriptSnippet(text='began using his time wisely. He stopped', start=201.28, duration=5.76), FetchedTranscriptSnippet(text='wasting his days wandering around. He', start=204.4, duration=4.72), FetchedTranscriptSnippet(text='understood the real value of every', start=207.04, duration=5.279), FetchedTranscriptSnippet(text='moment. Friends, time is free for', start=209.12, duration=6.399), FetchedTranscriptSnippet(text='everyone. But it is priceless. You', start=212.319, duration=6.64), FetchedTranscriptSnippet(text='cannot buy it, but you can use it. You', start=215.519, duration=6.481), FetchedTranscriptSnippet(text='cannot keep it, but you can spend it.', start=218.959, duration=5.2), FetchedTranscriptSnippet(text='Once it is gone, youcan never get it', start=222.0, duration=7.04), FetchedTranscriptSnippet(text='back. So use your time wisely.', start=224.159, duration=4.881)]
'''

# You can print snippet text only using for loop

'''
for snippet in video_transcipt.snippets:
    print(snippet.text)
'''

# Below is another way to load transcript using YoutubeLoader
'''
from langchain_community.document_loaders import YoutubeLoader

loader = YoutubeLoader(
    video_id=VIDEO_ID,
    language=["en"]
)

documents = loader.load()
'''

# Now Join all transcript text into one full string

transcript_full_string: str = " ".join(snippet.text for snippet in video_transcipt.snippets)

# Now lets split this text into chunk

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)

# create_documents() creates the chunked chunks of Document Object.
documents: list[Document] = text_splitter.create_documents([transcript_full_string])

print("Total documents:", len(documents))

# Now Generate Embedding and store in FAISS vector store

vector_store: FAISS = FAISS.from_documents(
    documents=documents, 
    embedding=embedding_model
    )

# Now Create Retriever

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 6})

# You can simply call below to just see what relevent chunks it returns based on query
# retriever.invoke('What lession Father wanted to teach his Son?')

# Now Augumentation part

prompt_template = PromptTemplate(
    template='''You are a YouTube video assistant.
    Provide answer based on given context only.
    If the answer is not available in the context, say:
    "I couldn't find the answer in this video's transcript."
    
    Context: {context}
    User Question: {question}
    ''',
    input_variables=['context', 'question']
    )

parser = StrOutputParser()

# Retrievers return list of document so format those docs into simple plain text
format_retrieved_docs = lambda retrieved_docs: " ".join(doc.page_content for doc in retrieved_docs) 

'''

You don't need to convert your lambda function into RunnableLambda explicitly in this case because LangChain's LCEL automatically converts a regular function or lambda into a RunnableLambda when you use the | pipe operator.
'''

context_chain: RunnableParallel[str] = RunnableParallel({
    'question': RunnablePassthrough(),
    'context': retriever | format_retrieved_docs
})

chain = context_chain | prompt_template | llm_model | parser

'''
Steps to build chain - 

1. Prompt template needs question and context as input.
2. Context comes from retriever.
3. So to build a chain we need to keep retriever before prompt_template
4. retriever by default only returns single result and that will go to prompt_template as input
5. But prompt_template also need question, so we need to return that question from retriever only
6. Thats why we have used  'question': RunnablePassthrough(), so that with context, retriever also preserve question.

'''

# Suppose If we need question in final answer as well

final_chain = RunnableParallel({
    "question": RunnablePassthrough(),
    "answer": chain
})

'''
result = final_chain.invoke({'question': 'What lession Father wanted to teach his Son?'})
'''

result = final_chain.invoke('What lession Father wanted to teach his Son?')
print(result)
'''
- Below Answer came with chunk_size = 200 and overlapping = 50 and k = 5

{'question': 'What lession Father wanted to teach his Son?', 
'answer': 'Based on the provided context, the man decided to "teach his son a lesson" by having him bring a watch from the cupboard and then go to the market to ask people "the price of the time inside this watch." \n\nHowever, the text does not explicitly explain the deeper moral or meaning of the lesson (as the son is only described as being confused and not understanding what his father really meant).'}

- Below Answer came with chunk_size = 500 and overlapping = 80 and k = 6
- And this result is more relevent to question. 
- We need to take care of proper chunk size and overlapping value.

{'question': 'What lession Father wanted to teach his Son?', 'answer': 'Based on the provided context, the father wanted to teach his son about the real value of time, helping him understand that "you cannot put a price on time," that you cannot buy back even one second of your life, and that he must use his time wisely instead of being lazy and careless.'}
'''