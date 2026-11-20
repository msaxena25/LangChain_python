## 1. What is Context Pruning?

`Context Pruning` is the process of `removing irrelevant, redundant, or unnecessary information` from the context before sending it to an LLM.

## When to use it

- Long-running AI conversations.
- RAG applications.
- AI agents with conversation history.

### Limitations

Removing context incorrectly or blindly can cause the LLM to lose important information.

### Here are some common techniques used to implement **Context Pruning**:

| #  | Technique                     | One-line definition                                                                      |
| -- | ----------------------------- | ---------------------------------------------------------------------------------------- |
| 1  | Sliding Window                | Retains only the most recent N messages and removes older messages.                      |
| 2  | Token-Based Trimming          | Removes older or less important content to stay within a token limit.                    |
| 3  | Summarization                 | Converts lengthy conversation history into a shorter summary.                            |
| 4  | Relevance-Based Filtering     | Retains only information relevant to the current query.                                  |
| 5  | Semantic Filtering            | Uses embeddings and semantic similarity to identify relevant context.                    |

For LangChain, particularly explore **trim_messages, Conversation Summary, and token-based history management**.

## What is Role-Based Prompting? How do LLMs interpret roles?

Role-Based Prompting is a technique where we `assign a specific role` or identity to the LLM to guide its response style, perspective, and task approach.

**With role:**

```
You are a Senior React Developer
with 10 years of experience.

Explain React performance optimization
with practical examples.
```

### How does an LLM understand the role?

An LLM doesn't actually become a senior developer.

It `processes the role instruction as part of its input` and generates responses based on learned patterns associated with that role.

For example:

- Senior Developer → Architecture, performance, design decisions.
- Teacher → Step-by-step explanations.
- Code Reviewer → Bugs, maintainability, coding standards.

## What is Chain-of-Thought (CoT) Prompting? What are its limitations?

`Chain-of-Thought Prompting` is a technique that encourages an LLM to solve a complex problem through intermediate reasoning steps rather than jumping directly to the final answer.

### 2. How it works

Consider this question:

```
A shopping application has 120 products.
Each page displays 20 products.

How many pages are required?
```

A direct answer:

```
6 pages.
```

**A reasoning-oriented prompt:**

```
Solve this problem step by step.

1. Identify the total products.
2. Identify products displayed per page.
3. Calculate the required pages.
4. Provide the final answer.
```

The model is encouraged to break the problem into smaller steps.

### Limitations

- More reasoning tokens can increase cost and latency.
- Intermediate reasoning can still contain mistakes.
- Longer reasoning doesn't always mean better accuracy.
- It is not necessary for simple questions.

## What is Iterative Prompting?

`Iterative Prompting` is the process of improving an LLM's output through `multiple interactions` by providing additional instructions, feedback, or corrections.

Instead of expecting a perfect result from the first prompt, we gradually improve it.

**Suppose you want to generate a React component.**

Iteration 1 : "Create a React login form."

Output: Basic login form.

Iteration 2: Provide additional instructions, Now add validations on username and password field.

Output: Login form with additional functionality.

Iteration 3

Provide further feedback

"Improve accessibility, add error messages, and use TypeScript."

Output: More complete and refined component.

##  What is Context Reset in a Prompt?

Context `Reset` means starting a task with a fresh or explicitly redefined context so that irrelevant information from previous interactions doesn't influence the new task.

### 2. How it works

```
Let's start a new topic.

Ignore the previous React-related task.
For this discussion, focus only on Python.

Explain Python decorators with examples.
```

This establishes a new task context.

**Important technical distinction:**

Writing "ignore previous context" does not necessarily delete the previous conversation from the model's context window.

`A true context reset generally requires starting a new conversation`.

------

## Which practices help maintain coherence in long AI conversations?

`Maintaining coherence means` ensuring that an LLM understands the conversation context, remembers important information, and provides consistent responses across multiple interactions.

As conversations become longer, we need to manage the context sent to the LLM.

Some useful practices:

| Practice                   | Definition                                                     |
| -------------------------- | -------------------------------------------------------------- |
| Context Pruning            | Remove irrelevant conversation history.                        |
| Conversation Summarization | Maintain a summary of important previous discussions.          |
| Sliding Window             | Keep only the most recent N messages.                          |
| Key Information Retention  | Preserve important facts, decisions, and instructions.         |
| Context Restatement        | Repeat important information when needed.                      |
| Structured Context         | Organize context using headings, sections, or key-value pairs. |
| Memory Management          | Store important information for future interactions.           |

### Practical example

Suppose you are building a chatbot for an e-commerce application.

The user says:

- My preferred language is English.
- I am looking for running shoes.
- My budget is ₹3,000.

After 20 interactions, the chatbot should still retain the relevant preferences when recommending shoes.

Instead of passing the entire conversation history, we can maintain a compact context:

```
User Preferences:
- Language: English
- Product: Running shoes
- Budget: ₹3,000
```
---------

##  What does Restating Keys mean in conversations, and why is it useful?

Restating Keys means `repeating important information, instructions, or constraints` in a conversation to ensure the LLM continues to consider them while generating responses.

Suppose you initially provide this instruction:

```
Always generate code using TypeScript.
Use functional components and React hooks.
```

After several interactions, you ask:

```
Now create a reusable dropdown component.

Remember:
- Use TypeScript.
- Use functional components.
- Use React hooks.
```

You have restated the important instructions.

----------

## Why can an LLM generate different outputs for the same input, even when the prompt and model remain unchanged?

LLMs can generate different responses for identical inputs because `text generation involves probabilistic token selection` and can be influenced by several runtime factors.

Let's understand your three hypotheses.

| Your hypothesis            | Is it a valid reason? | Explanation                                                                                                  |
| -------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ |
| API load balancing         | Usually not directly  | Requests may reach different servers, but load balancing alone should not necessarily change the output.     |
| Temperature                | Yes                   | Higher temperature generally increases randomness in token selection.                                        |
| External database fetching | Sometimes             | If the application retrieves external or changing information, the context supplied to the model may differ. |

There are some additional reasons.

**A. Sampling parameters**

- Temperature
- Top-K
- Top-P

These influence how the next token is selected.

**B. Model infrastructure**

Different hardware, numerical precision, inference kernels, and parallel execution can sometimes introduce small numerical differences.

**C. Model or backend changes**

A provider might update its model implementation or serving infrastructure without your application code changing.

**D. External context**

RAG retrieval, web search, APIs, and database queries can provide different context for each request.

-------------

## What does Inference Time mean when an LLM processes a prompt?

`Inference Time` - Time required to process input and generate output.

------

## What is the difference between Context and Constraints in Prompt Anatomy?

- **Context:** Provides background information required to understand the task.
- **Constraints:** Defines rules, boundaries, or restrictions that the output must follow.

`Context tells the LLM what it needs to know; constraints tell it what it must or must not do.`

-----

## How can we design a prompt to generate a consistent report with predefined headings, paragraphs, bullet points, and tables every time?

We can use `Structured Prompting with explicit output-format` instructions to make the LLM generate responses in a consistent structure.

**Sample prompt**

```
You are a Technical Documentation Expert.

Task:
Generate a technical project report
based on the provided project details.

Follow these output rules strictly:

1. Use the following headings:
   - Project Overview
   - Technology Stack
   - Architecture
   - Key Features
   - Challenges
   - Conclusion

2. Formatting rules:
   - Use paragraphs for explanations.
   - Use bullet points for features.
   - Use tables for technology comparisons.
   - Use numbered lists for sequential steps.

3. Keep the language simple and professional.

4. Do not skip any required heading.

5. If information is unavailable,
   write "Not Provided" instead of guessing.

Output only the report.
```

### How to improve consistency further

For production applications, prompt instructions alone may not be sufficient.

You can combine them with:

- `JSON Schema` for enforcing data structure.
- `Pydantic` for validating generated data.
- Structured Output `Parsers` in LangChain.

-------

## What are the main components of Prompt Anatomy?

Prompt Anatomy refers to the different elements that make a prompt clear and effective.

| Component          | Purpose                                  |
| ------------------ | ---------------------------------------- |
| Role               | Defines who the LLM should act as.       |
| Context            | Provides background information.         |
| Task / Instruction | Defines what the LLM should do.          |
| Constraints        | Defines rules and limitations.           |
| Input Data         | Provides the actual data to process.     |
| Output Format      | Defines the expected response structure. |
| Examples           | Demonstrates the expected output.        |

---------

## What is the difference between Zero-Shot, One-Shot, and Few-Shot Prompting?

These techniques define how many examples we provide to an LLM before asking it to perform a task.

| Technique | Meaning                     |
| --------- | --------------------------- |
| Zero-Shot | No examples provided.       |
| One-Shot  | One example provided.       |
| Few-Shot  | Multiple examples provided. |

---------

## What is Instruction-Based Prompting?

`Instruction-Based Prompting` means giving clear and specific instructions to an LLM about what action it should perform.

**Example:**

```
Analyze the following React code.

1. Identify performance issues.
2. Find unnecessary re-renders.
3. Suggest optimization techniques.
4. Provide corrected code.
```
-----

## What is the difference between Positive and Negative Prompting?

| Type               | Meaning                      | Example                                    |
| ------------------ | ---------------------------- | ------------------------------------------ |
| Positive Prompting | Tells the LLM what to do.    | Use TypeScript and functional components.  |
| Negative Prompting | Tells the LLM what to avoid. | Do not use JavaScript or class components. |

**Combined example:**

```
Generate a React component.

Positive instructions:
- Use TypeScript.
- Use functional components.
- Follow clean coding practices.

Negative instructions:
- Do not use class components.
- Do not use external UI libraries.
- Avoid unnecessary dependencies.
```
----

## What is Delimiter-Based Prompting, and why do we use XML tags or special separators?

`Delimiter-Based Prompting` uses special separators or tags to distinguish different sections of a prompt.

It helps organize instructions, context, and input data clearly.

**Example using XML tags:**

```
<role>
You are a Senior React Developer.
</role>

<task>
Review the provided code.
</task>

<constraints>
Use TypeScript.
Avoid unnecessary dependencies.
</constraints>

<code>

</code>
```

Other commonly used delimiters:

- Triple quotes (`"""`)
- Triple backticks (\`\`\`)
- XML tags (`<context>`, `<task>`)
- Separators (`###`, `---`)

**When to use:** Long prompts, RAG applications, code analysis, and structured instructions.

-----

## What is Structured Prompting, and how can we enforce a specific output format?

Structured Prompting means defining a specific structure for the LLM's response, such as JSON, tables, headings, or bullet points.

**Example:**

```
Analyze this product and return the result
in the following JSON structure:
```

-------------