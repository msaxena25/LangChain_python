# Python Core Concepts — Learning Checklist

## 1. Python Fundamentals

- Variables and naming conventions
- Data types: `int`, `float`, `str`, `bool`, `None`
- Type checking: `type()`, `isinstance()`
- Type conversion: `int()`, `str()`, `float()`
- Input and output: `input()`, `print()`
- Comments and indentation
- Operators: arithmetic, comparison, logical, assignment, membership, identity
- String formatting: f-strings

## 2. Conditional Statements & Loops

- `if`, `elif`, `else`
- Nested conditions
- `for` and `while` loops
- `range()`
- `break`, `continue`, `pass`
- `match-case` (Python 3.10+)
- `enumerate()`, `zip()`
- Loop `else`

## 3. Data Structures

- Lists — create, access, update, add, remove, slice
- Tuples — immutable sequences
- Sets — unique values, union, intersection
- Dictionaries — keys, values, update, delete
- Nested lists and dictionaries
- List, set and dictionary comprehensions
- Mutable vs immutable objects
- Copying: shallow copy vs deep copy

## 4. Strings

- Indexing and slicing
- String methods: `split()`, `join()`, `replace()`, `strip()`
- Searching: `find()`, `in`, `startswith()`
- Formatting and f-strings
- Escape characters and multiline strings

## 5. Functions

- Defining functions with `def`
- Parameters and arguments
- `return` vs `print()`
- Default and keyword arguments
- Positional and keyword-only arguments
- `*args` and `**kwargs`
- Lambda functions
- Scope: local and global variables
- Recursion
- Docstrings and type hints

## 6. Modules, Packages & Environments

- `import` and `from ... import`
- Built-in modules: `os`, `sys`, `math`, `json`, `datetime`
- Creating custom modules and packages
- `pip` and package installation
- Virtual environments: `venv`
- `requirements.txt`
- Environment variables and `.env` files

## 7. Exception Handling

- Errors vs exceptions
- `try`, `except`, `else`, `finally`
- Handling specific exceptions
- Raising exceptions: `raise`
- Creating custom exceptions
- Debugging and tracebacks

## 8. File Handling & Data Processing

- Reading and writing files
- `with open()` context manager
- File paths using `pathlib`
- JSON: `json.load()`, `json.dump()`
- CSV processing
- Working with text and binary files
- Regular expressions: `re`

## 9. Object-Oriented Programming (OOP)

- Classes and objects
- `__init__()` and `self`
- Instance vs class attributes
- Instance, class and static methods
- Encapsulation
- Inheritance
- Polymorphism
- Abstraction
- Properties: `@property`
- Magic/dunder methods
- Dataclasses

## 10. Iterators, Generators & Functional Concepts

- Iterable vs iterator
- `iter()` and `next()`
- Generators and `yield`
- `map()`, `filter()`, `sorted()`
- `any()` and `all()`
- `lambda` with sorting and filtering
- Decorators
- Closures

## 11. Advanced Python Essentials

- Context managers
- Unpacking and destructuring
- Identity (`is`) vs equality (`==`)
- Truthy and falsy values
- `None` handling
- Type hints and generics
- Structural pattern matching
- Concurrency: threading and multiprocessing
- Asynchronous programming: `async`, `await`, `asyncio`
- Memory management basics

## 12. Testing & Code Quality

- Unit testing: `unittest` or `pytest`
- Assertions
- Mocking dependencies
- Logging
- Debugging with breakpoints
- PEP 8 style guidelines
- Code organization and reusable functions

## 13. Python for APIs & AI Development

Especially useful for your LangChain learning path.

- HTTP requests using `requests` or `httpx`
- REST APIs and HTTP status codes
- Working with JSON API responses
- FastAPI basics
- Pydantic models and data validation
- Type hints and structured data
- API keys and secrets management
- Basic SQL and database connectivity
- Async API calls
- Working with model responses and token usage

Recommended order: Fundamentals → Control Flow → Data Structures → Functions → Modules and Environments → Exceptions and Files → OOP → Iterators and Generators → APIs → Testing → Advanced Python.

For LangChain, prioritize lists, dictionaries, functions, classes, imports, virtual environments, exceptions, JSON, type hints, Pydantic, and API requests before moving into advanced concurrency.