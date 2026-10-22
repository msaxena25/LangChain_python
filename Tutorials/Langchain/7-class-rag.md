# RAG

You've now learned the four important building blocks of RAG:

1. Document loaders — load data from PDFs, text files, websites, and other sources.
2. Text splitters — divide documents into manageable chunks.
3. Embedding Generation and Vector store — store document embeddings and support similarity search.
4. Retrievers — find relevant documents for a user's query.

`RAG is a technique` in which an LLM retrieves relevant information from an external knowledge source and uses that information to generate an answer.

## What is parameterized knowledge?

`Parameterized knowledge` is the information and patterns a model learns during training and represents through its learned `parameters` (weights).

## How is knowledge stored in parameters?

A neural network contains many numerical values called `parameters` or `weights`. During training, these values are adjusted to help the model predict the correct next tokens.

GPT-3 have `175 B` parameters, GPT-2 have `1.5 B` parametersetc..

## Why an LLM alone is not enough for a real-world application? 

**Scenario 1: Private company documents**

A general LLM cannot answer reliably from private documents it has never been given access to.

**Scenario 2: Today's news or recent information**

A model's training data has a cutoff or coverage limitation. It cannot reliably know events that happened after its training.

**Scenario 3: Hallucination**

Example: “Did Einstein play football for Germany in his early years?”

An LLM may confidently generate a false answer because it predicts plausible text rather than automatically verifying every claim against reality. A confident tone is not evidence that the answer is true.

## Fine tuning

Fine-tuning means taking an already-trained LLM and training it further on a `specific dataset` so that it becomes better suited to a particular task or way of responding.

## How does fine-tuning work?

1\. Choose a pre-trained model: An existing LLM

2\. Prepare training data: Input examples + expected outputs (Hundreds to thousands OR Tens of thousands or more dataset)

3\. Run fine-tuning: Update model weights to learn the examples

4\. Evaluate the model: Test accuracy, consistency and unwanted regressions

5\. Deploy the adapted model

During training, the model compares its predictions with the expected outputs and adjusts its trainable parameters to reduce the error.

## What should the training data look like?

A common format for chat-model supervised fine-tuning is `JSONL`: one JSON training example per line.

For example, a file named `training_data.jsonl` could contain:

```jsonl
{"messages":[{"role":"user","content":"I can't log in."},{"role":"assistant","content":"{\"category\":\"AUTHENTICATION\"}"}]}
{"messages":[{"role":"user","content":"My payment was deducted twice."},{"role":"assistant","content":"{\"category\":\"BILLING\"}"}]}
{"messages":[{"role":"user","content":"The app crashes on startup."},{"role":"assistant","content":"{\"category\":\"TECHNICAL_ISSUE\"}"}]}
```

So provided such JSONL data is called **Supervised fine tuning method (SFT)** where we give data in labelled format like above.

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

### How it works

1. Supervised fine tuning method (SFT): First, train the model on example questions and good answers.
2. Human feedback: Humans checks different responses and choose which is better, Choose Response A or Response B
  (We have seen many times on Chat GPT or Gemini to choose respones).
3. Reward model: A model learns to predict which responses humans prefer.
4. Reinforcement learning: The LLM is optimized to produce responses that receive higher reward scores.

**Remember:** RLHF is not the same as JSONL, LoRA, or QLoRA. RLHF describes a `preference-based training approach`; JSONL is a data format, while LoRA and QLoRA are parameter-efficient training techniques.

---------

# Challenges of Fine-Tuning an LLM

1. High cost — GPU compute, training, and deployment can be expensive.
2. Large data requirements — Collecting enough high-quality training examples can be difficult.
3. Data quality — Incorrect or inconsistent examples can teach the model undesirable behavior.
4. Technical complexity — Requires knowledge of training, models, datasets, and hardware.
4. Training time — Larger models and datasets can take substantial time to train.
5. Model maintenance — New requirements or data may require additional training and evaluation.
7. Model compatibility — Not every model supports every fine-tuning method or hardware configuration.
8. Catastrophic forgetting — The model may lose some previously learned capabilities.

---------

# In-context learning (ICL)

`In-context learning` is the ability of an LLM to perform a task by using instructions or examples provided in the current prompt, without updating its model parameters. It became widely known through `the GPT-3 research paper, Language Models are Few-Shot Learners, published in 2020`.

In-context learning (ICL) can avoid many fine-tuning costs and complexities, but it cannot solve all fine-tuning problems or all LLM limitations.

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

This is called **few-shot learning** because you provide a few examples in the prompt. With no examples, it is called zero-shot learning if you rely on instructions alone.

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

# RAG Evalution - Most Important

Now that you've built your first YouTube transcript-based RAG application, the next step is Evaluation. This is an important step toward building a reliable, industry-standard RAG application.

## What is RAG evaluation?

RAG evaluation is the process of measuring how `correctly` and `reliably` your RAG application retrieves relevant information and generates answers.

For example, suppose you ask your YouTube chatbot:

“What lesson did the father want to teach his son?”

**Evaluation helps you determine:**

- Did the retriever find the relevant transcript chunks?
- Did the LLM give the correct answer based on those chunks?
- Did the answer contain unsupported or fabricated information?
- Was the answer clear and relevant?

## 2. RAG evaluation techniques

Here are the major techniques and a short description of each.

| Technique                                | Short description                                                                                                     |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| 1. Retrieval Evaluation                  | Measures whether the retriever finds the correct and relevant document chunks.                                        |
| 2. Answer / Generation Evaluation        | Measures the correctness, relevance, and quality of the generated answer.                                             |
| 3. Faithfulness Evaluation               | Checks whether the answer is supported by the retrieved context rather than invented.                                 |
| 4. Context Precision                     | Measures whether the retrieved chunks are relevant, particularly whether relevant results rank above irrelevant ones. |
| 5. Context Recall                        | Measures whether the retrieved context contains the information needed to answer the question.                        |                                            |
| 6. Hallucination Detection               | Identifies claims that are unsupported by the provided evidence or contradict it.                                     |
| 7. Cost Evaluation                      | Measures token usage, embedding costs, LLM costs, and overall cost per query.                                         |

## 3. Libraries and frameworks

**Ragas**

Focus: RAG-specific metrics

Provides metrics such as faithfulness, answer relevancy, context precision, context recall, and answer correctness.

**DeepEval**

Focus: automated LLM testing

Supports RAG evaluation, hallucination checks, answer relevance, and repeatable test cases.

**LangSmith**

Focus: tracing, datasets, and experiments

Helps trace LangChain executions, compare versions, run evaluations, and monitor application behavior.

## 4. Why is evaluation important?

Without evaluation, your application may appear to work because a few example questions produce good answers, while failing on real user questions.

**Evaluation helps you:**

- Measure quality: establish a baseline before making changes.
- Compare approaches: determine whether different chunk sizes, retrievers, embedding models, or prompts improve results.
- Reduce hallucinations: test whether answers are grounded in the transcript.
- Prevent regressions: verify that code or model changes haven't degraded performance.
- Monitor production: identify quality, latency, and cost problems over time.

## 5. Is evaluation required for an industry-standard RAG application?

Yes, a systematic evaluation process is strongly recommended for production-grade RAG. There is no single mandatory evaluation library or universal set of metrics, but shipping a system without testing its retrieval quality, answer quality, failure cases, and operational performance is risky.

----------

# RAG improvement: Indexing improvement some techniques

1\. **Document cleaning and preprocessing**

Remove unnecessary HTML, duplicated text, navigation content, transcription artifacts, and irrelevant boilerplate before creating chunks.

2\. **Advanced chunking strategies**

Go beyond fixed-size splitting. Consider semantic chunking, structure-aware chunking, sentence-based splitting, or document-specific strategies.

3\. **Optimize chunk size and overlap**

Experiment with chunk size and overlap using an evaluation dataset instead of selecting arbitrary values.

4\. **Metadata enrichment**

Attach metadata such as source, document ID, video ID, title, topic, timestamps, creation date, and access permissions.

5\. **Deduplication and content validation**

Detect duplicate documents or chunks, empty content, corrupted records, and invalid metadata before indexing.

6\. **Vector store**

Currently we have used FAISS that is basic vector store. For industry standard we can with Pincone a cloud based vector store as well.

---------

# RAG Retrieval Improvements

## 1. Pre-retrieval Techniques

1\. Query Rewriting: Rewrite vague, ambiguous, or misspelled questions into clearer search queries to improve retrieval quality.

2\. Query Expansion / Multi-Query Retrieval: Generate multiple alternative queries for the same question to retrieve relevant information expressed in different ways.

3\. Query Contextualization: Use conversation history to convert follow-up questions into standalone queries that can be understood without previous messages.

## 2. During-retrieval Techniques

1\. Similarity Search Tuning: Optimize the number of retrieved chunks (`k`) and search configuration to balance relevance and context coverage.

2\. Similarity Score Threshold: Retrieve only documents whose relevance scores meet a specified threshold, avoiding weak matches.

3\. MMR (Maximal Marginal Relevance): Retrieve relevant documents while reducing redundancy among the selected chunks.

4\. Hybrid Search: Combine semantic vector search with keyword-based search, such as BM25, to capture both meaning and exact keyword matches.

5\. Ensemble Retrieval or Domain Aware routing: Combine results from multiple retrievers using techniques such as Reciprocal Rank Fusion (RRF) to improve retrieval coverage.

## 3. Post-retrieval Techniques

1\. Reranking: Use a reranking model, often a cross-encoder, to rescore retrieved documents against the query and reorder them by relevance.

2\. Contextual Compression: Remove irrelevant portions of retrieved documents or extract only the information relevant to the user's question.

3\. Deduplication: Remove duplicate or substantially overlapping chunks from the retrieved results.

---------

# RAG Improvement: Augmentation Phase

1\. Context Formatting: Format retrieved chunks clearly, separating documents with newlines and including source information where useful.

2\. Context Duplication & Compression: Remove repeated and Reduce unnecessary text while preserving information needed to answer the question, saving tokens and reducing noise.

3\. Prompt Instruction Optimization: Clearly instruct the LLM to answer using the provided context, avoid unsupported claims, and say when the context does not contain the answer.

4\. Conversation History Integration: For conversational RAG, include only the relevant previous messages alongside the retrieved context, avoiding unnecessary history.

5\. Context Token Budget Management: Estimate prompt token usage and limit the context so the combined instructions, question, retrieved content, and expected answer fit within the model's context window.

6\. Answer grounding: means ensuring that the LLM's answer is based on the provided context or reliable source documents, rather than unsupported assumptions or its own potentially incorrect knowledge.
---------

# RAG Improvements: Generation Phase

1\. Hallucination Reduction: Instruct the model to acknowledge missing information rather than inventing an answer. This reduces risk but does not eliminate hallucinations.

2\. Structured Output: Use formats such as JSON with defined fields or schemas to produce predictable, machine-readable responses.

3\. Temperature Tuning: Adjust temperature to control output variability. Lower values often suit factual RAG answers, although they do not guarantee correctness

4\. Citation Generation: Ask the LLM to include source IDs, document references, or timestamps supporting its answer, then validate those citations.

5\. Streaming Responses: Stream the generated answer to the user as tokens arrive, improving perceived responsiveness.

6\. Guardrails: are rules and validation mechanisms that control an AI application's inputs and outputs to make it safer, more reliable, and compliant with business requirements.

----------

# RAG system design approaches or architectural patterns

They address different requirements:

| RAG approach     | Main purpose                                                                                     |
| ---------------- | ------------------------------------------------------------------------------------------------ |
| Multimodal RAG   | Retrieve and use multiple data types, such as text, images, audio, and video.                    |
| Agentic RAG      | Use an AI agent to decide how to search, which tools to use, and whether to retrieve again.      |
| Memory-based RAG | Retrieve relevant information from past conversations, user preferences, or stored interactions. |

Important distinction: These approaches are not mutually exclusive. You can combine all three in one application.

For example, a personalized video assistant could retrieve video transcripts and frames (multimodal), remember previous conversations (memory-based), and decide dynamically when to search again (agentic).

-----------