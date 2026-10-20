
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

\- Flat (Brute-Force) Search: Compares the query against every stored vector. It provides exact nearest-neighbor results but can be slow for large datasets.

\- HNSW (Hierarchical Navigable Small World): Builds a graph connecting nearby vectors and navigates that graph to find similar vectors quickly. It generally provides a good balance between speed and search accuracy.

\- PQ (Product Quantization): Compresses vectors into smaller representations to reduce memory usage. It can be combined with IVF or other search methods to make large-scale vector search more efficient.

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

# similarity_search with score - similarity_search_with_score
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