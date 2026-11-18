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

## **6. Which practices help maintain coherence in long AI conversations?**

Maintaining coherence means ensuring that an LLM understands the conversation context, remembers important information, and provides consistent responses across multiple interactions.

### **2. How it works**

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

### **3. Practical example**

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

### **4. When to use it**

- Customer support chatbots.
- Long-running AI conversations.
- AI agents.
- Personal assistants.
- Multi-step workflows.

### **5. Limitations**

- Summaries can lose important details.
- Incorrect memory can produce incorrect answers.
- Context management requires careful prioritization.

**Remember:** Good context management helps maintain consistency across long conversations.

## **7. What does Restating Keys mean in conversations, and why is it useful?**

### **1. Meaning**

Restating Keys means repeating important information, instructions, or constraints in a conversation to ensure the LLM continues to consider them while generating responses.

It is especially useful in long conversations where important instructions may become less prominent.

### **2. How it works**

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

### **3. When to use it**

- Long conversations.
- Multi-step code generation.
- Maintaining output formats.
- Enforcing coding standards.
- Reusing important business rules.

### **4. Limitations**

- Repeating everything increases token consumption.
- Repeated instructions can become contradictory if not maintained properly.
- Restating instructions does not guarantee compliance.

**Remember:** Restating Keys means reinforcing important information when it matters.

## **8. Why can an LLM generate different outputs for the same input, even when the prompt and model remain unchanged?**

### **1. Meaning**

LLMs can generate different responses for identical inputs because text generation involves probabilistic token selection and can be influenced by several runtime factors.

### **2. How it works**

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

### **3. Practical example**

Suppose you send the same prompt three times:

```
Generate a test case for this function:

function add(a, b) {
  return a + b;
}
```

Possible outputs:

- Test case 1: `add(2, 3) = 5`
- Test case 2: `add(10, 20) = 30`
- Test case 3: `add(-2, 2) = 0`

All three are valid test cases, but their outputs differ.

### **4. When to use this understanding**

- Automated test case generation.
- Code generation.
- AI-based report generation.
- Production LLM applications.
- Prompt evaluation and testing.

### **5. How to improve consistency**

- Use temperature = 0 where supported.
- Use fixed prompts and structured output schemas.
- Keep model versions unchanged.
- Control external data and retrieval.
- Validate outputs programmatically.

**Remember:** Same prompt does not always guarantee identical output. Temperature is one factor, but not the only one.

## **9. What does Inference Time mean when an LLM processes a prompt?**

### **1. Meaning**

Inference Time is the time during which a trained LLM processes an input and generates an output.

In simple terms:

**Training = Teaching the model.**

**Inference = Using the trained model to generate responses.**

### **2. How it works**

When you send a prompt to an LLM, the following process happens:

**1. User Prompt**

Input text

**2. Tokenization**

Text converted into tokens

**3. Model Processing**

Neural network processes input tokens

**4. Token Generation**

Model generates output tokens

**5. Final Response**

Generated answer

All these activities happen during inference.

### **3. Important terminology**

| Term                       | Meaning                                             |
| -------------------------- | --------------------------------------------------- |
| Training Time              | Time required to train the model.                   |
| Inference Time             | Time required to process input and generate output. |
| Time to First Token (TTFT) | Time taken to generate the first output token.      |
| Tokens Per Second          | Number of output tokens generated per second.       |
| Latency                    | Time taken to receive a response.                   |

### **4. When to use this understanding**

- Comparing LLM performance.
- Optimizing chatbot response speed.
- Choosing between cloud and local models.
- Optimizing LangChain applications.
- Reducing API response latency.

### **5. Limitations / considerations**

Inference time can increase due to:

- Large input context.
- Large output length.
- Complex model architecture.
- Hardware limitations.
- High server load.

**Remember:** Inference is the process of using a trained model to generate predictions or responses.

## **10. What is the difference between Context and Constraints in Prompt Anatomy?**

### **1. Meaning**

Both Context and Constraints provide additional instructions to an LLM, but they serve different purposes.

- **Context:** Provides background information required to understand the task.
- **Constraints:** Defines rules, boundaries, or restrictions that the output must follow.

### **2. Practical example**

Suppose you want to generate a React component.

```
Role:
You are a Senior React Developer.

Context:
We are developing an e-commerce application
using React and TypeScript.

Task:
Create a reusable product card component.

Constraints:
- Use functional components.
- Use TypeScript.
- Do not use external UI libraries.
- Follow mobile-first responsive design.
- Keep the component reusable.
```

Let's separate them:

| Component     | Purpose                    | Example                         |
| ------------- | -------------------------- | ------------------------------- |
| Role          | Defines the perspective    | Senior React Developer          |
| Context       | Provides background        | E-commerce application          |
| Task          | Defines what to do         | Create product card             |
| Constraints   | Defines limitations        | Use TypeScript, no UI libraries |
| Output Format | Defines response structure | Code + explanation              |

### **3. When to use it**

- Code generation.
- Technical documentation.
- Generating reports.
- Data extraction.
- AI agents and RAG applications.

### **4. Limitations**

- Too many constraints can restrict useful responses.
- Missing context can cause incorrect assumptions.
- Conflicting constraints can produce unpredictable results.

**Remember:** Context tells the LLM what it needs to know; constraints tell it what it must or must not do.

## **11. How can we design a prompt to generate a consistent report with predefined headings, paragraphs, bullet points, and tables every time?**

### **1. Meaning**

We can use Structured Prompting with explicit output-format instructions to make the LLM generate responses in a consistent structure.

The key is to define the expected format clearly instead of simply asking for a report.

### **2. How it works**

We define the report structure, formatting rules, and content requirements inside the prompt.

### **3. Practical example**

Suppose you want an LLM to generate a technical project report.

You can write:

**Sample prompt**

Reusable

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

&#x20;Copy prompt

### **4. When to use it**

- Technical reports.
- API documentation.
- Code review reports.
- Test case generation.
- Business analysis.
- Automated reporting systems.

### **5. How to improve consistency further**

For production applications, prompt instructions alone may not be sufficient.

You can combine them with:

- JSON Schema for enforcing data structure.
- Pydantic for validating generated data.
- Structured Output Parsers in LangChain.
- Programmatic validation for mandatory fields.

For example, instead of relying only on the LLM to generate a table, you can ask it to return structured JSON and convert that JSON into a table using your application.

**Remember:** Explicit output instructions improve consistency; schema validation provides stronger structural guarantees.

# **Quick Revision – Questions 6–11**

| #  | Concept                | Key takeaway                                                                  |
| -- | ---------------------- | ----------------------------------------------------------------------------- |
| 6  | Conversation Coherence | Maintain relevant context across interactions.                                |
| 7  | Restating Keys         | Repeat important instructions when needed.                                    |
| 8  | Output Variability     | Same input can produce different outputs due to sampling and runtime factors. |
| 9  | Inference Time         | Time during which a trained model processes input and generates output.       |
| 10 | Context vs Constraints | Background information vs rules and restrictions.                             |
| 11 | Structured Prompting   | Define explicit output structure and formatting rules.                        |

## **Important concepts to remember**

There are three distinctions worth keeping clear:

1. **Context Pruning vs Context Reset:** Pruning removes selected information; resetting starts with a fresh or redefined context.
2. **Iterative Prompting vs Restating Keys:** Iteration improves an output; restating reinforces important instructions.
3. **Structured Prompting vs Structured Output:** Structured prompting uses instructions to guide formatting; structured output uses schemas or constrained generation to enforce a format.

These distinctions will be particularly useful when we move towards LangChain, RAG, and AI agents.

Next, we can move to Questions 12–17: Prompt Anatomy and Prompt Fundamentals.