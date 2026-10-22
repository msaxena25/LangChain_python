# RAG

You've now learned the four important building blocks of RAG:

1. Document loaders — load data from PDFs, text files, websites, and other sources.
2. Text splitters — divide documents into manageable chunks.
3. Vector stores — store document embeddings and support similarity search.
4. Retrievers — find relevant documents for a user's query.

Now let's connect these components into a complete RAG application.

RAG is a technique in which an LLM retrieves relevant information from an external knowledge source and uses that information to generate an answer.

## What is parameterized knowledge?

`Parameterized knowledge` is the information and patterns a model learns during training and represents through its learned `parameters` (weights).

Let's understand this with a simple example.

Suppose you ask an LLM:

> Who wrote the Ramayana?

The model answers:

> The Ramayana is traditionally attributed to Valmiki.

Where does this information come from if you haven't provided a document or used RAG?

It may have learned this association during training. That learned information is part of its parameterized knowledge.

## How is knowledge stored in parameters?

A neural network contains many numerical values called `parameters` or `weights`. During training, these values are adjusted to help the model predict the correct next tokens.

```
Model	        Parameter count
GPT-3              175 B
GPT-2               1.5 B
Llama 2 7B         7 Billion
```

## How can access this information?

A user can access information encoded in an LLM's parameters by `asking questions through a prompt`.

When this prompt or query goes to LLM, LLM use their saved parametric knowledge, process it and return response.

## why an LLM alone is not enough for a real-world application

### Scenario 1: Private company documents

A general LLM cannot answer reliably from private documents it has never been given access to. It might give a generic answer based on its training, but that doesn't mean it knows your company's actual policy.

### Scenario 2: Today's news or recent information

A model's training data has a cutoff or coverage limitation. It cannot reliably know events that happened after its training.

### Scenario 3: Hallucination

Example: “Did Einstein play football for Germany in his early years?”

An LLM may confidently generate a false answer because it predicts plausible text rather than automatically verifying every claim against reality. A confident tone is not evidence that the answer is true.

## Fine tuning

Fine-tuning means taking an already-trained LLM and training it further on a `specific dataset` so that it becomes better suited to a particular task or way of responding.

You don't usually train a model from scratch. You start with an existing model and adapt it.

## How does fine-tuning work?

1\. Choose a pre-trained model: An existing LLM

2\. Prepare training data: Input examples + expected outputs

3\. Run fine-tuning: Update model weights to learn the examples

4\. Evaluate the model: Test accuracy, consistency and unwanted regressions

5\. Deploy the adapted model

During training, the model compares its predictions with the expected outputs and adjusts its trainable parameters to reduce the error. After training, the adapted model can be used for inference like other LLMs.

## How much training data is required?

There is no universal minimum. It depends on the task, the quality of your examples, the base model, and how much improvement you need.

OpenAI API

| Dataset size              | What it can be useful for                                  |
| ------------------------- | ---------------------------------------------------------- |
| 10–50 examples            | Small proof of concept                                     |
| 50–200 examples           | Testing a specific behavior or output format               |
| Hundreds to thousands     | More coverage of real-world variations                     |
| Tens of thousands or more | Larger or more diverse tasks, if the additional data helps |

These are rough planning ranges, not strict thresholds.

## What should the training data look like?

A common format for chat-model supervised fine-tuning is `JSONL`: one JSON training example per line.

For example, a file named `training_data.jsonl` could contain:

```jsonl
{"messages":[{"role":"user","content":"I can't log in."},{"role":"assistant","content":"{\"category\":\"AUTHENTICATION\"}"}]}
{"messages":[{"role":"user","content":"My payment was deducted twice."},{"role":"assistant","content":"{\"category\":\"BILLING\"}"}]}
{"messages":[{"role":"user","content":"The app crashes on startup."},{"role":"assistant","content":"{\"category\":\"TECHNICAL_ISSUE\"}"}]}
```

So provided such JSONL data is called `Supervised fine tuning method (SFT)` where we give data in labelled format like above.

## How can you implement fine-tuning?

There are two main routes.

### Option A: Fine-tuning through a hosted API

You upload your prepared dataset, choose a supported base model, submit a training job, and use the resulting model through an API.

Advantages: Less infrastructure management; easier deployment.

Trade-offs: Provider-dependent pricing, model availability, data policies, and limits.

### Option B: Fine-tune an open-weight model

Download or load a supported model and train it using Python libraries such as Hugging Face Transformers and PEFT.

Advantages: More control over the model, training process, and deployment.

Trade-offs: You need compatible hardware or rented GPU compute, and more setup and troubleshooting.

## Main fine-tuning methods

| Method                 | What it means                                                                             | Resource requirement      |
| ---------------------- | ----------------------------------------------------------------------------------------- | ------------------------- |
| Full Fine-Tuning (FFT) | Updates all model parameters                                                              | High                      |
| LoRA                   | Freezes original weights and trains small, additional low-rank matrices                   | Lower                     |
| QLoRA                  | Loads the base model in low-bit quantized form, typically 4-bit, and trains LoRA adapters | Lower still in many cases |
| Adapter tuning         | Adds small trainable modules to the model                                                 | Lower                     |
| Prompt tuning          | Trains virtual prompt embeddings while keeping the main model frozen                      | Low                       |        |

## Tools and libraries to implement them

**Hugging Face Transformers:** Loads models, tokenizers and datasets, and provides training workflows. Often used with PEFT for LoRA and QLoRA.

**Hugging Face PEFT:** Implements parameter-efficient methods such as LoRA, AdaLoRA, IA³, prompt tuning and prefix tuning.

**Unsloth:** Provides optimized training workflows designed to make fine-tuning supported models more memory- and compute-efficient.

-------

# Continued Pre-Training (CPT)

`Continued Pre-Training (CPT)` means taking an already pre-trained LLM and training it further on additional text, usually using the same or a similar objective used during its original pre-training. This method is also called as `Unsupervised tuning method`.

**Original pre-training:** The model learns general language and knowledge from a large text corpus.
**Continued pre-training:** You train a model further on a large collection of banking documents, reports, and technical material.
**Result: **The model may become more familiar with banking language and concepts.

## data example

```txt
A mortgage is a loan used to purchase property.
The borrower repays the loan according to the agreed terms.
```

----------

# RLHF (Reinforcement Learning from Human Feedback)

`RLHF` (Reinforcement Learning from Human Feedback) is a fine-tuning approach that uses human preferences to help an LLM produce better responses.

RLHF (Reinforcement Learning from Human Feedback) is a fine-tuning approach that uses human preferences to help an LLM produce better responses.

### How it works

1. SFT: First, train the model on example questions and good answers.
2. Human feedback: Humans compare different responses and choose which is better.
3. Reward model: A model learns to predict which responses humans prefer.
4. Reinforcement learning: The LLM is optimized to produce responses that receive higher reward scores.

### Example

User asks: “Explain AI simply.”

- Response A: A complex explanation full of technical jargon.
- Response B: A simple explanation with a practical example.

A human prefers Response B. Feedback helps train the reward model, and reinforcement learning can then encourage the LLM to produce more responses like B.

Remember: RLHF is not the same as JSONL, LoRA, or QLoRA. RLHF describes a `preference-based training approach`; JSONL is a data format, while LoRA and QLoRA are parameter-efficient training techniques.

---------

# Challenges of Fine-Tuning an LLM

1. High cost — GPU compute, training, and deployment can be expensive.
2. Large data requirements — Collecting enough high-quality training examples can be difficult.
3. Data quality — Incorrect or inconsistent examples can teach the model undesirable behavior.
4. Technical complexity — Requires knowledge of training, models, datasets, and hardware.
5. Catastrophic forgetting — The model may lose some previously learned capabilities.
6. Hallucinations — Fine-tuning does not guarantee factual accuracy or eliminate hallucinations.
7. Knowledge updates — Updating frequently changing facts requires repeated training if relying on model weights alone.
8. Limited generalization — The model may perform well on training examples but poorly on unfamiliar inputs.
9. Evaluation difficulty — Measuring whether fine-tuning genuinely improved results can be challenging.
10. Overfitting — The model may memorize training examples rather than learn general patterns.
11. Training time — Larger models and datasets can take substantial time to train.
12. Model maintenance — New requirements or data may require additional training and evaluation.
13. Privacy and security — Sensitive training data may be memorized or exposed through model outputs.
14. Model compatibility — Not every model supports every fine-tuning method or hardware configuration.
15. No guaranteed improvement — Fine-tuning may not outperform a good prompt or RAG pipeline.

Key takeaway: Fine-tuning is most useful when you need to improve a model's behavior or specialized task performance—not as the default solution for accessing private or frequently changing information.

---------

# In-context learning (ICL)

In-context learning is the ability of an LLM to perform a task by using instructions or examples provided in the current prompt, without updating its model parameters. It became widely known through `the GPT-3 research paper, Language Models are Few-Shot Learners, published in 2020`.

In-context learning (ICL) can avoid many fine-tuning costs and complexities, but it cannot solve all fine-tuning problems or all LLM limitations.

Instead of updating model weights, you provide instructions, examples, or relevant information directly in the prompt.

| Fine-tuning challenge                   | Can ICL help?                                                            |
| --------------------------------------- | ------------------------------------------------------------------------ |
| Training cost and GPU requirements      | ✅ Avoids a separate training process                                     |
| Collecting a large training dataset     | ✅ Often needs only a few examples                                        |
| Updating model weights                  | ✅ No weight updates required                                             |
| Adapting to a new task                  | ✅ Often, through instructions and examples                               |
| Catastrophic forgetting from training   | ✅ Avoids this training-related risk                                      |
| Accessing private company documents     | ⚠️ Only if relevant documents are supplied securely; RAG is often better |
| Accessing today's news                  | ⚠️ Needs current information supplied through search or another tool     |
| Hallucinations                          | ❌ Can still occur                                                        |
| Limited context window                  | ❌ The prompt has a size limit                                            |
| Consistent performance on complex tasks | ⚠️ Depends on the model, examples, and task                              |

### Example

With in-context learning:

You provide examples in the prompt:

```
Classify support tickets using these categories.

Example 1:
Input: "I cannot log in."
Output: AUTHENTICATION

Example 2:
Input: "My payment failed."
Output: BILLING

Now classify:
Input: "The application crashes on startup."
Output:
```

The model can infer the expected pattern and respond with `TECHNICAL_ISSUE`—without any fine-tuning.

This is called `few-shot learning` because you provide a few examples in the prompt. With no examples, it is called zero-shot learning if you rely on instructions alone.

----------

# Emergent Property

`Emergent` means something that appears or develops as a result of different parts working together, rather than being a property of one part alone.

Hindi meaning: उभरकर सामने आने वाला / विकसित होकर प्रकट होने वाला।

An `emergent property` is a characteristic or `ability` that appears when different - different individual parts interact, even though the individual parts don't have that same property on their own.

**In-context learning (ICL)** has been described as an emergent ability of large language models. ICL became notably apparent in large language models such as` GPT-3`, especially in few-shot learning.

-------

## Context-grounded prompting

Instead of few shot prompting, If we directly pass whole Context with prompt and them LLM generate answers based on this context. This is generally called `context-grounded prompting`or context-based question answering.

Example - 

```
Context:
Our company provides 24 days of annual leave to employees.

Question:
How many annual leave days do employees receive?

Answer using only the provided context.
```

**And this way is actually called RAG.**

## Diff b/w ICL & Context grounded prompting

| In-context learning (ICL)                                      | Context-grounded prompting                                          |
| -------------------------------------------------------------- | ------------------------------------------------------------------- |
| Teaches the model a `task pattern` using examples in the prompt. | Provides facts or information for answering a question.             |
| Usually uses input/output examples (few-shot).                 | Usually uses documents, data, or factual context.                   |
| Example: Show 3 examples of ticket classification.             | Example: Provide a company leave policy and ask about annual leave. |
| No model weight updates.                                       | No model weight updates.                                            |

-----


## RAG — Retrieval-Augmented Generation

1\. Retrieval

Find relevant information from an external knowledge source based on the user's question.

2\. Augmentation

Add the retrieved information to the prompt along with the user's question.

3\. Generation

The LLM uses the question and supplied context to generate an answer.

**Important:** In the LangChain workflow you've been learning, the retriever handles retrieval, the prompt template combines the question with retrieved context, and the LLM performs generation.

----

## Indexing

Indexing is the process of preparing your knowledge base so that it can be efficiently searched at query time. And it involves 4 sub steps.

1. Document Loader
2. Text splitting
3. Embedding generation 
4. Vector store

----------

# YouTube Chatbot using RAG — Python

## Requirement

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

## Install required packages

Run this in your notebook:

```
pip install -U langchain langchain-community langchain-google-genai langchain-text-splitters faiss-cpu youtube-transcript-api python-dotenv
```

We'll use:

- `YouTubeTranscriptApi` to fetch the transcript.
- `RecursiveCharacterTextSplitter` to split the transcript.
- `GoogleGenerativeAIEmbeddings` to convert chunks into vectors.
- `FAISS` to store and search those vectors.
- `as_retriever()` to retrieve relevant chunks.
- `ChatGoogleGenerativeAI` and `PromptTemplate` to generate the answer.
- LangChain's Runnable components to connect everything into one chain.

## Complete RAG application Code

```
Langchain-code\14.class-youtube-chatbot-rag.py
```

----------

# YouTube RAG chatbot — HLD and LLD

This is the same application as `Langchain-code/14.class-youtube-chatbot-rag.py`, written the way an interview expects: first the shape of the system (HLD), then the exact wiring with the watch-story video as the example (LLD).

Video: `https://www.youtube.com/watch?v=7aEAS5E5vjg`  
Question used in the script: `What lession Father wanted to teach his Son?`

```
INDEXING  (once per video, before any question)
video id
  -> YouTubeTranscriptApi.fetch
  -> join snippet text into one string
  -> RecursiveCharacterTextSplitter
  -> GoogleGenerativeAIEmbeddings
  -> FAISS

QUERY  (every question, one .invoke())
question string
  -> retriever (similarity, k = 6)
  -> join chunk text into context
  -> PromptTemplate(context + question)
  -> ChatGoogleGenerativeAI
  -> StrOutputParser
  -> { question, answer }
```

## HLD — high level design

1. **Fix the job of the system.**  
   The chatbot answers questions about one YouTube video, and the only allowed source is that video's transcript. The LLM is used to read and phrase an answer. It is not used as the source of facts about the video. That is why this is RAG and not a plain Gemini call, and why it is not fine-tuning: the knowledge changes with every video id, and we do not want to retrain weights to learn one story.

2. **Split the system into indexing and query.**  
   Indexing prepares the video so it can be searched. Query answers one user question from that index. Indexing runs when the script starts. Query runs on `final_chain.invoke(...)`. In an interview, draw these as two pipelines that share the vector store. Rebuilding the index on every question would repeat the embedding API cost for the same transcript.

3. **Take the transcript as the knowledge source.**  
   `YouTubeTranscriptApi.fetch(video_id)` returns caption snippets (`text`, `start`, `duration`). Captions are already text, so we do not download audio or run speech-to-text. `YoutubeLoader` from `langchain_community` can do this in one call and return LangChain `Document`s. We called the transcript API directly so we can see each snippet, catch `TranscriptsDisabled`, and decide how the text is joined before it becomes documents.

4. **Make chunks the unit of search, not the whole transcript and not each caption line.**  
   Caption lines are a few words (`"Oneday the man decided to teach his son"`). Embedding each line would lose the story. Putting the full transcript into every prompt would work for this short video, and it would also send irrelevant sentences, cost more tokens, and hit the context window on a long video. We join the snippets, then split them into overlapping chunks. Search returns a few chunks. The prompt sees only those chunks.

5. **Embed the chunks and store the vectors in FAISS.**  
   `GoogleGenerativeAIEmbeddings` (`gemini-embedding-001`) turns each chunk into a vector. FAISS keeps those vectors in memory and answers "which chunks are closest to this question?". FAISS fits this design because the corpus is one short transcript, it runs locally, and it needs no separate database server. A hosted store (Chroma server, pgvector, Pinecone) is the follow-up when many videos must survive process restarts or be shared across API workers. The chat model and the embedding model both use `GOOGLE_API_KEY`, so the script has one provider.

6. **Retrieve a small neighborhood of chunks per question.**  
   The retriever is FAISS similarity search with `k = 6`. The question vector is compared with chunk vectors, and the six nearest chunks become the context. We use plain similarity because a short story's answer is often spread across neighboring sentences, and those neighbors are useful. MMR is the alternative when a long video repeats the same point and you want diverse chunks. A score threshold is the alternative when you would rather return nothing than a weakly related chunk.

7. **Augment a grounded prompt, then generate.**  
   Retrieval finds text. Augmentation places that text and the user question into a `PromptTemplate`. Generation is `ChatGoogleGenerativeAI` (`gemini-3.5-flash-lite`). The template tells the model to answer from the context only, and to say `I couldn't find the answer in this video's transcript.` when the context does not contain the answer. That sentence is the hallucination control. `max_output_tokens=500`, `timeout=20`, and `max_retries=2` keep one answer short and bounded.

8. **Hide the query path behind one chain.**  
   The prompt needs two inputs, `context` and `question`. The retriever accepts only the question and returns `list[Document]`. `RunnableParallel` is the piece that solves that mismatch: one branch keeps the question (`RunnablePassthrough`), the other branch retrieves and joins document text. `prompt | llm | parser` then runs as a normal sequence. The caller writes `final_chain.invoke(question)` and does not call retrieve, format, prompt, and generate by hand.

9. **Return the question with the answer.**  
   An outer `RunnableParallel` runs the RAG chain and also forwards the original question. The result is `{"question": "...", "answer": "..."}`. The inner chain still does the real work. The outer chain only shapes the response so a caller can see which question produced the answer.

10. **Treat retrieval quality as part of the design.**  
    With `chunk_size=200`, `chunk_overlap=50`, and `k=5`, the retrieved context contained the setup (father, watch, market) and missed the moral. The model followed the prompt and said the deeper lesson was not in the context. With `chunk_size=500`, `chunk_overlap=80`, and `k=6`, the context included the old shopkeeper's lines about time, and the answer became the real lesson. Same LLM, same prompt. The index and the retriever decided whether the answer was possible.

## LLD — low level design

Same video, same question, in code order. Models are created once, above the chain, so a question does not construct a new client.

### 1. Load the key and create the two models

`load_dotenv()` reads `GOOGLE_API_KEY`.

```python
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY,
)

llm_model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=GOOGLE_API_KEY,
    max_output_tokens=500,
    max_retries=2,
    timeout=20,
)
```

Example: both objects exist before `VIDEO_ID` is fetched. Indexing uses only `embedding_model`. Query uses `embedding_model` again inside FAISS (to embed the question) and `llm_model` to write the answer.

Why these models: one Google key for vectors and for chat. `gemini-embedding-001` is the embedding model. `gemini-3.5-flash-lite` is a small, fast chat model, which is enough when the facts are already in the prompt. A larger chat model would not recover a moral that retrieval never fetched.

### 2. Fetch the transcript by video id

```python
VIDEO_ID = "7aEAS5E5vjg"
youtube_api_obj = YouTubeTranscriptApi()
video_transcipt = youtube_api_obj.fetch(VIDEO_ID)
```

Example snippet:

```text
FetchedTranscriptSnippet(
    text="Oneday the man decided to teach his son",
    start=14.08,
    duration=6.16,
)
```

`TranscriptsDisabled` is the failure path: no captions, stop. There is no vector store and no LLM call.

`YoutubeLoader(video_id=..., language=["en"]).load()` is the shorter LangChain path. It returns `Document`s immediately. We skipped it here because the raw snippets make the next join step visible, and the exception is explicit. The loader is the right choice when you only want documents and do not need `start` / `duration`.

### 3. Join snippet text into one string

```python
transcript_full_string = " ".join(
    snippet.text for snippet in video_transcipt.snippets
)
```

Example:

```text
Once upon a time there lived a man in a small village. He was very worried about his son. ... So use your time wisely.
```

Input is many tiny snippets. Output is one string. `start` and `duration` are dropped at this join. The chatbot can answer "what lesson" and cannot answer "at what timestamp" unless we keep that metadata on each `Document`. That is a deliberate scope cut for this script.

### 4. Split the string into overlapping documents

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=80,
)
documents = text_splitter.create_documents([transcript_full_string])
```

Example shape of one chunk:

```text
Document(
    page_content="Oneday the man decided to teach his son a lesson. ... Ask everyone you meet how much they think it is worth.",
    metadata={},
)
```

`create_documents([one_string])` returns `list[Document]`. `chunk_size=500` is about 500 characters, not 500 tokens. `chunk_overlap=80` copies the tail of one chunk into the head of the next, so a sentence that sits on the cut still appears in a chunk.

`RecursiveCharacterTextSplitter` tries larger separators first (paragraph, line, space) and only then cuts characters. A spoken transcript joined with spaces has almost no paragraphs, so the splitter mostly breaks on spaces and stays off the middle of a word. `CharacterTextSplitter` uses one separator only. A token splitter tracks the model limit more closely and is harder to read while tuning. Character size was enough to see the quality change in step 10 of the HLD.

The first draft of the requirement used `chunk_size=1000` and `chunk_overlap=200`. The script uses `500` and `80` because that setting, with `k=6`, is the one that returned the moral.

### 5. Embed the documents and build FAISS

```python
vector_store = FAISS.from_documents(
    documents=documents,
    embedding=embedding_model,
)
```

Example:  document text goes to `gemini-embedding-001`, the vector is stored next to that text, and FAISS can search it. `from_documents` both embeds and builds the index. There is no `save_local` in this script, so the index lives until the process ends. Running the file again refetches the transcript and pays for embeddings again. `FAISS.save_local` / `FAISS.load_local` is the persistence step when the same video is queried many times.

### 6. Turn the vector store into a retriever

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 6},
)
```

Example call, before the chain exists:

```python
retriever.invoke("What lession Father wanted to teach his Son?")
# -> 6 Document objects, the nearest chunk texts
```

Input is a string. Output is `list[Document]`, not a prompt and not an answer. `k=6` is wide enough for this story to include both the father's instruction and the shopkeeper's explanation. `search_type="similarity"` is nearest-neighbor search over the FAISS vectors.

### 7. Write the prompt that performs augmentation

```python
prompt_template = PromptTemplate(
    template='''You are a YouTube video assistant.
    Provide answer based on given context only.
    If the answer is not available in the context, say:
    "I couldn't find the answer in this video's transcript."

    Context: {context}
    User Question: {question}
    ''',
    input_variables=["context", "question"],
)
```

Example after formatting:

```text
Context: ... you cannot put a price on time. You can give millions of rupees, but you cannot buy back even one second of your life. ...
User Question: What lession Father wanted to teach his Son?
```

`PromptTemplate` is a single string with two placeholders. That matches this app: no chat history, no system/human message list. `ChatPromptTemplate` is the next step when you add a separate system message or prior turns. The fallback sentence is what made the small-chunk run honest: the model reported that the moral was missing instead of inventing it.

### 8. Flatten retrieved documents into the context string

```python
format_retrieved_docs = lambda retrieved_docs: " ".join(
    doc.page_content for doc in retrieved_docs
)
```

Example:

```text
input:  [Document(...watch...), Document(...old man...), ...]
output: ".... took out the watch ... you cannot put a price on time. ..."
```

The retriever returns objects. The prompt placeholder `{context}` needs a string. The lambda is left as a normal function. LCEL wraps a callable in `RunnableLambda` when it is used with `|`. An explicit `RunnableLambda` is the same thing, written out.

Joining with a space removes chunk boundaries. Generation still works. If the product must cite a chunk or a timestamp, the formatter should keep separators and the metadata we dropped in step 3.

### 9. Build the parallel step that feeds the prompt

```python
context_chain = RunnableParallel({
    "question": RunnablePassthrough(),
    "context": retriever | format_retrieved_docs,
})
```

Example input:

```text
"What lession Father wanted to teach his Son?"
```

Example output:

```python
{
    "question": "What lession Father wanted to teach his Son?",
    "context": "<the six chunks joined into one string>",
}
```

This is the LLD detail interviews push on. `RunnableParallel` gives the same input to every branch.

- `RunnablePassthrough()` copies that string into `question`.
- `retriever | format_retrieved_docs` embeds the same string, fetches 6 documents, and joins their `page_content` into `context`.

A plain `retriever | prompt_template` cannot do this. The retriever's output replaces the input, so the prompt would receive `list[Document]` and would lose the original question. The parallel step is how both values arrive together, which is what `input_variables=['context', 'question']` requires.

The chain's contract is a string. `final_chain.invoke("...")` matches that. Passing `{"question": "..."}` would forward the dict into the retriever and into `{question}`.

### 10. Connect augmentation and generation

```python
parser = StrOutputParser()
chain = context_chain | prompt_template | llm_model | parser
```

Example data at each pipe:

| Step | Value |
| --- | --- |
| `context_chain` | `{"question": "...", "context": "..."}` |
| `prompt_template` | one formatted prompt string |
| `llm_model` | `AIMessage(content="Based on the provided context, ...")` |
| `parser` | that content as a plain `str` |

`StrOutputParser` is there because the rest of the app wants a string. The chat model returns a message object.

`chain` is the RAG pipeline. Older `RetrievalQA` hid this wiring inside one class. LCEL keeps retrieve, format, prompt, model, and parse as separate runnables, so each one can be swapped or printed. That is why the script uses this chain.

### 11. Add an outer parallel for the response shape

```python
final_chain = RunnableParallel({
    "question": RunnablePassthrough(),
    "answer": chain,
})
```

`RunnableParallel` again passes the original string to both branches. `question` is the raw string. `answer` is the full inner chain: retrieve, prompt, Gemini, parse.

### 12. Run the whole query with one invoke

```python
result = final_chain.invoke(
    "What lession Father wanted to teach his Son?"
)
```

Example result with `chunk_size=500`, `chunk_overlap=80`, `k=6`:

```python
{
    "question": "What lession Father wanted to teach his Son?",
    "answer": "Based on the provided context, the father wanted to teach his son about the real value of time, helping him understand that \"you cannot put a price on time,\" that you cannot buy back even one second of your life, and that he must use his time wisely instead of being lazy and careless.",
}
```

Example result with the weaker index (`chunk_size=200`, `chunk_overlap=50`, `k=5`): the answer described the watch and the market, then said the context never states the moral. The grounding rule was doing its job. The retriever had not supplied the shopkeeper's lines.

End-to-end query path for that successful call:

1. Outer parallel receives the question string.
2. Inner `context_chain` keeps the string and also retrieves 6 chunks.
3. Those chunks include the shopkeeper: time has no price, a second cannot be bought back, use time wisely.
4. The prompt is filled with that context and the question.
5. `gemini-3.5-flash-lite` writes the answer from that context.
6. The parser returns a string, and the outer parallel packages `{question, answer}`.

## If the interview asks what you would add next

These are not in the script. They are the usual follow-ups, in the order they matter.

1. **Persist the index.** `save_local` / `load_local` so a second question does not re-embed the transcript.
2. **Keep metadata.** Store `video_id`, `start`, and `duration` on each `Document` before the join discards them, then return a timestamp with the answer.
3. **Many videos.** One FAISS index, `video_id` in metadata, and a metadata filter on the retriever so a question searches only the selected video.
4. **Multi-turn chat.** `ChatPromptTemplate` plus history. The retriever should still see a standalone question, so a rewrite step turns "what did he mean?" into "what lesson did the father want to teach his son?".
5. **Stronger retrieval.** MMR or a reranker when the video is long. A score threshold when "I couldn't find the answer" is better than a weak chunk.

