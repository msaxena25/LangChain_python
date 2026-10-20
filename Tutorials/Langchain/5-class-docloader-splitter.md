# RAG in LangChain

## 1. What is RAG?

RAG stands for Retrieval-Augmented Generation.

It is a `technique` in which an AI application retrieves relevant information from an external source and provides that information to a language model so it can generate a more relevant, context-aware answer.


Let's break down the three words:

- `Retrieval`: Find relevant information from documents, files, databases, or other sources.
- `Augmented`: Add that retrieved information to the context provided to the model.
- `Generation`: The model uses that context to generate an answer.

### A simple real-world example

Imagine you have 500 PDF documents containing your company's internal policies. You ask:

"How many casual leaves can an employee take?"

A normal LLM might not know your company's specific policy. RAG helps your application search those PDFs, find the relevant leave policy, and provide it to the model to answer your question.

1\. User asks a question

"How many casual leaves can I take?"

2\. Retrieval

Search the company's policy documents

3\. Relevant context is retrieved

The section describing casual leave entitlement

4\. LLM generates an answer

Uses the question and retrieved policy to answer

**The key idea: instead of relying only on what the model learned during training, we give it relevant information at the time of the question.**

## 2. What problem does RAG actually solve?

There are four major problems RAG helps address.

| Problem                                          | How RAG helps                                                         |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| The LLM doesn't know your private data           | Retrieves information from your own documents and systems             |
| The LLM's knowledge may be outdated              | Retrieves newer information from an updated source                    |
| Sending every document to the LLM is impractical | Retrieves only selected relevant sections                             |
| The LLM may invent unsupported answers           | Grounds answers in retrieved context, which can reduce hallucinations |

One important point: RAG does not guarantee correct answers. If retrieval finds the wrong documents, the documents contain errors, or the model misinterprets them, the final answer can still be wrong.

RAG also doesn't require retraining the LLM whenever your documents change. You generally update your knowledge source and its searchable index instead.

## 3. How does RAG fit into LangChain?

RAG is an **application pattern, not a single LangChain class or method. LangChain provides the building blocks** you can combine to implement it.

Here is how the concepts you've studied fit together:

### LangChain RAG architecture

A typical RAG application has two phases.

### Phase 1: Prepare your knowledge base

Document Loaders: Read PDFs, text files, web pages, etc.

Text Splitters: Split large documents into smaller chunks.

Embedding Model + Vector Store : Represent chunks as vectors and store them for searching.

Knowledge base is ready

### Phase 2: Answer a user's question

1\. Retriever: Find relevant document chunks for the question.

2\. Prompt Template: Combine the retrieved context with the question.

3\. Chat Model + Output Parser: Generate and format the answer.

## 4. One important distinction: Indexing vs. RAG

You previously learned about indexing and RAG. Keep this distinction clear:

- Indexing prepares data for efficient retrieval: load, split, embed, and store.
- Retrieval searches that prepared data for relevant content.
- RAG uses retrieved content to augment the LLM's input and generate an answer.

You can have a searchable index without generating an answer with an LLM. That is semantic search. When you combine retrieval with generation, you have a RAG workflow.

## 5. What should we learn next?

I'd recommend this sequence, with practical Python examples:

1. Document Loaders — load a `.txt` file or PDF.
2. Document and Text Splitters — understand `Document`, chunks, and chunk overlap.
3. Embeddings — understand how text becomes vectors.
4. Vector Stores — store and search those vectors.
5. Retrievers — retrieve relevant chunks from a question.
6. Build a complete RAG pipeline — connect retrieval, prompt, model, and parser using LCEL.

---
# What is a Document Loader in LangChain?

A `Document Loader` is a `component` that reads data from a source and converts it into LangChain `Document` objects so that the data can be processed in a consistent way.

Sources can include text files, PDFs, websites, CSV files, Word documents, databases, and more.

## What problem does it solve?

Imagine you're building a RAG application that needs to read:

- 20 `.txt` files
- 50 PDF files
- A company website
- A CSV containing product information

Each source has a different format and requires a different way to read it. Without a common structure, you would need to write separate extraction and processing logic for each format.

LangChain's document loaders simplify this by converting those sources into a common `Document` structure.


# 2. The two parts of a LangChain Document

Each LangChain `Document` has two main data attributes:

1. `page_content` — the actual text content.
2. `metadata` — information describing that content.

For example, imagine a document containing your company's leave policy.

```py
from langchain_core.documents import Document

doc = Document(
    page_content="Employees are entitled to 12 casual leaves per year.",
    metadata={
        "source": "leave_policy.txt",
        "department": "HR",
        "year": 2026
    }
)

print(doc.page_content)
print(doc.metadata)
```

# 3. The four important Document Loaders

## A. TextLoader — load a `.txt` file

Purpose: Read a plain-text file and convert its content into a LangChain `Document`.

**Install the package:** All loaders comes under this below package.

```py
pip install -U langchain-community
```

```py
from langchain_community.document_loaders import TextLoader

loader = TextLoader("company_policy.txt", encoding="utf-8") #encoding is optional

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

**Important:** **load() returns a list of Document objects, even if the loader returns just one document**.

The text loader typically puts the file's full text into one document. You can split it into smaller chunks later.

## B. PyPDFLoader — load a PDF

Purpose: Extract text from a PDF and create LangChain `Document` objects.

Required package - lanchain-community and pypdf


```py
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("company_policy.pdf")

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

By default, `PyPDFLoader` generally creates one document per PDF page. The metadata includes the source and page number.

## Other PDF Loader

`PDFPlumberLoader`: table-related content. pdf have tables , rows and columns 

`UnstructuredPDFLoader`: pdf that contains scanned images, extract more structure patterns and understand element-based document extraction

`PyMuPDFLoader`: table extraction, image extraction, and layout-aware text extraction.

`PyPDFDirectoryLoader`: when you have many PDFs in a folder and want to load them together.

## `DirectoryLoader`

DirectoryLoader is used to l**oad multiple files from a directory (folder)** instead of loading each file individually.

```
company_docs/
    leave_policy.txt
    refund_policy.txt
    security_policy.txt
    employee_handbook.txt
```

```py
from langchain_community.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader(
    "company_docs/",
    glob="*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

docs = loader.load()

print("Total documents:", len(docs))
print(docs[0].page_content)
print(docs[0].metadata)
```

Here is what each argument means:

| Argument                | Purpose                                                            |
| ----------------------- | ------------------------------------------------------------------ |
| `"company_docs/"`       | The folder to search.                                              |
| `glob="*.txt"`          | Selects `.txt` files in that folder.                               |
| `loader_cls=TextLoader` | Specifies how each selected file should be loaded.                 |
| `loader_kwargs`         | Passes additional arguments to `TextLoader`.                       |
| `load()`                | Loads the matching files and returns a list of `Document` objects. |

## Load PDFs from a directory

You can use the same `DirectoryLoader` with `PyPDFLoader`:

**Remember:** DirectoryLoader does not itself extract every file format. It finds the files, then delegates each file to the loader you specify through `loader_cls`.

```py
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    "company_docs/", # can define path directly as first argument
    glob="**/*.pdf", # matches PDF files in the directory and its subdirectories.
    loader_cls=PyPDFLoader
)

OR

loader = DirectoryLoader(
    path= "company_docs/", # can define with path property
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.load()

print("Total page documents:", len(docs)) # will print total pages, not the number of PDF files.
print(docs[0].page_content) # 0th page that it stores in document object
print(docs[0].metadata)

print(docs[3].page_content) # 3rd page from document object

print(docs[5].page_content) #IndexError: list index out of range (means total page will be only 5 (0 to 4))
```

- `glob="**/*.pdf"` matches PDF files in the directory and its subdirectories.

- With `PyPDFLoader`, the resulting document count generally corresponds to the total number of PDF pages, not the number of PDF files.

----

## load() vs lazy_load() method

### load()

- load everything at once.
- return a list of Document Object.
- load all documents immediately ito memory.
- use when number of documents are small or you want every document upfront before any processing.

### lazy_load()

- load document on demand
- return a `generator` of document object.
- Documents are not loaded at once, they are fetched one at a time as needed.
- Use when dealing with large number of documents or you want stream processing (chunking, embedding) without using lots of memory.

```py

loader = DirectoryLoader(
    path= "company_docs/",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load()

print(docs) # <generator object DirectoryLoader.lazy_load at 0x0000023FB3584D30>

# use for loop on this docs object & this will print meta data once after load
for doc in docs:
    print(doc.metadata)


```

### Here's the sequence:

1. Create a generator: `lazy_load()` returns an iterator/generator-like object instead of a list of all documents.
2. Request the first document: When the `for` loop asks for the next item, the loader produces a document.
3. Process the document: Your code reads, prints, or otherwise processes that document.
4. Move to the next document: When the loop requests the next item, the loader continues and yields another document.
5. Memory management: If your code doesn't keep references to previous documents, they can become eligible for garbage collection after they're no longer needed.

One important correction: `lazy_load()` does not necessarily explicitly remove each document from memory after processing it. Python manages memory, and the loader's implementation determines how it reads the source.

**In short: produce a document → process it → request the next document, without needing to collect all documents into a list first.**

------

## WebBaseLoader

A web-based document loader fetches content from a webpage and converts the extracted content into LangChain `Document` objects.

The official implementation fetches webpages and parses their HTML using **Beautiful Soup** `beautifulsoup4` library. WebBaseLoader uses Beautiful Soup internally to parse HTML, so we didn't explicitly call it in our code. But you need to install it.

```py
pip install -U langchain-community beautifulsoup4

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://example.com/") # provide public url of that webpage
docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

The output contains the extracted webpage text in `page_content` and available information such as the URL or page title in `metadata`.

### What problem does it solve?

Imagine you're building a RAG chatbot that answers questions about your company's public website.

Without a web loader, you might have to manually copy webpage content, clean it, and prepare it for your RAG pipeline.

A web loader automates the initial fetching and extraction process by loading web page.

## 4. Limitations of `WebBaseLoader`

| Limitation                  | What happens                                                                                         |
| --------------------------- | ---------------------------------------------------------------------------------------------------- |
| JavaScript-rendered content | Content added after the page loads in a browser may be missing.                                      |
| Login-protected websites    | Pages requiring authentication may return a login page or an error.                                  |
| Anti-bot protection         | The website may block the request or return a challenge page.                                        |
| Unwanted HTML content       | Navigation links, footers, cookie banners, and advertisements may appear in extracted text.          |
| Multiple pages              | Providing one URL loads that page; it does not automatically crawl the entire website.               |
| PDFs and other files        | It is designed primarily for HTML pages, not specialized extraction from PDFs or other file formats. |
| Website changes             | HTML structure and page content can change, so extraction results may change too.                    |

These limitations are important because poor extraction can lead to poor retrieval and inaccurate RAG answers.

---

## CSVLoader

`CSVLoader` is a LangChain document loader that reads a CSV file and converts its rows into LangChain `Document` objects.

CSV stands for Comma-Separated Values. It's commonly used for product catalogs, customer records, transaction reports, and other tabular data.

### What problem does it solve?

Suppose you want to build a RAG chatbot that answers questions about 10,000 products. Instead of manually converting each CSV row into text, `CSVLoader` can turn the rows into documents that LangChain can process.

### 2. Example CSV file

Suppose you have a file named `products.csv`:

```
id,name,description,price
101,Mouse,Wireless mouse,799
102,Keyboard,Mechanical keyboard,2499
103,Monitor,Full HD monitor,12999
```

Each row represents one product, and the first row contains the column names.

## 3. Load the CSV file

**Important:** CSVLoader reads each CSV row and converts it into a formatted text string. It doesn't simply copy the original comma-separated row.

How does this happen?

1. CSVLoader reads the CSV file using CSV-reading logic.
2. It identifies the column headers: id, name, description, and price.
3. It reads the first data row and matches each value with its column name.
4. It formats each column-value pair as `column: value` on a `separate line`.
5. It stores that formatted text in Document.page_content

```py
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader("products.csv")

docs = loader.load()

print("Total documents:", len(docs)) #3

print(docs[0].page_content)
# id: 101
# name: Mouse
# description: Wireless mouse
# price: 799

print(docs[0].metadata)
# {'source': 'products.csv', 'row': 0}

# Print only single column name from each row - 

for row in docs:
    line = row.page_content.splitlines()
    for item in line:
        if item.startswith('name:'):
            print(item)
# name: Mouse
# name: Keyboard
# name: Monitor
```

### Load a specific encoding

If your CSV contains special characters or non-English text:

```py
loader = CSVLoader(
    file_path="products.csv",
    encoding="utf-8"
)

docs = loader.load()
```

### Put selected columns into metadata

For example, If you want product ID in metadata as well then use metadata_columns

```py
loader = CSVLoader(
    file_path="products.csv",
    metadata_columns=["id"]
)

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

---------

# Text Splitters

Since you've learned Document Loaders, the next step in the RAG pipeline is Text Splitters.

## What is a Text Splitter?

A text splitter divides a large document into smaller pieces called chunks.

Document Loader - Loads the PDF into Document objects

Text Splitter - Divides document content into chunks

## Why do we need it?

- LLMs have limits on how much text they can process in one request.
- Smaller chunks help retrieval find information relevant to a question.
- Chunks can be embedded and stored in a vector store individually.
- Smaller, relevant context can reduce unnecessary information in the prompt.

One important point: a text splitter usually splits the `page_content` of a `Document` and preserves its metadata in the resulting chunks.

# RecursiveCharacterTextSplitter

The most commonly used splitter is `RecursiveCharacterTextSplitter`.

| Parameter         | Meaning                                                |
| ----------------- | ------------------------------------------------------ |
| `chunk_size`      | Maximum target size of each chunk                      |
| `chunk_overlap`   | Number of characters repeated between adjacent chunks  |
| `length_function` | Function used to measure chunk size; defaults to `len` |
| `separators`      | Boundaries used to decide where to split text          |


**Its default separator order is:**

`\n\n` 1\. Paragraphs - Try splitting at blank lines.

`\n` 2\. Lines - If still too large, try newlines.

`" "` 3\. Words - If still too large, try spaces.

`""` 4\. Characters - As a last resort, split between characters.

Let's understand these with Python.

## First practical example

Install the current text-splitter package if you don't have it:

```
pip install -U langchain-text-splitters

# -U in a pip command means upgrade.
# It tells pip to install the package and upgrade it to the latest compatible version if an older version is already installed.
```

Create a simple example:

```py
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
Python is a programming language.
It is widely used for AI and machine learning.
LangChain helps developers build applications with LLMs.
Text splitting is an important step in RAG.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,
    chunk_overlap=10 # tries to retain 10 characters from the preceding chunk where applicable.
)

chunks = splitter.split_text(text)

for index, chunk in enumerate(chunks, start=1):
    print(index, chunk)
```

Here, `split_text()` takes a string and returns a list of strings.

- `chunk_size=60`: aims to keep each chunk within 60 characters.
- `chunk_overlap=10`: tries to retain 10 characters from the preceding chunk where applicable.

The exact chunks depend on the text and the splitter's boundary logic.

## 4. What is chunk overlap, and why do we need it?

Imagine a sentence gets split at a boundary:

Without overlap

```
['The employee can request a refund within 30', 'days of purchasing the product.']
```

With overlap

```
['The employee can request a refund within 30 days', 'within 30 days of purchasing the product.]
```

Overlap helps preserve context between chunks. The example above is illustrative; actual overlap is based on character counts and split boundaries.

## 5. Split LangChain Documents

In real RAG applications, you'll often split the `Document` objects returned by your loaders, rather than manually splitting strings.

```py
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("company_policy.txt", encoding="utf-8")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print("Original documents:", len(documents))
print("Total chunks:", len(chunks))

print(chunks[0].page_content)
print(chunks[0].metadata)
```

`split_text(text)` → accepts a string and returns strings.

`split_documents(documents)` → accepts Document objects and returns smaller Document objects, preserving their metadata.

--------

# `CharacterTextSplitter` 

`CharacterTextSplitter` splits text using one specific separator that you choose.

For example, you can tell it to split text wherever it finds:

- `"\n\n"` — a blank line, usually separating paragraphs.
- `"\n"` — a newline.
- `" "` — a space.
- `","` — a comma.

Its default separator is `"\n\n"`. You can also configure `chunk_size` and `chunk_overlap`.

The key difference is that it doesn't automatically try other separators when the chunks are too large.

## Code example: `CharacterTextSplitter`

```py
from langchain_text_splitters import CharacterTextSplitter

text = '''
Python is a programming language.

It is widely used for AI and machine learning.

LangChain helps developers build applications with LLMs.
'''

splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=60,
    chunk_overlap=0
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i}:")
    print(chunk)
    print("---")
```

How it works:

1. It looks for `"\n\n"` in the text.
2. It splits the text at those boundaries.
3. It combines the resulting pieces into chunks, `trying` to respect `chunk_size`.
4. If one piece between separators is too large, it can still produce a chunk larger than `chunk_size`.

That last point is important: `chunk_size=60` is not a guarantee that every chunk will be at most 60 characters.

-------

# Difference `RecursiveCharacterTextSplitter` & `CharacterTextSplitter`

The main difference is what happens when a piece of text is larger than `chunk_size`.

## 1. `CharacterTextSplitter` — one separator

Suppose you configure it with `separator="\n\n"`.

It only uses blank lines as splitting boundaries. If a paragraph is too large, it doesn't automatically try splitting it at spaces or individual words.

Input text — one long paragraph

## 2. `RecursiveCharacterTextSplitter` — multiple separators

It starts with larger, natural boundaries. If a piece is still too large, it tries smaller boundaries.

Its default separator order is:

`\n\n` 1\. Paragraphs - Try splitting at blank lines.

`\n` 2\. Lines - If still too large, try newlines.

`" "` 3\. Words - If still too large, try spaces.

`""` 4\. Characters - As a last resort, split between characters.

For the same input and same chunk_size, it can split at spaces to create smaller chunks.


## Remember this

| `CharacterTextSplitter`                   | `RecursiveCharacterTextSplitter`                                |
| ----------------------------------------- | --------------------------------------------------------------- |
| Uses one configured separator             | Tries multiple separators in sequence                           |
| Doesn't fall back to smaller separators   | Falls back to smaller separators                                |
| Can return oversized chunks               | Usually respects the target size when suitable boundaries exist |
| Useful when you need a specific delimiter | Useful for general-purpose RAG                                  |

Important: `chunk_size` is a target limit, not an absolute guarantee for either splitter. For the recursive splitter, an unusually long word or string with no available separator can still exceed the target.
 

-------

# Recursive Text Splitter for different document types

In RAG, you may load different kinds of files: 

**Python code, JavaScript/TypeScript, Markdown (`.md`), HTML, PDFs**, and plain text. Although `RecursiveCharacterTextSplitter` can split all of them, the best splitting strategy depends on the document's structure.

## Code examples

For code, use `RecursiveCharacterTextSplitter.from_language()` to load a language-specific separator configuration.

```py
python_splitter = RecursiveCharacterTextSplitter.from_language(
    Language.PYTHON, 
    chunk_size=500, 
    chunk_overlap=50
)
# TypeScript
ts_splitter = RecursiveCharacterTextSplitter.from_language(
    Language.TS, chunk_size=500, chunk_overlap=50
)

# Markdown
md_splitter = RecursiveCharacterTextSplitter.from_language(
    Language.MARKDOWN, chunk_size=500, chunk_overlap=50
)

#rest code is same.
```

What's different here?

The Python-specific separator list prioritizes `boundaries` such as class and function definitions before falling back to generic boundaries.

-----

# MarkdownTextSplitter

Although we can split mark down document with RecursiveCharacterTextSplitter.from_language(Language.MARKDOWN), But still we have seperate splitter for that.

Markdown contains headings, paragraphs, lists, and code blocks. This uses `Markdown-specific separators` with recursive splitting.

```py
from langchain_text_splitters import MarkdownTextSplitter

splitter = MarkdownTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
)
```
--------

# LangChain: Semantic-Based Text Splitter

Till now we have seen splits on the basis of length, special splitter point like space, line break, words and chars.

The main idea is simple: instead of splitting text after a fixed number of characters, split it `when the meaning or topic changes`.

A character-based splitter might divide the document according to length, even in the middle of a topic. **A semantic splitter tries to keep related content together** and identify where the topic changes.

## The five steps behind semantic splitting

**1 Divide the document into small units:** The splitter first separates the document into sentences or other small text units.

**2 Generate embeddings**: Each text unit is converted into an embedding — a numerical representation of its meaning.

**3 Compare neighboring text units:** The splitter compares the meaning of nearby sentences using their embeddings. It looks for places where the meaning changes substantially, rather than simply measuring how many characters separate them.

**4 Determine the semantic-change threshold:** This is where parameters such as `standard_deviation` and `percentile` come into play. They help determine how large a change in meaning must be before the splitter treats it as a potential boundary.

**5 Create the final chunks:** The splitter joins neighboring text units until it reaches a detected semantic boundary. The resulting chunks aim to preserve related ideas together, making them more useful for downstream retrieval in a RAG application.

------

## First Understand mathmetical term `Standard deviation`

Standard deviation is a mathematical measure that tells us how much the values in a dataset are `spread out from their average (mean)`.

- Low standard deviation: Values are close to the average.
- High standard deviation: Values are spread far from the average.

Suppose we have two datasets:

```
- Dataset A: 8, 9, 10, 11, 12
- Dataset B: 2, 6, 10, 14, 18
```

**Step 1: Calculate the mean**

```
(8 + 9 + 10 + 11 + 12) / 5 = 10

(2 + 6 + 10 + 14 + 18) / 5 = 10
```

**Step 2: Calculate the difference from the mean and square it**

For dataset A:

```py
# We square the differences so that negative and positive differences don't cancel each other out.

Value	Difference from mean	Squared difference
8	        8 − 10 = −2	            4
9	        9 − 10 = −1	            1
10	        10 − 10 = 0	            0
11	        11 − 10 = 1	            1
12	        12 − 10 = 2         	4
Total		                        10
```

**Step 3: Calculate the variance**

`Variance` tells us `how spread out the values are around the mean`. 

Variance is the average of the squared differences from the mean.

```py
(4 + 1 + 0 + 1 + 4) / 5 = 2

# Variance = 2: Average squared distance from the mean.
```
**Step 4: Standard deviation**

Standard deviation is simply the `square root of variance`.

```py
sd = sqrt_root(2) = 1.41 # this for dataset A

Same like above steps standard deviation of dataset B = 5.66
```

**The key takeaway:** Dataset B has a higher standard deviation because its values are more spread out from the mean.

----------

# Semantic Splitter — Step-by-Step Example

Lets first create a document with different - different topics - 

First 2 paragraphs are related to Pyhton, 3rd para = cricket and 4th and 5th paras related to enviournment.

```
Python is a programming language used to build applications, automate tasks, and process data.
Python supports lists, dictionaries, functions, and classes.
Cricket is a bat-and-ball sport played between two teams.
The environment includes forests, rivers, oceans, air, and living organisms.
Planting trees, reducing plastic waste, and conserving water help protect natural resources.
```

**Step 1: Compare adjacent paragraphs**

Imagine that an embedding model converts each paragraph into a numerical vector. We compare neighboring paragraphs and assign these hypothetical semantic-distance scores:

```
Comparison	    Topic transition	    Distance
P1 → P2	        Python → Python	        0.10
P2 → P3	        Python → Cricket	    0.80
P3 → P4	        Cricket → Env       	0.75
P4 → P5	        Env → Env	            0.15
```

**Step 2: Calculate the mean**

```py
Mean = 0.45 # add all distance and devide by 4
```

**Step 4: Calculate variance**

```py
Variance = 0.425 / 4 = 0.10625

# For each distance, we calulate distance from means then calculate square of that difference.
# Then total of each differece = 0.425.
# Thent take mean of that total difference = 0.10625
```
**Step 5: Calculate standard deviation**

```py
sd = square_root(variance) = square_root(0.10625) = 0.3260
```

**Step 6: Calculate the threshold**

We need a rule to decide which distances are large enough to indicate a potential topic change.

The `threshold` is that cutoff value:

- Distance above the threshold → split.
- Distance at or below the threshold → don't split.

```py
Threshold = Mean + Standard deviation

T = 0.45 + 0.3260 = 0.7760 
```
**Step 7: Compare each distance with this threshold value**

```
Distance	    Comparison	    Decision
0.10	        0.10 < 0.7760	Don't split
0.80	        0.80 > 0.7760	Split
0.75	        0.75 < 0.7760	Don't split
0.15	        0.15 < 0.7760	Don't split
```

## Python code 

```py
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import GoogleGenerativeAIEmbeddings

model = GoogleGenerativeAIEmbeddings(model='gemini-embedding-001', google_api_key=GOOGLE_API_KEY)

vector = model.embed_query(content)
print('embedding')
print(vector)
print("Total embedding vectors:", len(vector)) #Total embedding vectors: 3072

splitter = SemanticChunker(embeddings=model, breakpoint_threshold_type="standard_deviation", breakpoint_threshold_amount=1)

chunks = splitter.create_documents([content])

print('total chunks length', len(chunks)) #2

for i, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {i}:")
    print(chunk.page_content)

# Below chunks with breakpoint_threshold_amount=1

Chunk 1:
Python is a programming language used to build applications, automate tasks, and process data. Python supports lists, dictionaries, functions, and classes. Cricket is a bat-and-ball sport played between two teams.

Chunk 2:
The environment includes forests, rivers, oceans, air, and living organisms. Planting trees, reducing plastic waste, and conserving water help protect natural resources. 

# Below chunks with breakpoint_threshold_amount=0.5

Chunk 1:

Python is a programming language used to build applications, automate tasks, and process data. Python supports lists, dictionaries, functions, and classes. Cricket is a bat-and-ball sport played between two teams.

Chunk 2:
The environment includes forests, rivers, oceans, air, and living organisms.

Chunk 3:
Planting trees, reducing plastic waste, and conserving water help protect natural resources. 
```

## breakpoint_threshold_amount

Lower value = more splits. 

Higher value = fewer splits, generally.

Important: More splits doesn't necessarily mean more precise. A lower value may separate topics better, but it can also split related content unnecessarily.

## Conclusion

**Final takeaway:** SemanticChunker is useful for meaning-based chunking, but it does not guarantee perfectly separated topics. Always inspect the results and choose a chunking strategy appropriate for your RAG application.

-----

# Same Embedding model for both document & user query

Yes, your understanding is correct. ✅

For reliable similarity search in RAG, you should use the same embedding model for both your documents and the user's query.

### Example

| Document embeddings | User query embedding | Recommended? |
| ------------------- | -------------------- | ------------ |
| Gemini embeddings   | Gemini embeddings    | Yes          |
| OpenAI embeddings   | OpenAI embeddings    | Yes          |
| Gemini embeddings   | OpenAI embeddings    | Generally no |
| Model A embeddings  | Model B embeddings   | Generally no |

### Why?

Suppose you store your document embeddings using Gemini. When a user asks, "What is my name?", you generate an embedding for that query using Gemini too.

Both vectors are then in the same embedding space, so you can compare them using cosine similarity or another suitable distance metric.

If you use a different model for the query, its vector may have different dimensions or represent meaning differently. Similarity scores may then be invalid or unreliable.

----------

