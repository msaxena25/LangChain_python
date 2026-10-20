# Python: History, creator, and latest versions

## Contents

- [1. Python history](#1-python-history)
- [2. In which language is Python written?](#2-in-which-language-is-python-written)
- [3. Current Python version — October 2026](#3-current-python-version--october-2026)
- [Python 3.15.0](#python-3150)
  - [4. Previous three major versions](#4-previous-three-major-versions)
  - [Python 3.14.0](#python-3140)
  - [Python 3.13.0](#python-3130)
  - [Python 3.12.0](#python-3120)
  - [What is ABC language, on which Python language influenced?](#what-is-abc-language-on-which-python-language-influenced)
    - [Why was ABC created?](#why-was-abc-created)
    - [Example: ABC vs Python](#example-abc-vs-python)
- [Why is Python widely used in AI and Machine Learning?](#why-is-python-widely-used-in-ai-and-machine-learning)
  - [1. Simple and readable syntax](#1-simple-and-readable-syntax)
  - [2. Powerful AI and ML libraries](#2-powerful-ai-and-ml-libraries)
  - [3. High performance without writing everything in Python](#3-high-performance-without-writing-everything-in-python)
  - [4. Easy experimentation](#4-easy-experimentation)
  - [5. Strong community and ecosystem](#5-strong-community-and-ecosystem)
- [How Python code executes internally?](#how-python-code-executes-internally)
  - [1. The complete execution flow](#1-the-complete-execution-flow)
    - [1. Python source code](#1-python-source-code)
    - [2. Parsing and compilation](#2-parsing-and-compilation)
    - [3. Python bytecode](#3-python-bytecode)
    - [4. Python virtual machine (PVM)](#4-python-virtual-machine-pvm)
    - [5. Operating system and CPU](#5-operating-system-and-cpu)
  - [2. Which compiler does Python use?](#2-which-compiler-does-python-use)
  - [3. Does Python use a transpiler?](#3-does-python-use-a-transpiler)
  - [4. Does Python execute code from top to bottom?](#4-does-python-execute-code-from-top-to-bottom)
  - [5. Does Python create a `.pyc` file?](#5-does-python-create-a-pyc-file)
- [Install Python](#install-python)
  - [Current Version - 3.15.0](#current-version---3150)
  - [After installation, follow these steps in your project terminal.](#after-installation-follow-these-steps-in-your-project-terminal)
- [`-m` means “run a module as a script](#-m-means-run-a-module-as-a-script)
  - [Example 1: Without `-m`](#example-1-without--m)
  - [Example 2: With `-m`](#example-2-with--m)
- [Python `requirements.txt`](#python-requirementstxt)
  - [1. What problem does it solve?](#1-what-problem-does-it-solve)
  - [2. How to create `requirements.txt`](#2-how-to-create-requirementstxt)
  - [3. How to install dependencies from the file](#3-how-to-install-dependencies-from-the-file)
  - [4. How to generate the file automatically](#4-how-to-generate-the-file-automatically)
- [Python Virtual Environment (`venv`)](#python-virtual-environment-venv)
  - [1. What problem does `venv` solve?](#1-what-problem-does-venv-solve)
    - [Main problems it solves](#main-problems-it-solves)
  - [2. How to create a virtual environment](#2-how-to-create-a-virtual-environment)
  - [3. How to activate it](#3-how-to-activate-it)
  - [4. How to deactivate it](#4-how-to-deactivate-it)
- [To Upgrade & check pip package -](#to-upgrade--check-pip-package--)
- [In LangChain, OpenAI, Google Gemini, and Anthropic use separate integration packages.](#in-langchain-openai-google-gemini-and-anthropic-use-separate-integration-packages)
  - [Install HuggingFace](#install-huggingface)
    - [Verify installation](#verify-installation)
    - [Example import](#example-import)
  - [Machine learning Utilities Packages _ will learn later](#machine-learning-utilities-packages-_-will-learn-later)
- [Diff between `OpenAI` and `ChatOpenAI`](#diff-between-openai-and-chatopenai)
  - [1. `OpenAI` vs `ChatOpenAI`](#1-openai-vs-chatopenai)
  - [Parent Classes of both](#parent-classes-of-both)

## 1. Python history

Creator: Guido van Rossum

Started: 1989

First public release: Python 0.9.0, in February 1991.

**Original idea:** Create a language that is easy to read and write, with a clear syntax, while still being powerful enough for real software development.

**Why the name Python?** It was inspired by the British comedy show Monty Python's Flying Circus, not the snake.

**Who manages Python today?** The Python community develops it through the Python Software Foundation (PSF), Python's core developers, and the Python Steering Council.

**Is Python a completely new language?** No. It was influenced by earlier languages, especially ABC, and has evolved continuously since its first release.

## 2. In which language is Python written?

Python is a programming language specification with different implementations. The most widely used implementation is CPython, which is primarily written in C.

```
Your Python code - `print("Hello World")`
          |
CPython interpreter - Processes your code and executes its operations
          |
Machine-level operations - The operating system and processor carry out the work
```

Python is generally considered a high-level, interpreted language. CPython commonly compiles Python source into bytecode first, then its virtual machine executes that bytecode.

## 3. Current Python version — October 2026

# Python 3.15.0

Stable release

Released: 9 October 2026

Three important improvements

1. Lazy imports: Modules can be loaded only when first needed, potentially improving application startup time.
2. UTF-8 by default: More consistent text encoding across different operating systems.
3. Performance improvements: The experimental JIT compiler has been improved to make eligible code run faster.

## 4. Previous three major versions

## Python 3.14.0

Released: 7 October 2025

- Template string literals (t-strings): Support for processing template strings through custom logic.
- Multiple interpreters: Standard-library support for working with separate Python interpreters.
- Deferred annotations: Type annotations can be evaluated later, helping with certain typing and import-related issues.

## Python 3.13.0

Released: 7 October 2024

- Improved interactive interpreter: Better command-line experience, including colorized output and improved error messages.
- Experimental free-threaded mode: A build option designed to allow Python threads to run without the traditional GIL.
- Experimental JIT compiler: Introduced an early implementation of just-in-time compilation.


## Python 3.12.0

- Faster f-strings: More flexible syntax for formatting strings.
- Type parameter syntax: New syntax for defining generic classes and functions.
- Performance and diagnostics: Improvements to interpreter performance and error messages.

----

## What is ABC language, on which Python language influenced?

ABC was an early programming language designed to make programming simple and easy to learn.

It was developed at CWI (Centrum Wiskunde & Informatica), a research institute in the Netherlands, during the 1980s. 

### Why was ABC created?

The goal was to make programming accessible to beginners and non-programmers, rather than requiring them to learn complicated syntax.

### Example: ABC vs Python

ABC used a more English-like syntax:

```
WRITE "Hello World"
```

Python uses:

```py
print("Hello World")
```

The example illustrates their readability-oriented design, though ABC and Python have different syntax and capabilities.

---

# Why is Python widely used in AI and Machine Learning?

The simplest answer is: Python makes it easy to build AI applications because it combines simple syntax, powerful libraries, and access to high-performance computing.

**Since you're learning Python for LangChain and AI engineering, understand these five reasons.**

## 1. Simple and readable syntax

Python lets you focus on the AI logic instead of writing lots of code.

For example, calculating the average of numbers:

Python:

```py
numbers = [10, 20, 30, 40]
average = sum(numbers) / len(numbers)
print(average)
```

You can understand this code without much programming knowledge.

## 2. Powerful AI and ML libraries

**Python has a mature ecosystem of libraries that handle complex work for you.**

**NumPy** - Performs numerical calculations and operations on arrays.

**pandas** - Helps clean, organize, and analyze datasets.

**scikit-learn** - Provides traditional machine-learning algorithms, such as classification and regression.

**PyTorch** - Used to build and train neural networks and deep-learning models.
LangChain - Helps developers build LLM applications using prompts, models, tools, retrieval, and agents.

## 3. High performance without writing everything in Python

Python itself is not always the fastest language. However, many AI libraries perform computationally expensive operations using optimized C, C++, GPU, or other native code.

## 4. Easy experimentation

AI development involves trying different models, prompts, parameters, and datasets.

Python makes it easy to change your code and test ideas quickly, especially in Jupyter notebooks.

## 5. Strong community and ecosystem

Python has extensive documentation, tutorials, open-source projects, and integrations. For example, scikit-learn provides ready-to-use algorithms for classification, regression, clustering, and model selection.

---

# How Python code executes internally?

Think of this as the journey from the Python code you write to the instructions your computer executes.

## 1. The complete execution flow

### 1. Python source code

`main.py` — the code you write

### 2. Parsing and compilation

Syntax is checked & validate; CPython generates bytecode

### 3. Python bytecode

Intermediate instructions for the Python virtual machine

### 4. Python virtual machine (PVM)

CPython's execution engine interprets the bytecode

### 5. Operating system and CPU

Native machine instructions perform the actual operations

## 2. Which compiler does Python use?

In the most common implementation, `CPython`, the compiler is self built into the Python interpreter itself. You do not usually install or run a separate compiler command like `gcc` for your Python application.

The compilation stages are roughly:

1. Tokenization: Reads the source and identifies tokens such as names, numbers, and operators.
2. Parsing: Checks the grammar and builds an Abstract Syntax Tree (AST).
3. Bytecode generation: Converts the parsed program into bytecode instructions.
4. Execution: The virtual machine executes those instructions.

The compiler implementation in CPython is written primarily in C, just like much of the interpreter.

## 3. Does Python use a transpiler?

Normally, no. A transpiler converts source code from one programming language into another programming language—for example, TypeScript into JavaScript.

## 4. Does Python execute code from top to bottom?

Yes

## 5. Does Python create a `.pyc` file?

Often, yes. When Python imports a module, it can cache compiled bytecode in a directory such as `__pycache__`.

For example:

```
project/
├── main.py
├── helper.py
└── __pycache__/
    └── helper.cpython-315.pyc
```

- `.py` contains your source code.
- `.pyc` contains cached Python bytecode, not a normal native executable.

---


# Install Python

You can download from Microsoft Store if available for You OR You can directly install from Python Official website (https://www.python.org/downloads/).

### Current Version - 3.15.0

But Working with Latest Version create dendencies issues or Conflicts with packages so Best to choose Version 3.13.0.

You can install Python 3.13 from the Microsoft Store. You don't need to uninstall Python 3.15.

### After installation, follow these steps in your project terminal.

1. Verify Python 3.13 is available (Below command will give all installed version)

```
py -0p
```

2. Verify the setup

```
python --version
python -m pip show langchain
```

You should see Python 3.13.x and the installed LangChain package details.

---

# `-m` means “run a module as a script

In Python commands, `-m` means “run a module as a script.”

Python uses it to find a module and execute it through the Python interpreter.

## Example 1: Without `-m`

```
python hello.py
```

Here, Python executes your file named `hello.py`.

## Example 2: With `-m`

```
python -m pip --version
``` 

Here:

- `python` → starts the Python interpreter.
- `-m` → tells Python to run a module.
- `pip` → the module Python runs to manage packages.
- `--version` → asks pip to display its version.

---

# Python `requirements.txt`

## 1. What problem does it solve?

Imagine your LangChain project uses these packages:

- `langchain`
- `langchain-openai`
- `python-dotenv`

Without `requirements.txt`, you may have to remember and install each package manually. On another computer, you might accidentally install different versions, which can cause compatibility issues.

With `requirements.txt`, you can record the dependencies in one file and install them with a single command.

## 2. How to create `requirements.txt`

Example:

```
langchain==1.0.3
langchain-openai==1.0.2
python-dotenv==1.1.1

```
These version numbers are illustrative, not a recommendation to install those specific releases.

Version operators you can use:

| Syntax                | Meaning                                               |
| --------------------- | ----------------------------------------------------- |
| `langchain==1.0.3`    | Exactly version 1.0.3                                 |
| `langchain>=1.0.0`    | Version 1.0.0 or newer                                |
| `langchain>=1.0,<2.0` | Any version in the specified range                    |
| `langchain~=1.0.0`    | Compatible releases, generally `>=1.0.0` and `<1.1.0` |

For learning projects, exact versions can make it easier to reproduce the same environment.

## 3. How to install dependencies from the file

Activate your project's virtual environment first, then run:

```
python -m pip install -r requirements.txt
```

Here, `-r` tells pip to read package requirements from the specified file.

Pip will install the listed packages and their required dependencies, subject to the version constraints.

## 4. How to generate the file automatically

**If you have already installed the packages in your virtual environment, you can run:**

```
python -m pip freeze > requirements.txt
```

This records the installed packages and their versions.

Important distinction:

- `pip freeze` records all installed packages in that environment, including transitive dependencies.
- A manually maintained `requirements.txt` can list only the packages your project directly needs.

For a learning project, either approach works. For reproducibility, make sure you generate the file from the correct virtual environment.

-----

# Python Virtual Environment (`venv`)

A virtual environment is an isolated Python environment for a particular project. 

It lets each project maintain its own installed packages without mixing them with other projects.

## 1. What problem does `venv` solve?

Imagine you have two projects:

- Project A: Uses LangChain version 0.x.
- Project B: Requires a newer LangChain version 1.x.

Without isolation, installing or upgrading packages in one shared environment can break the other project.

### Main problems it solves

1. Dependency conflicts: Projects can use different versions of the same library.
2. Global Python pollution: You don't need to install every project package into your shared Python environment.
3. Reproducibility: You can record dependencies in a `requirements.txt` file and recreate an environment later.
4. Safer experimentation: You can install, upgrade, or remove project packages without intentionally changing packages in other project environments.

**A virtual environment isolates Python packages; it is not a complete virtual machine or a security boundary.**

## 2. How to create a virtual environment

First, open your terminal inside your project folder.

```
mkdir langchain-learning
cd langchain-learning
```

Create the environment:

```
python -m venv .venv
```

What does this command mean?

- `python` — runs Python.
- `-m venv` — runs Python's built-in virtual environment module.
- `.venv` — the folder name where the environment will be created.

Your folder structure will look like this:

```
langchain-learning/
├── .venv/
│   ├── Scripts/
│   ├── Lib/
│   └── pyvenv.cfg
└── main.py
```

## 3. How to activate it

```
.venv\Scripts\activate
```

After activation, your terminal prompt typically shows `(.venv)`.

Now install a package:

```
python -m pip install langchain
```

It will be installed into your active virtual environment rather than the normal shared environment.

## 4. How to deactivate it

Simply run:

```
deactivate
```

Your terminal returns to its normal environment.

---

# To Upgrade & check pip package -

```
python -m pip install --upgrade pip

python -m pip --version
```

# In LangChain, OpenAI, Google Gemini, and Anthropic use separate integration packages.

Run this command inside your activated virtual environment:

```
python -m pip install langchain-openai langchain-google-genai langchain-anthropic
```

## Install HuggingFace

```
python -m pip install langchain-huggingface
```

If you also need Hugging Face's core libraries for models, tokenizers, and pipelines, install:

```
python -m pip install langchain-huggingface transformers huggingface-hub
```

### Verify installation

```
python -m pip show langchain-huggingface
```

### Example import

```
from langchain_huggingface import HuggingFaceEndpoint
```

## Machine learning Utilities Packages _ will learn later

numpy
scikit-learn

----

# Diff between `OpenAI` and `ChatOpenAI`


## 1. `OpenAI` vs `ChatOpenAI`

| Feature      | `OpenAI`                                                    | `ChatOpenAI`                                             |
| ------------ | ----------------------------------------------------------- | -------------------------------------------------------- |
| Model type   | Text-completion models                                      | Chat models                                              |
| Input        | Usually a text prompt                                       | Messages with roles, such as system, user, and assistant |
| Output       | Text Simple                                             | Assistant message with additional informartion like tokens, uses etc.                                 |
| Modern usage | Legacy completion workflows or compatible completion models | Recommended for modern OpenAI chat models                |
| Import       | `langchain_openai`                                          | `langchain_openai`                                       |

## Parent Classes of both

OpenAI -> BaseOpenAI -> BaseLLM

ChatOpenAI -> BaseChatOpenAI -> BaseChatModel