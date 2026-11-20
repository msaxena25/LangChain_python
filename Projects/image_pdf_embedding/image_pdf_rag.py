from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers import RapidOCRBlobParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Required package - pip install -U rapidocr-onnxruntime

# PDF Loader with image extraction with RapidOCRBlobParser

loader = PyPDFLoader(
    "Projects/image_pdf_embedding/spacecraft-pdf.pdf",
    mode='page',
    extract_images=True,
    images_parser=RapidOCRBlobParser()
    )

'''
# Use PyMuPDFLoader with both table extraction and image OCR.

# required package - pymupdf, rapidocr

loader = PyMuPDFLoader(
    file_path="Projects/image_pdf_embedding/spacecraft-pdf.pdf",
    mode="page",
    extract_images=True,
    images_parser=RapidOCRBlobParser(),
    extract_tables="markdown"
)
'''


docs = loader.load()

# for doc in docs:
#     print(doc.page_content)
#     print("--------------------------------")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80
)
chunks = text_splitter.split_documents(docs)

embedding_model = OllamaEmbeddings(model="dengcao/Qwen3-Embedding-0.6B:Q8_0")

vector_store = FAISS.from_documents(chunks, embedding_model)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 4},
    search_type="similarity"
)

prompt = PromptTemplate(
    template="""
    You are a helpful assistant that can answer questions about the following text:
    {context}
    Question: {query}
    Answer the question based on the context provided.
    If you don't know the answer, just say "I don't have answer in provided document".
    """,
    input_variables=["context", "query"]
)

llm_model = ChatOllama(model="llama3.1:8b", temperature=0.2)
chain = prompt | llm_model | StrOutputParser()

while True:
    query = input("Enter your question: ")
    if query == "exit":
        break
    else:
        docs = retriever.invoke(query) 
        context = "\n".join([doc.page_content for doc in docs])
        print("🚀mohit ~ context:", context)
        result = chain.invoke({
            "context": context,
            "query": query
        })
        print(result)











'''
# How RapidOCRBlobParser works - step by step

1. PDF Loader reads the PDF: PyPDFLoader or PyMuPDFLoader opens the PDF and reads its pages.

2. Extracts normal text: The loader extracts selectable text from each page.

3. Extracts embedded images: When extract_images=True, the loader extracts images from the PDF.

4. Passes images to RapidOCRBlobParser: Each extracted image is passed as an image blob to the OCR parser.

5. OCR processes the image: RapidOCR detects text inside the image and converts it into machine-readable text.

6. Returns extracted text: The OCR parser returns the extracted text to the loader.

7. Combines the text: The loader combines normal PDF text and OCR-extracted image text into the page's page_content.

8. Creates LangChain Documents: The loader returns Document objects containing the extracted text and page metadata.


# retriever.invoke(query)

it first converts your query into an embedding vector and then searches for similar document embeddings 
in the vector store.



'''