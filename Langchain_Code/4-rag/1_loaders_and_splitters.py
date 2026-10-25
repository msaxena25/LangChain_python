'''
A `Document Loader` is a `component` that reads data from a source and converts it into LangChain 
`Document` objects so that the data can be processed in a consistent way.
'''


# Load txt file with document loader

from langchain_community.document_loaders import TextLoader

print('laod txt file with TextLoader..')

loader = TextLoader("test-document/notes.txt")

result1 = loader.load()
print(result1)

# Every type of loader will return a list of Document objects.

'''
[Document(
metadata={'source': 'test-document/notes.txt'}, 
page_content='Hello Python\nLearning AI\n\n\n19-10\n12.30 se start  1:30\n2:10 start '
)]
'''

print(result1[0].page_content)
print(result1[0].metadata) # {'source': 'test-document/notes.txt'}

#--------------------------------------------

# Load pdf file with PyPDF Loader

from langchain_community.document_loaders  import PyPDFLoader

print('PyPDFLoader..')

loader = PyPDFLoader("test-document/test-pdf.pdf")

result1 = loader.load()
print(result1[0].page_content)

print(result1[0].metadata)
'''
{'producer': 'Microsoft® Word for Microsoft 365', 
'creator': 'Microsoft® Word for Microsoft 365', 
'creationdate': '2026-10-19T14:15:44+05:30', 
'author': 'Mohit Saxena', 
'moddate': '2026-10-19T14:15:44+05:30', 
'source': 'test-document/test-pdf.pdf', 
'total_pages': 4, 'page': 0, 'page_label': '1'}
'''

'''
By default, `PyPDFLoader` generally creates one document per PDF page. 
The metadata includes the source and page number.
'''

#-------------------------------------------------

# Load multiple txt file from Directory with Directory Loader

print('Load multiple txt file from Directory with Directory Loader...')

'''
DirectoryLoader is used to load multiple files from a directory (folder) instead
of loading each file individually.

DirectoryLoader does not itself extract every file format. 
It finds the files, then delegates each file to the loader you specify through `loader_cls`.
'''

from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "test-document/", 
    glob="*.txt",  # glob is pattern to match the files.
    loader_cls=TextLoader # Loader that will actually load that file.
    )

docs = loader.load()

print("Total documents:", len(docs))
print(docs[0].page_content)
print(docs[0].metadata)



# Load multiple pdf file from Directory with Directory Loader

print('Load multiple txt file from Directory with Directory Loader...')

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path= "test-document/", 
    glob="*.pdf", 
    loader_cls=PyPDFLoader
    )

docs = loader.load()

print("Total documents:", len(docs)) # 5

# the resulting document count generally corresponds to the total number of PDF pages, 
# not the number of PDF files.

print(docs[5].page_content) #IndexError: list index out of range
print(docs[5].metadata) #IndexError: list index out of range

#-----------------------------

# Lazy Load

'''
- load document on demand
- return a `generator` of document object.
- Documents are not loaded at once, they are fetched one at a time as needed.
- Use when dealing with large number of documents or you want stream processing (chunking, embedding) without using lots of memory.
'''

print('lazy_laod()...')

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path= "test-document/", 
    glob="*.pdf", 
    loader_cls=PyPDFLoader)

docs = loader.lazy_load()

print(docs) # <generator object DirectoryLoader.lazy_load at 0x0000023FB3584D30>

# use for loop on this docs object & it will print once doc loaded
for doc in docs:
    print(doc.metadata)
    


#----------------------------------------------------

# Web based loader

'''
A web-based document loader fetches content from a webpage and converts the extracted content 
into LangChain `Document` objects.
'''

print('Web based loader.....')

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://www.samsung.com/in/smartphones/galaxy-m/galaxy-m17e-5g-blitz-blue-128gb-sm-m076blbbins/buy/?cid=in_pd_pmax_google_galaxy-m17_ongoing_m17-26-pmax-pla-lti-pfm_pla_product-kv_1ur-590041l-2026&utm_source=google&utm_medium=paid&utm_campaign=-23678709337--&utm_term=&gad_source=1&gad_campaignid=23678725111&gbraid=0AAAAADm5iQUPnjurkKf9HIX1pa43AzyUa&gclid=CjwKCAjw_9bWBhBGEiwAomyTImlNLfEsEMK4Nqt4l_gMIdrziwLYRsY-dfN9qZJAPOamdLqB6DJSrRoCK0AQAvD_BwE')

doc = loader.load()

print(doc[0].page_content)

print(doc[0].metadata)



#--------------------------------------------

# CSV Loader

'''
`CSVLoader` is a LangChain document loader that reads a CSV file and converts its rows into LangChain 
`Document` objects.
'''

print('CSV Loader..')

from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("test-document/test-csv.csv", metadata_columns=['id'])
# metadata_columns is used to specify the columns that will be used as metadata.

file = loader.load()

print("Total documents:", len(file))

print(file[0].page_content)
# id: 101
# name: Mouse
# description: Wireless mouse
# price: 799

print(file[0].metadata)

'''
Step-by-step process of CSVLoader:

1. CSVLoader reads the CSV file using CSV-reading logic.
2. It identifies the column headers: id, name, description, and price.
3. It reads the first data row and matches each value with its column name.
4. It formats each column-value pair as `column: value` on a `separate line`.
5. It stores that formatted text in Document.page_content
'''


for row in file:
    line = row.page_content.splitlines() 
    print(line)
    # ['id: 101', 'name: Mouse', 'description: Wireless mouse', 'price: 799']
   
# print only name field of each row
 
for row in file:
    line = row.page_content.splitlines()
    for item in line:
        if item.startswith('name:'):
            print(item)
# name: Mouse
# name: Keyboard
# name: Monitor



#----------------------------------------------

# TEXT splitter 

'''
A `Text Splitter` is a `component` that splits text into smaller chunks.
'''

# package used - langchain-text-splitters

print('Text splitter....')

from langchain_text_splitters import RecursiveCharacterTextSplitter

# The most commonly used splitter is `RecursiveCharacterTextSplitter`.

'''
**Its default separator order is:**

`\n\n` - 1. Paragraphs - Try splitting at blank lines.

`\n` - 2. Lines - If still too large, try newlines.

`" "` - 3. Words - If still too large, try spaces.

`""` - 4. Characters - As a last resort, split between characters.
'''

text = '''
Python is a programming language.
It is widely used for AI and machine learning.
LangChain helps developers build applications with LLMs.
Text splitting is an important step in RAG.
'''

# we didn't pass any configurations here, lets see output - 
splitter = RecursiveCharacterTextSplitter()

# to split a string we use split_text method
chunks = splitter.split_text(text)

# print(chunks) # it just return single chunk with whole string.
'''
['Python is a programming language.\nIt is widely used for AI and machine learning.\nLangChain helps 
developers build applications with LLMs.\nText splitting is an important step in RAG.']

'''

# Lets pass some configurations to the splitter.

'''
chunk_size: The size of each chunk in characters.
chunk_overlap: The number of characters to overlap between chunks.
'''

print('RecursiveCharacterTextSplitter with chunk size more then text length..')

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50 # tries to retain 50 characters from the preceding chunk where applicable.
)
chunks = splitter.split_text(text)

# print(chunks) 
# We did chunk size 1000 and that is more then our text length so it will return only one chunk.

'''
['Python is a programming language.\nIt is widely used for AI and machine learning.\nLangChain 
helps developers build applications with LLMs.\nText splitting is an important step in RAG.']
'''

# Chunk size 50

print('RecursiveCharacterTextSplitter with chunk size 50..')

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=20 # tries to retain 20 characters from the preceding chunk where applicable.
)
chunks = splitter.split_text(text)

print(type(chunks)) # <class 'list'>
# print(chunks)

'''
Outputs with different chunk_overlap values:

chunk_overlap = 0 or 5

['Python is a programming language.', 'It is widely used for AI and machine learning.', 
'LangChain helps developers build applications', 
'with LLMs.', 'Text splitting is an important step in RAG.']

# below with chunk_overlap = 20

['Python is a programming language.', 'It is widely used for AI and machine learning.', 
'LangChain helps developers build applications', 'build applications with LLMs.', 
'Text splitting is an important step in RAG.']

with chunk_overlap = 30

['Python is a programming language.', 'It is widely used for AI and machine learning.', 
'LangChain helps developers build applications', 'developers build applications with LLMs.', 
'Text splitting is an important step in RAG.']

'''

for index, chunk in enumerate(chunks, start=1):
    print(index, chunk)
'''
1 Python is a programming language.
2 It is widely used for AI and machine learning.
3 LangChain helps developers build applications
4 build applications with LLMs.
5 Text splitting is an important step in RAG.
'''


#--------------------------------------------------

# PDF file splitter

print('PDF file splitter into chunks..........')

# use of split_document method

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('test-document/test-pdf-2.pdf')

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100, chunk_overlap=20)

chunks = splitter.split_documents(docs)

print('total document objects', len(docs)) #1
print('total chunks', len(chunks)) # 5

for index, chunk in enumerate(chunks, start=1):
    print(index, chunk.page_content)

'''
1 Important methods and options 
• load() — loads all matching documents into a list.
2 • lazy_load() — yields documents progressively.
3 • recursive=True — searches subdirectories recursively.
4 • show_progress=True — displays a progress bar; you may need tqdm installed.
5 • silent_errors=True — skips files that fail to load instead of stopping at the first 
'''



#-----------------------------------------------

# CharacterTextSplitter

print('CharacterTextSplitter.......')

# `CharacterTextSplitter` splits text using one specific separator that you choose.

from langchain_text_splitters import CharacterTextSplitter

text = '''
Python is a programming language.

It is widely used for AI and machine learning.

LangChain helps developers build applications with LLMs.
'''

splitter = CharacterTextSplitter(
    separator="\n\n", # — a blank line, usually separating paragraphs.
    chunk_size=60, # it will break from blank line (given seprator) only so chunks sizes could be verry.
    chunk_overlap=0
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:", end=' ')
    print(chunk)

'''
Chunk 1: Python is a programming language.
Chunk 2: It is widely used for AI and machine learning.
Chunk 3: LangChain helps developers build applications with LLMs.
'''

# IF there is not blank line between paragraphs - 

print('test separtor........')

text = '''
Python is a programming language.
It is widely used for AI and machine learning.
LangChain helps developers build applications with LLMs.
'''

# It will first create 60 chars chunks and then devide this from space char.
splitter = CharacterTextSplitter(
    separator=" ",
    chunk_size=60,
    chunk_overlap=0
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i} & Length is {len(chunk)} chars: ", end=' ')
    print(chunk)

'''
Chunk 1 & Length is 58 chars:  Python is a programming language. It is widely used for AI
Chunk 2 & Length is 54 chars:  and machine learning. LangChain helps developers build
Chunk 3 & Length is 23 chars:  applications with LLMs.
'''


#---------------------------------------------------------------------------------

# Sementic Splitter

# The main idea is simple: instead of splitting text after a fixed number of characters, 
# split it `when the meaning or topic changes`.

print('Sementic Splitter with SemanticChunker...............')

# Required package > langchain-experimental and embedding models

content = '''
Python is a programming language used to build applications, automate tasks, and process data.
Python supports lists, dictionaries, functions, and classes.
Cricket is a bat-and-ball sport played between two teams.
The environment includes forests, rivers, oceans, air, and living organisms.
Planting trees, reducing plastic waste, and conserving water help protect natural resources.
'''

from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv
import os
load_dotenv()

# Load the environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001', google_api_key=GOOGLE_API_KEY)

# vector = model.embed_query(content)

# print('embedding')
# print(vector)
# print("Total embedding vectors:", len(vector)) # Total embedding vectors: 3072

splitter = SemanticChunker(
    embeddings=model,
    breakpoint_threshold_type="standard_deviation", 
    breakpoint_threshold_amount=0
    )


'''
breakpoint_threshold_amount = range (0 to 1)

Lower value = more splits. 
Higher value = fewer splits, generally.
'''


chunks = splitter.create_documents([content])

print('total chunks length', len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk.page_content)
    
'''
Below chunks with breakpoint_threshold_amount=1

Chunk 1:
Python is a programming language used to build applications, automate tasks, and process data. Python supports lists, dictionaries, functions, and classes. Cricket is a bat-and-ball sport played between two teams.

Chunk 2:
The environment includes forests, rivers, oceans, air, and living organisms. Planting trees, reducing plastic waste, and conserving water help protect natural resources. 

Below chunks with breakpoint_threshold_amount=0.5

Chunk 1:
Python is a programming language used to build applications, automate tasks, and process data. Python supports lists, dictionaries, functions, and classes. Cricket is a bat-and-ball sport played between two teams.

Chunk 2:
The environment includes forests, rivers, oceans, air, and living organisms.

Chunk 3:
Planting trees, reducing plastic waste, and conserving water help protect natural resources. 

'''

# Final takeaway Semantic Chunker is useful for meaning-based chunking, but it does not guarantee perfectly separated topics. Always inspect the results and choose a chunking strategy appropriate for your RAG application.

#---------------------------------------------------------------