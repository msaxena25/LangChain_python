# Logging in Python

## How to create logging config

```py
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

## format

The format is customizable.

```py
format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"

OR

format="%(levelname)s - %(message)s"

# 2026-10-23 15:30:10,123 - INFO - retriever - Documents loaded successfully
```

Let's break it down.

| Format field    | Meaning                              | Example                         |
| --------------- | ------------------------------------ | ------------------------------- |
| `%(asctime)s`   | Date and time                        | `2026-10-23 15:30:10,123`       |
| `%(levelname)s` | Logging level                        | `INFO`, `ERROR`, `WARNING`      |
| `%(name)s`      | Logger's name, often the module name | `retriever`                     |
| `%(message)s`   | The message you pass to the logger   | `Documents loaded successfully` |

----

## What does `level` mean?

It tells Python which log messages to record, based on their severity.

| Level      | Meaning                                        |
| ---------- | ---------------------------------------------- |
| `DEBUG`    | Detailed information for debugging             |
| `INFO`     | Normal application progress                    |
| `WARNING`  | Something unexpected, but the app can continue |
| `ERROR`    | An operation failed                            |
| `CRITICAL` | A very serious problem                         |

For example, if you set `level=logging.WARNING`, Python records `WARNING`, `ERROR`, and `CRITICAL` messages, but ignores `DEBUG` and `INFO`.

**Default:** If you dont provide level, By default, the root logger's threshold is `WARNING`.

----

## How to use?

### Without logging

```py
def greet(name):
    print(f"Hello, {name}")

greet() # called without argument
```

Python raises a `TypeError` because the required `name` argument is missing.

### With logging

The important point is that the error happens when you call the function, so put the function call inside a `try-except` block.

```py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def greet(name):
    print(f"Hello, {name}")

try:
    greet()
except TypeError:
    logger.exception("Failed to call greet()")
```

The log will contain a message similar to:

```py
ERROR:__main__:Failed to call greet()
Traceback (most recent call last):
...
TypeError: greet() missing 1 required positional argument: 'name'
```

`logger.exception()` records the error message and traceback, helping you identify where and why the error occurred.

-----------

## How to choose the logging level

- `INFO`: normal milestones in the workflow.
- `DEBUG`: detailed internal steps.
- `WARNING`: an unexpected result that the application can handle.
- `EXCEPTION`: an operation failed; log the traceback and re-raise the error.

`logger.exception()` is a convenient way to log an error with its traceback inside an exception handler. You don't need to use it for every exception if you already log the same failure at another layer.

## The practical rule developers follow

| Ask yourself                                                | Choose     |
| ----------------------------------------------------------- | ---------- |
| Do I need detailed diagnostic information?                  | `DEBUG`    |
| Is this normal, useful progress?                            | `INFO`     |
| Is something unusual, but recoverable?                      | `WARNING`  |
| Did an operation fail?                                      | `ERROR`    |
| Is the application or a critical service in severe trouble? | `CRITICAL` |

-------

## Key differences print vs logging

| Feature                                | `print()`               | `logging`                                       |
| -------------------------------------- | ----------------------- | ----------------------------------------------- |
| Display a message                      | Yes                     | Yes, when configured                            |
| Severity levels                        | No built-in levels      | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| Timestamp and severity in each message | Must implement yourself | Configurable                                    |
| Save messages to a file                | Requires extra code     | Built-in file handlers                          |
| Filter messages by severity            | Must implement yourself | Built in                                        |
| Include exception traceback            | Requires extra code     | `logger.exception()`                            |
| Control output across multiple modules | Requires your own setup | Centralized configuration                       |

-----

## Configure logging at the application level

This gives you centralized configuration and makes it easier to identify which file produced each log message.

### 1. Recommended project structure

In `main.py`: at the application level

```py
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# getLogger(__name__) — create a named logger for a module.
logger = logging.getLogger(__name__)
logger.info("Application started")
```

This configures the root logger and its default file handler.

### 2. Create a logger in each Python file

In `document_loader.py`, or any file :

```py
import logging

logger = logging.getLogger(__name__) # this line is important

def load_documents():
    logger.info("Loading documents")
    # Document loading logic
```

------

