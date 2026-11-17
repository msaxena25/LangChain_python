# Libraries used

Scanned from `Langchain_Code`, `Projects`, and `Python-Code`. Local project files are not listed.

## Built-in

**abc** (In built) - Define abstract base classes and required methods.

**array** (In built) - Store compact lists of numbers of one type.

**datetime** (In built) - Work with dates, times, and time zones.

**decimal** (In built) - Do exact decimal math, useful for money.

**enum** (In built) - Create a set of named constant values.

**importlib** (In built) - Load a Python module dynamically by file path.

**json** (In built) - Convert Python data to and from JSON text.

**logging** (In built) - Write log messages while a program runs.

**os** (In built) - Read environment variables and work with the operating system.

**pathlib** (In built) - Build and check file and folder paths.

**random** (In built) - Pick random numbers and random choices.

**re** (In built) - Search and match text with regular expressions.

**sqlite3** (In built) - Create and query a local SQLite database.

**sys** (In built) - Read interpreter details such as the module search path.

**textwrap** (In built) - Wrap long text onto shorter lines.

**threading** (In built) - Run functions at the same time in separate threads.

**time** (In built) - Pause execution and measure elapsed time.

**typing** (In built) - Add type hints such as Annotated, Literal, and Any.

**uuid** (In built) - Generate unique IDs.

## Third-party

**langchain** - Build chains, agents, and other LLM application pieces.

**langchain-anthropic** - Call Anthropic Claude chat models.

**langchain-chroma** - Store and search document embeddings in Chroma.

**langchain-classic** - Use classic agents, hub prompts, and retrievers.

**langchain-community** - Load documents and use community tools and vector stores.

**langchain-core** - Share prompts, messages, tools, runnables, and output parsers.

**langchain-experimental** - Split text with experimental tools such as semantic chunking.

**langchain-google-genai** - Call Google Gemini chat models and embedding models.

**langchain-huggingface** - Call Hugging Face chat models and inference endpoints.

**langchain-ollama** - Call chat models running in Ollama.

**langchain-openai** - Call OpenAI completion and chat models.

**langchain-text-splitters** - Split long documents into smaller chunks for retrieval.

**langsmith** - Fetch prompts and work with the LangSmith client.

**ollama** - Talk to a local Ollama server from Python.

**pydantic** - Validate data and describe structured model fields.

**pypdf** - Read text out of PDF files.

**python-dotenv** - Load API keys and settings from a `.env` file.

**requests** - Send HTTP requests to web APIs.

**scikit-learn** - Compare embedding vectors with cosine similarity.

**typing-extensions** - Use newer typing features such as TypedDict.

**youtube-transcript-api** - Download the transcript of a YouTube video.

## Required, not imported directly

These are not imported in the project files. A LangChain class loads them when that code runs, and they are not installed with the LangChain packages above.

**beautifulsoup4** - Parse HTML pages loaded by WebBaseLoader.

**ddgs** - DuckDuckGo search client used by DuckDuckGoSearchRun.

**faiss-cpu** - Similarity search library used by the FAISS vector store.

**wikipedia** - Wikipedia client used by WikipediaRetriever.
