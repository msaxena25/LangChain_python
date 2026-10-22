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