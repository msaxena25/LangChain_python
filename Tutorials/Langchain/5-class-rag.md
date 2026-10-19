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

This is the most important connection to what you've already learned.

RAG is an application pattern, not a single LangChain class or method. LangChain provides the building blocks you can combine to implement it.

Here is how the concepts you've studied fit together:

### LangChain RAG architecture

A typical RAG application has two phases.

### Phase 1: Prepare your knowledge base

Document Loaders: Read PDFs, text files, web pages, etc.

Text Splitters: Split large documents into smaller chunks.

Embedding Model + Vector Store : Represent chunks as vectors and store them for searching.

Knowledge base is ready

### Phase 2: Answer a user's question

1\. Retriever

Find relevant document chunks for the question.

2\. Prompt Template

Combine the retrieved context with the question.

3\. Chat Model + Output Parser

Generate and format the answer.

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
# 1. What is a Document Loader in LangChain?

A Document Loader is a component that reads data from a source and converts it into LangChain `Document` objects so that the data can be processed in a consistent way.

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

Install the package: All loaders comes under this below package.

```py
pip install -U langchain-community
```

```py
from langchain_community.document_loaders import TextLoader

loader = TextLoader("company_policy.txt", encoding="utf-8")

docs = loader.load()

print(docs[0].page_content)
print(docs[0].metadata)
```

**Important:** load() returns a list of Document objects, even if the loader returns just one document.

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

`UnstructuredPDFLoader`: pdf that contains scanned images, extrcat more structure patterns and understand element-based document extraction

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
    glob="**/*.pdf",
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

**Important:** CSVLoader reads each CSV row and converts it into a formatted text string. It doesn't simply copy the original comma-separated row.

How does this happen?

1. CSVLoader reads the CSV file using CSV-reading logic.
2. It identifies the column headers: id, name, description, and price.
3. It reads the first data row and matches each value with its column name.
4. It formats each column-value pair as `column: value` on a `separate line`.
5. It stores that formatted text in Document.page_content

---------