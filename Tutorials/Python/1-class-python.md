# Python - 

## Install Python

You can download from Microsoft Store if available for You OR You can directly install from Python Official website (https://www.python.org/downloads/).

### Current Version - 3.15.0

But Working with Latest Version create dendencies issues or Conflicts with packages so Best to choose Version 3.13.0.

You can install Python 3.13 from the Microsoft Store. You don't need to uninstall Python 3.15.

### After installation, follow these steps in your project terminal.

1\. Verify Python 3.13 is available (Below command will give all installed version)

```
py -0p
```
2\. Create a fresh virtual environment

```
py -3.13 -m venv .venv
```

3\. Activate it

```
.venv\Scripts\activate
```

4\. Install your LangChain dependencies

```
python -m pip install langchain langchain-openai python-dotenv
```

5\. Verify the setup

```
python --version
python -m pip show langchain
```

You should see Python 3.13.x and the installed LangChain package details.

## Install packages from `requirements.txt`

Make sure your project contains a `requirements.txt` file, then run:

```
python -m pip install -r requirements.txt
```

Example `requirements.txt`:

```
langchain
langchain-openai
python-dotenv
```

This installs the packages listed in the file and their required dependencies.

## Deactivate the environment

When you're done working:

```
deactivate
```

### To Upgrade & check pip package -

```
python -m pip install --upgrade pip

python -m pip --version
```

## In LangChain, OpenAI, Google Gemini, and Anthropic use separate integration packages.

Run this command inside your activated virtual environment:

```
python -m pip install langchain-openai langchain-google-genai langchain-anthropic
```

### Example usage

```
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

openai_model = ChatOpenAI(model="gpt-4.1-mini")
gemini_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
claude_model = ChatAnthropic(model="claude-sonnet-4-5")
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

## Maching learning Utilities Packages _ will learn later

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