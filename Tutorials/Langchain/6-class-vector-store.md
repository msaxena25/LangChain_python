
# Vector Store

A vector store is a system designed to store and retrieve data represented as numerical vectors.

## Key Features

1. **Storage** - Ensures that vectors and their `associated metadata` are retained, whether `in-memory` for quick lookups or `on-disk` for durability and large-scale use.

    **Storage can be:**

    - In-memory: Kept in RAM. Fast, but data may disappear when the application stops unless it is persisted.
    - On-disk or database-backed: Stored persistently so the data can survive application restarts.

2. **Similarity Search** - Helps retrieve the vectors most similar to a query vector.

    **Similarity is commonly measured using:**

    - Cosine similarity: Compares the direction of two vectors.
    - Euclidean distance: Measures the straight-line distance between vectors.
    - Dot product: Measures the product of corresponding vector values, summed together.

3. **Indexing** - Provide a `data structure` or method that enables fast similarity searches on high-dimensional vectors (e.g., `approximate nearest neighbor lookups`).

    **Indexing — Find similar vectors faster**

    One common technique is Approximate Nearest Neighbor (ANN) search. It aims to find very similar vectors quickly without necessarily checking every vector.

4. **CRUD Operations** - Manage the lifecycle of data-adding new vectors, reading them, updating existing entries, removing outdated vectors.

----

## Use-cases

1. Semantic Search
2. RAG
3. Recommender Systems
4. Image/Multimedia search

------

## Indexing Algo - Cluster-Based Indexing (IVF)

IVF stands for Inverted File.

1\. Create clusters: Divide all stored vectors into groups based on their similarity. Each group is called a cluster.

2\. Choose cluster centers: Identify a center point for each cluster, called a `centroid`.

3\. Assign vectors: Assign each vector to its nearest centroid.

4\. Receive a query: Convert the user's query into an embedding vector.

5\. Find relevant clusters: Compare the query vector with the cluster centroids and select the closest clusters.

6\. Search selected clusters: Compare the query vector with vectors inside only those selected clusters, instead of searching every stored vector.

7\. Return results: Return the closest matching vectors found in the selected clusters.

**Advantage:** Can reduce the amount of data searched and use less memory than some alternatives.

**Disadvantage:** If the relevant movie is in an unsearched cluster, it can be missed.

**Best for:** Large datasets where clustering and tuning can deliver an appropriate speed–accuracy trade-off.

## 2. Other indexing algorithms and techniques

\- **Flat (Brute-Force) Search:** Compares the query against every stored vector. It provides exact nearest-neighbor results but can be slow for large datasets.

\- **HNSW (Hierarchical Navigable Small World):** Builds a graph connecting nearby vectors and navigates that graph to find similar vectors quickly. It generally provides a good balance between speed and search accuracy.

\- **PQ (Product Quantization):** Compresses vectors into smaller representations to reduce memory usage. It can be combined with IVF or other search methods to make large-scale vector search more efficient.

---------

# Vector Store Vs Vector Database

## Vector Store

o Typically refers to a `lightweight library` or service that focuses on storing vectors (embeddings) and performing similarity search.

o May not include many traditional database features like transactions, rich query languages, or role-based access control.

o Ideal for prototyping, smaller-scale applications

o Examples - `FAISS`, `Chroma`, `Annoy`, `QdrantVectorStore`, `PineconeVectorStore`

## Vector Database

o A full-fledged database system designed to store and query vectors.

o Offers additional "database-like" features:

    · Distributed architecture for horizontal scaling
    . Durability and persistence (replication, backup/restore)
    · Metadata handling (schemas, filters)
    · Potential for ACID or near-ACID guarantees
    · Authentication/authorization and more advanced security
    · Example - `Milvus`, `Qdrant`, `Weaviate`, `Pinecone`

**Important: Vector database is effectively a vector store with extra database feature.**

--------

# ChromaDB Vector Store

Chroma DB is a Vector Store that provides some feature of database as well.

## Required packages 

```py
pip install -U langchain-chroma
pip install -U chromadb

# We dont need to import chromadb packaage in code. langchain-chroma use that internally.
```

## langchain.vectorstores

The older `langchain.vectorstores` import isn't the correct path to use for the current Chroma integration. 

LangChain now documents Chroma through the separate `langchain-chroma` package.

from langchain.vectorstores import Chroma (this does not work now.)

## Create vector store from Chroma Class

```py
from langchain_core.documents import Document
from langchain_chroma import Chroma

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
    )

# lets create vector_store 
vector_store = Chroma(
    collection_name="learning_notes",
    persist_directory="./chromadb", # foldername where chromedb will store.
    embedding_function=embedding_model
)
```

Chroma creates a directory named `chroma_db` in your current working directory. It manages its own internal database and index files there.

## Adding documents

```py
documents = [
    Document(
        page_content="Python is a programming language used for AI and machine learning.",
        metadata={"topic": "Python", "source": "notes_1"},
        id="doc_1" # optional but recommended to add id to the documents while adding them to the vector store.
    )
]
vector_store.add_documents(documents=documents)
```

## Chroma.from_documents()

`Chroma.from_documents() `is a class method that creates a Chroma vector store and adds the provided documents to it. You dont need to call add document method seperately.

```py
from langchain_chroma import Chroma

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="learning_notes",
    persist_directory="./chroma_db"
)
```

## Get documents

```py
# return all documents dictionary
documents = vector_store.get() 

# Get document By id or ids
doc_ids: dict[str, Any] = vector_store.get(ids=['doc_1'])["ids"]
print('doc_ids', doc_ids)

#view documents with metadata using include prop
documents = vector_store.get(include=["documents", "metadatas"])

```

## similarity_search

```py
# k is the number of related documents to return
documents = vector_store.similarity_search(query="What is Python?", k=2)

# similarity_search with score
documents = vector_store.similarity_search_with_score(query="What is Python?", k=1)

# filter options - topic, source, id (associated metadata values)
documents = vector_store.similarity_search(
    query="", k=1, filter={"topic": "LangChain"})
```

## Update and delete document

```py
document= Document(page_content="Python is a programming language used for AI and machine learning.", 
metadata={"topic": "Python", "source": "notes_1"}, id="doc_1")

# update single doc
vector_store.update_document(document_id="doc_1", document=document)

# update multiple or single doc
vector_store.update_documents(ids=["doc_1"], documents=[document])

# delete documents from the vector store
vector_store.delete(ids=["doc_1"])
```

## Checking Existing document

```py

# First extract Ids from documents list
document_ids: list[str | None] =  [doc.id for doc in documents]
print('document_ids', document_ids)

# Now check if the embeddings already exist in the vector store
embeddings_ids: dict[str, Any] = vector_store.get(ids=document_ids)["ids"]
print('embeddings_ids', embeddings_ids)
# embeddings_ids ['doc_1', 'doc_2', 'doc_3', 'doc_4']

# Now find the new ids which need to be added to the vector store

new_docs = [doc for doc in document_ids if doc.id not in embeddings_ids]
print('new_docs', new_docs)
# new_ids []

if new_docs:
    new_added_docs_ids = vector_store.add_documents(documents=new_docs)
    print('New documents added to the vector store', new_added_docs_ids)
else:
    print('All documents already exist in the vector store')
```

-----------

# Retriever

Retriever is a component in LangChain that fetches relevant document from a data source in response to a user query.

Most important part is all `retrievers in LangChain are Runnables`. Means they all have invoke method.

## Types of Retriever

Generally Retrievers are classified in two types.

1. Data source based Retriever: Wikipedia retriever, Vector store retriever, Archieve retriever

2. Search strategy based retriever: MMR, Multi query Retriever, Contextual compression

## Wikipedia Retriever

WikipediaRetriever is a retriever that fetches information from Wikipedia. LangChain's implementation uses a Wikipedia API wrapper to search Wikipedia and return the results as LangChain Document objects.

### Steps:

1. User ask for query or called invoke method with query.
2. WikipediaRetriever passes the query to its `Wikipedia wrapper` that uses `wikipedia Python package` to communicate with wikipedia service.
3. Wikipedia searches for relevant pages based on `Wikipedia's search and article-retrieval mechanisms`.
4. The wrapper retrieves article content. It does not use any LLM to find pages.
5. LangChain converts the results into Document objects.
6. Your application receives the documents.

**Package required:** langchain_community and Wikipedia

```py
from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(
    lang="en",
    top_k_results=3,
    doc_content_chars_max=4000
)

# this is runnable thats why we have invoke method.
docs = retriever.invoke("History of India")

for i, doc in enumerate(docs, start=1):
    print(f"\nDocument {i}")
    print("Metadata:", doc.metadata)
    print("Content:", doc.page_content[:500])
```

```py

TOPIC: "LangChain framework for developing applications powered by large language models"

Answer: Given on diff topic 'Prompt engineering' and 'Lists of open-source artificial intelligence software' but something relative.

page_content Prompt engineering is the process of structuring natural language inputs (known as prompts) to produ
title Prompt engineering
--------------------------------
page_content These lists include projects which release their software under open-source licenses and are related
title Lists of open-source artificial intelligence software

TOPIC: "History of India"

Answer: exact answer is given in the page_content.

page_content Anatomically modern humans are estimated to have first arrived on the Indian subcontinent between 73
title History of India
--------------------------------
page_content The Indus Valley Civilisation, the early civilisation of India and Pakistan, developed an economy ba
title Economic history of India
--------------------------------
```

**the important point is that WikipediaRetriever searches Wikipedia for pages related to your query; it does not guarantee that the returned page will be an exact answer to your question.**

------

## Vector store Retriever

A Vector Store Retriever in LangChain is the most common type of retriever that lets you search and fetch documents from a vector store based on semantic similarity using vector embeddings.

## How It Works

1. You store your documents in a vector store (like FAISS, Chroma, Weaviate)
2. Each document is converted into a dense vector using an embedding model
3. When the user enters a query:
    . It's also turned into a vector
    . The retriever compares the query vector with the stored vectors
    . It retrieves the top-k most similar ones

## Create retriever

```py
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# as_retriever() converts your vector store into a retriever.
# k: 3 means retrieve the 3 most relevant documents for a query.

docs = retriever.invoke("What is Python?")

for doc in docs:
    print(doc.page_content)
```

## Use the built-in similarity search

This will also give same result as retriever.

```py
results = vector_store.similarity_search(
    "What is Python?",
    k=2
)

for doc in results:
    print(doc.page_content)
```

## Difference: similarity_search() vs Vector Store Retriever

**similarity_search**

- A vector store method
- Call it directly
- Search strategy:	Direct similarity search (only support this single strategy)
- Batch queries:	Not through this method's standard interface
- Integration with LangChain chains:	No

**Vector Store Retriever**

- A LangChain retriever component
- Use vector_store.as_retriever()
- Search strategy: Similarity, MMR, or score-threshold search
- Batch queries: Supports batch() because this is runnable.
- Integration with LangChain chains:	Yes because this is runnable.

## Code example

```py

books_documents: list[Document] = [
    Document(
        page_content="Ramayan is a book written by Valmiki. This is the story of Ram and his wife Sita. This is a very famous book in India.", 
        metadata={"topic": "Ramayan", "source": "notes_1"}, 
        id="doc_5"
        )
    ]

vector_store = Chroma.from_documents(
    documents=books_documents,
    collection_name="books",
    persist_directory="./chromadb", # foldername where chromedb will store.
    embedding=embedding_model
)

retriever: VectorStoreRetriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1}
)
#     search_type="mmr",
#     search_type="similarity_score_threshold",

result = retriever.invoke("Who wrote the book Ramayan?")
print('result', result[0].page_content)
# Ramayan is a book written by Valmiki. This is the story of Ram and his wife Sita. This is a very famous book in India.

result = retriever.invoke("Who wrote the book Mahabharat?")
print('result', result[0].page_content)
# Ramayan is a book written by Valmiki.

1. I asked query on Mahabharat.
2. It searches in document but not found exact anything on this query.
3. Then it finds closest document and returns.
```

By default, a similarity-based retriever tries to return the most similar documents from the vector store. It does not automatically verify that a document contains the answer to your question.

**The key distinction:** finding the closest document is not the same as finding a relevant document.

## Solution with similarity score threshold

```py

retriever: VectorStoreRetriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 1, "score_threshold": 0.8}
)
result = retriever.invoke("Who wrote the book Mahabharat?")
print('result with similarity score threshold', result[0].page_content)
# Now get Error - No relevant docs were retrieved using the relevance score threshold 0.8

```

## score_threshold range 0 to 1
```
Threshold	    Behavior

0.3	            Less strict — more documents may pass
0.5	            Moderately strict
0.8	            Strict — only higher-scoring documents pass
0.95	        Very strict — fewer documents may pass
```

-------

## LangChain: MMR Retriever

MMR stands for `Maximum Marginal Relevance`. It is a retrieval strategy that tries to return documents that are both `relevant to your query and diverse from one another`.

You already understand similarity-based retrieval and similarity score thresholds. Let's build on that knowledge.

## 1. What problem does MMR solve?

Imagine your vector store contains these five documents about LangChain:

```
Document 1 — LangChain is a framework for building LLM applications.
Document 2 — LangChain simplifies developing applications powered by large language models.
Document 3 — Developers use LangChain to integrate LLMs with external data and tools.
Document 4 — Retrievers fetch relevant documents from a knowledge base.
Document 5 — Langchain Memory helps applications retain conversation context.
```

Your query is:

> Explain LangChain and its main capabilities.

You ask the similarity-based retriever for three documents.

It might return Documents 1, 2, and 3 because all three are highly similar to your query.

**The problem?** They contain `overlapping` information. You could have retrieved more useful information about retrievers and memory instead.

This is the problem MMR tries to solve: redundant results.

## 2. How does MMR work?

MMR considers two things when selecting documents:

1. Relevance: How similar is the document to the user's query?
2. Diversity: How different is the document from documents already selected?

It tries to balance these two factors.

It might return Documents 1, 4, and 5 folling above two relevance and diversity.

## MMR Code

```py

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3, # Number of final documents returned
        "fetch_k": 10, # Number of candidate documents considered before MMR selection
        "lambda_mult": 0.5 # 0.0, 0.5, 1.0 - Balances relevance and diversity
    }
)

result = retriever.invoke(
    "Explain LangChain and its main capabilities"
)

for doc in result:
    print(doc.page_content)
    print("---")
```

------------    

# FAISS Vector store

The main difference b/w FAISS & Chroma is that `FAISS is primarily a vector-search library`, while `Chroma provides a database with named collections`.

FAISS creates an `in-memory vector index` and associates it with the document store. You don't need a collection name because this index object itself represents your current set of vectors and documents.

## Required package

**langchain-community** - Provides the integration that lets you use FAISS through a familiar LangChain interface.

**faiss-cpu** - The Python-installable package that provides FAISS functionality using your CPU.

```
pip install -U langchain-community
pip install -U faiss-cpu
```

## Create store

```py
# Without save_local()
# Default storage -  In memory
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

# With save_local()
vector_store = FAISS.from_documents(documents, embeddings)
vector_store.save_local("my_faiss_index") #directory name
```

**Compare the two:**

| Feature                   | FAISS                           | Chroma                                                  |
| ------------------------- | ------------------------------- | ------------------------------------------------------- |
| Collection name required? | No                              | When using named collections, yes                       |
| Default storage           | In memory                       | Persistent or in memory, depending on configuration     |
| Multiple collections      | Create separate indexes/objects | Create named collections                                |
| Save data to disk         | Explicitly save the index       | Can persist automatically with persistent configuration |
| Search                    | Vector similarity search        | Vector similarity search                                |

## How does FAISS store your documents?

1. The embedding model converts each document into a numerical vector.
2. FAISS adds those vectors to its search index.
3. LangChain maintains a mapping between index entries and the original Document objects, including their metadata.
4. IF you skip directory name (means skip `save_local()`) - `index remains in memory (RAM)`. It is not automatically saved to a directory.
    - You can search it while the Python process and object remain available.
    - If the Python process ends and the object is lost, you cannot recover that index from disk unless you
      saved  it separately.
    - The document embeddings and index are recreated every time you rebuild the vector store this way.
5. If you provide a directory name, `FAISS saves the index files inside the [directory_name]` relative to your current working directory.
    - This saves the FAISS index and its associated document data to disk.
    - Next time, instead of recreating the index from the documents, load the saved index.
    - The original documents do not need to be embedded again when you load the saved index.
6. Load saved index & retrieve document.


## Store data permanently in directory

You can save the FAISS vector store to a directory yourself:

```py
vector_store.save_local("my_faiss_index")

# load
loaded_vector_store = FAISS.load_local(
    "my_faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)
```

**Security note:** Only load a saved FAISS store using `allow_dangerous_deserialization=True` when you trust the files. The saved document store can use Python pickle deserialization, which can execute malicious code.

## 4. How would you separate Notes and Books in FAISS?

You could create two independent indexes:

```py
# pass notes documents - it will crete notes Index 
notes_store = FAISS.from_documents(
    documents=notes_documents,
    embedding=embeddings
)

# pass books documents - it will create seperate books index
books_store = FAISS.from_documents(
    documents=books_documents,
    embedding=embeddings
)
```

Now `notes_store` searches Notes, and `books_store` searches Books.

**Remember:** In Chroma, you can organize data into named collections within a database. In FAISS, you typically manage separate index objects and decide how and where to save them.

---------

# Multi query Retriever

Sometimes a single query might not capture all the ways information is phrased in your documents.

For example:

**Query:** "How can I stay healthy?" (this is very broad query and could have multiple queries.)

Could mean:

. What should I eat?
. How often should I exercise?
. How can I manage stress?

MultiQuery Retriever uses an `LLM to generate multiple alternative queries`, searches with those queries, and combines the retrieved documents.

1. Takes your original query
2. Uses an LLM (e.g., GPT-3.5) to generate multiple semantically different versions of that query
3. Performs retrieval for each sub-query
4. Combines and deduplicates the results


## Package required -

langchain_classic

```py
# older way before langchain-1.x
from langchain.retrievers.multi_query import MultiQueryRetriever

# below is new way to import MultiQuery Retriever
from langchain_classic.retrievers import MultiQueryRetriever
```

## Code example

```py

# create and add docs
vector_store: FAISS = FAISS.from_documents(
    documents=documents,
    embedding=embeddings_model
)

# directory name to save faiss index and docs
vector_store.save_local('faiss-vector-store')

# create base retriever object
base_retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs = {'k': 3}
)

# now create llm model for multi query retriever
llm_model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",  
    max_output_tokens=100, 
    google_api_key=GOOGLE_API_KEY,
    timeout=20,
    max_retries=0
    )

# create multi query retriever
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm= llm_model
)

results = multi_query_retriever.invoke("How can I preserve previous chat messages in an LLM application?")

print('Results len:', len(results))

for doc in results:
    print("Content:", doc.page_content)
    print("---")
```

## Workflow to generate final result - 

1. We have provided k = 3 in our base_retriever, This means each search retrieves up to 3 documents.
2. Then you pass that retriever into MultiQueryRetriever. 
3. The LLM generates multiple alternative queries.
4. Each query is sent to base_retriever.
5. Each search can return up to 3 documents.
6. MultiQueryRetriever combines the results and removes duplicate documents.
7. Then It prints finally unique documents and that could be greather then or less then 3 (defined k value).

## How to get or print generated Queries 

To see the queries generated by MultiQueryRetriever, We need to enable `logging`.

MultiQueryRetriever API doesn't expose them as a separate return value. Logging is the simplest way to inspect them without modifying the retriever.

MultiQueryRetriever — already contains logging statements that report the generated queries.

```py

import logging

logging.basicConfig()
logging.getLogger("langchain_classic.retrievers.multi_query").setLevel(logging.INFO)
```
------