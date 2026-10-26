# Python Reading Plan

Goal: become a fluent Python developer with core knowledge, everyday useful concepts, and advanced concepts, and be ready for a senior Python developer interview.

This plan is based on `Tutorials/Python` (class notes 1 through 8) and `Python-Code` (practice files). `Tutorials/Python/0-python_course.md` is a checklist only. Several items on that checklist are not in the class notes yet, so they appear below as topics still to cover.

Suggested path: close the core gaps, then the standard library, then build one real API with tests, then concurrency and the data model, then interview drills.

---

## Topics already covered

### Language, setup, and how Python runs

- Python history, creator, versions, and the ABC language
- Why Python is widely used in AI and machine learning
- Execution flow: source, bytecode, virtual machine, and `.pyc` files
- Installing Python, `pip`, and running modules with `python -m`
- Virtual environments (`venv`)
- `requirements.txt`
- `import` and `from ... import`
- Packages, `__init__.py`, and importing across folders
- Loading a module dynamically
- File and folder naming
- Built-in modules at a first level: `os`, `sys`, `math`, `json`, `datetime`

### Data, operators, and control flow

- Variables, naming, and constants by convention
- Scope: local, enclosing, global, and `nonlocal`
- Basic types: `int`, `float`, `complex`, `str`, `bool`, `None`
- `type()`, `isinstance()`, and type conversion
- Collections: list, tuple, set, dict, range, and nested collections
- Strings: creation, indexing, slicing, methods, formatting, multiline text, immutability
- `string.Template` and `textwrap`
- A first `re.search` example
- Logical operators, membership (`in`), and `and` versus `&`
- `if` / `elif` / `else`
- `for`, `while`, `range`, `enumerate`
- `break`, `continue`, `pass`
- `for-else` and `while-else`
- `match-case`
- `input()` and `print()`, including `sep` and `end`
- f-strings and `str.format()`
- Slicing with step, including reverse slices
- List comprehensions, including filter and nested comprehensions
- Small programs: palindrome check and factorial (loop and recursion)

### Functions

- Defining and calling functions, default parameters, and return values
- Positional arguments and keyword arguments
- Unpacking with `*` and `**`
- `*args`, and a first `**kwargs` example in practice code
- Lambda functions
- `map()` and `filter()`
- Why Python replaces a second method definition, and how defaults or `*args` cover that case
- A mention of `typing.overload` for type checkers

### Object-oriented programming

- Classes, objects, `self`, and creating objects without `new`
- Instance variables and class variables
- Public, protected (`_name`), and private (`__name`) names
- Inheritance and method overriding
- Encapsulation
- Abstract classes and `@abstractmethod`
- `@property`, setter, and deleter
- `@staticmethod`, and how Python passes the instance into a normal method
- `@dataclass`
- Magic methods started: `__init__`, `__repr__`, `__eq__`, `__add__`, `__len__`

### Types and validation

- Type hints on variables and functions
- Hints for `list`, `dict`, `tuple`, and `set`
- `Any`, unions with `|`, `Literal`, and `str | None`
- `TypedDict`, `total=False`, and `NotRequired`
- Pydantic `BaseModel`, `Field`, coercion, and strict types
- Pydantic practice: enums, nested models, `ConfigDict`, field and model validators, computed fields, `EmailStr`, `HttpUrl`, `SecretStr`, `Decimal`, `Annotated`

### Errors, files, logging, and HTTP

- `try` / `except` / `else` / `finally` and common exceptions
- `open`, `with`, `read`, `readline`, `readlines`, the file pointer, and `seek`
- Text files, binary mode, JSON (`load` / `loads`), creating CSV and PDF files, reading PDFs with `pypdf`
- `pathlib`: exists, mkdir, read/write text, resolve, glob, rglob
- Logging: levels, format, `getLogger(__name__)`, and logging versus `print`
- `requests`: GET, POST, and raising on HTTP errors
- `urllib` GET and POST

### Touched, still thin

These names appeared in the notes or practice code. Treat them as introductions, and study the fuller topic in the sections below.

- Sets (uniqueness only; set algebra is still open)
- `re` (one search example)
- `*args` / `**kwargs` (used, not the full parameter rules)
- `array.array` (imported in practice code)
- `Enum` and `Decimal` (used inside Pydantic, not as their own lessons)
- `@classmethod` (used on a Pydantic validator)

---

## Topics still left

Each line is the topic and what you should be able to do with it.

### 1. Core gaps — finish fluency

- **Mutable versus immutable, and hashability** — Know which values can change in place, which cannot, and which can be dictionary keys or set members.
- **Shallow copy versus deep copy** — Copy a nested list or dict with `copy.copy` and `copy.deepcopy` and predict what still shares inner objects.
- **Identity versus equality (`is` and `==`)** — Tell whether two names point at the same object or only hold equal values.
- **Truthy and falsy values** — Predict how `if` treats `None`, `0`, empty strings, and empty collections.
- **Sets in practice** — Use union, intersection, difference, and a set to drop duplicates.
- **Dictionary patterns** — Use `get`, `setdefault`, `update`, merge with `|`, and loop over `items` without mutating the dict unsafely.
- **Dictionary and set comprehensions** — Build dicts and sets in one expression, the same way you already build lists.
- **`zip`, `any`, `all`, `sorted`, `reversed`** — Pair sequences, test a whole collection, and order data with a key function.
- **Full argument rules** — Write positional-only (`/`), keyword-only (`*`), `*args`, and `**kwargs` parameters in a legal order.
- **Mutable default arguments** — Explain and avoid the shared default list or dict that remembers earlier calls.
- **Closures and late binding** — Explain what a nested function captures, and why a lambda inside a loop often sees the final variable.
- **Custom exceptions and `raise`** — Define your own error types, raise them, and attach a cause with `raise ... from`.
- **`except*` and exception groups** — Read and raise several related failures together, as added in Python 3.11.
- **Iterators** — Explain iterable versus iterator, and drive a loop with `iter()` and `next()`.
- **Generators and `yield`** — Produce values one at a time so a large sequence does not all sit in memory.
- **Generator expressions and `yield from`** — Write a lazy comprehension and delegate to another generator.
- **Decorators** — Write a wrapper with `@`, and keep the original function name with `functools.wraps`.
- **Decorators with arguments, and stacked decorators** — Pass options into a decorator and apply more than one wrapper.
- **`@classmethod`** — Add alternate constructors that receive the class instead of an instance.
- **Dunder methods for real classes** — Implement `__str__`, `__hash__`, ordering, `__getitem__`, `__iter__`, `__contains__`, `__bool__`, and `__call__`.
- **`__new__` versus `__init__`** — Separate object allocation from initialization.
- **Context managers you write** — Support `with` using `__enter__` / `__exit__` and `@contextlib.contextmanager`.
- **Multiple inheritance and the MRO** — Explain how `super()` walks parent classes and how Python resolves a diamond hierarchy.
- **Duck typing** — Call methods on any object that has the right behavior, without requiring one shared base class.
- **`bytes`, `str`, and encoding** — Keep text and raw bytes apart, and use UTF-8 at file and HTTP boundaries.
- **`float` versus `Decimal`** — Choose `Decimal` for money and other values that must stay exact.
- **Walrus operator (`:=`)** — Assign inside a condition or loop when that makes the code clearer.
- **`match-case` in depth** — Match sequences, mappings, classes, alternatives, and guards.
- **`if __name__ == "__main__"`** — Let one file be imported as a module and also run as a script.
- **Circular imports** — Recognize the failure and restructure imports so modules load cleanly.
- **`__all__` and public exports** — Decide what a package exposes to `from package import *` and to readers.
- **Docstrings** — Document a function’s purpose, arguments, and return value so `help()` and reviewers can use it.
- **PEP 8 and a formatter** — Follow community layout, and let Ruff or Black apply it.
- **Debugging** — Read a traceback, stop in `breakpoint()` / `pdb`, and inspect state at the failure.

### 2. Useful concepts — standard library and daily work

- **`collections.Counter`, `defaultdict`, and `deque`** — Count items, fill missing keys, and add or pop from both ends of a queue.
- **`namedtuple` and `typing.NamedTuple`** — Use a small immutable record with named fields.
- **`itertools`** — Chain iterables, group neighbors, and build products or windows without hand-written nested loops.
- **`functools.partial`, `reduce`, `cache`, and `lru_cache`** — Fix some arguments, fold a sequence, and remember expensive results.
- **`enum`** — Define a closed set of named constants, including `auto()` and string enums.
- **Dataclasses in depth** — Use `field`, `default_factory`, `frozen=True`, `slots=True`, ordering, and `asdict`.
- **Typing for larger code** — Use `Callable`, `TypeAlias`, `Annotated`, `Self`, and `cast` with intent.
- **`Protocol`** — Describe required methods without forcing a class hierarchy.
- **Generics and `TypeVar`** — Keep one type consistent from a function’s input to its output.
- **Regular expressions in depth** — Use `findall`, `sub`, groups, and compiled patterns, and know when a string method is enough.
- **`csv` module** — Read and write header rows, quoting, and dialects.
- **`datetime` in depth** — Use `timedelta`, timezone-aware values, and `strptime` / `strftime`.
- **`pathlib` for scripts** — Use `parents`, `relative_to`, byte read/write, and a directory walk.
- **`os` and `sys` for scripts** — Read environment variables, `argv`, and process exit codes.
- **`argparse`** — Build a command-line tool with flags, help text, and typed options.
- **`json` in depth** — Use `dump` and `dumps`, and encode values such as dates that JSON does not know.
- **Logging handlers and rotation** — Send logs to a file, split format from level, and rotate large files.
- **Environment variables and `.env`** — Load configuration and secrets from the environment, and keep them out of source code.
- **`secrets`, `uuid`, and `hashlib`** — Create tokens and ids, and hash values for integrity checks.
- **`heapq` and `bisect`** — Keep a priority queue and insert into a sorted sequence quickly.
- **`sqlite3`** — Store and query local relational data with the standard library.
- **Project packaging** — Describe a project in `pyproject.toml`, use a `src` layout, and install it in editable mode.
- **Repeatable installs** — Lock dependency versions with a tool such as `uv` or `pip-tools`.
- **HTTP as a client** — Use timeouts, sessions, retries, headers, and status codes with purpose.
- **FastAPI** — Expose routes, validate bodies with Pydantic, and inject dependencies.
- **`httpx` async client** — Call HTTP without blocking, once `async` / `await` is in place.
- **SQL basics** — Write `SELECT`, `INSERT`, `UPDATE`, `DELETE`, joins, and a simple index.
- **SQLAlchemy (or one ORM)** — Map classes to tables and commit work through a session.
- **Error-handling policy** — Decide what to catch at a boundary, what to let travel, and what the caller should see.

### 3. Advanced language concepts

- **How `@` becomes a call** — Trace a decorator as a function that receives a function and returns a wrapper, including decorators that take arguments.
- **Descriptors** — Explain `__get__`, `__set__`, and `__delete__`, and how `@property` is built on that protocol.
- **`__slots__`** — Restrict attributes and reduce memory when a program creates many small objects.
- **`__init_subclass__`** — Hook subclass creation without writing a metaclass.
- **Metaclasses** — Explain how a class object is created, and when a decorator or `__init_subclass__` is the better tool.
- **Container protocol** — Make your own class support `len`, `for`, indexing, and `in`.
- **`__eq__` and `__hash__` together** — Keep equal objects hash-compatible so they can live in sets and as dict keys.
- **`contextlib` tools** — Use `suppress`, `closing`, and `ExitStack` when several resources open together.
- **Reference counting and cyclic GC** — Explain how CPython frees objects, and when a cycle needs the garbage collector.
- **Weak references** — Hold a cache entry that must not keep the original object alive.
- **Small integers, interning, and `id()`** — Explain the identity surprises interviewers use with small ints and some strings.
- **The GIL** — Explain why CPU-bound threads do not scale in CPython, and what that means for design.
- **`threading`** — Run I/O-bound work on threads and protect shared data with a `Lock`.
- **`multiprocessing` and `ProcessPoolExecutor`** — Use separate processes for CPU-bound work.
- **`concurrent.futures`** — Submit work to a thread pool or a process pool through one interface.
- **`asyncio`** — Write `async` / `await` code, create tasks, and wait with `gather`.
- **Async patterns** — Use timeouts, `TaskGroup`, async context managers, and async queues.
- **Choosing a concurrency model** — Pick threads, processes, or async from the workload: waiting on I/O, or burning CPU.
- **`contextvars`** — Keep request-scoped data across async tasks without adding a parameter to every function.
- **Profiling** — Measure with `timeit` and `cProfile` before rewriting code for speed.
- **Streaming with generators** — Read large files or paged APIs one chunk at a time.
- **`pickle` and trust** — Know the built-in serializer, and refuse to load pickle data you did not create.
- **Buffer protocol (awareness)** — Know that `memoryview` exposes raw bytes for large binary data.
- **Typing variance (awareness)** — Recognize covariant and contravariant generics if an interview question goes there.
- **Import machinery (awareness)** — Explain `sys.path`, finders, and loaders well enough to debug a bad import.

### 4. Senior interview and production engineering

- **pytest** — Write tests, assert outcomes, and run a suite from the command line.
- **Fixtures and parametrize** — Share setup and run one test body over many inputs.
- **Mocking** — Replace the network, clock, or database so a unit test stays local and repeatable.
- **Test layers** — Separate unit tests, integration tests, and a few end-to-end checks.
- **Static type checking** — Run mypy or Pyright and treat type errors as part of the workflow.
- **Ruff** — Catch unused code, risky patterns, and style issues in one linter.
- **Application layout** — Split domain logic, API handlers, configuration, and tests into clear modules.
- **Pythonic design patterns** — Implement strategy, factory, and adapter with functions, classes, or callables as fits the problem.
- **SOLID and composition** — Prefer small collaborating objects over a deep inheritance tree.
- **Dependency injection by hand** — Pass collaborators into constructors so behavior can be swapped in tests.
- **API design in Python** — Choose stable signatures, precise return types, and errors a caller can handle.
- **REST habits** — Model resources, pick status codes, paginate lists, and keep safe methods idempotent.
- **API authentication** — Use API keys or bearer tokens, and keep secrets out of logs and git.
- **Database transactions** — Commit a complete unit of work and roll back when a step fails.
- **Caching** — Use `functools.cache` in-process, and describe a shared cache such as Redis when many processes run.
- **Background jobs** — Move slow work to a queue and worker so a request can return quickly.
- **Structured logging** — Emit fields (request id, user, status) that a log system can filter.
- **Configuration by environment** — Run the same code with different settings per machine.
- **Python security pitfalls** — Avoid `eval` / `exec` on user input, SQL built by string concat, untrusted pickle, and path traversal.
- **Complexity of built-in collections** — State typical cost of lookup and insert for list, set, and dict.
- **Race conditions and deadlocks** — Describe how shared mutable state breaks, and how a lock order avoids deadlock.
- **Versioning and compatibility** — Use semantic versioning and say what counts as a breaking change.
- **What `for` and `with` call** — Name the dunder methods those statements use.
- **Code review standard** — Look for names, small functions, hidden shared state, and missing tests.
- **A small system sketch** — Describe an API service with an app process, a database, a cache, and a worker, and where Python sits in each piece.

---

## Order to study

1. **Core gaps.** Copies, `is` versus `==`, truthiness, dict and set fluency, iterators, generators, decorators, closures, custom exceptions, context managers, MRO, the rest of the dunder methods, bytes and encoding, `Decimal`, and the main-guard. This is the fluency layer.
2. **Standard library.** `collections`, `itertools`, `functools`, `enum`, deeper dataclasses, `Protocol`, regex, `csv`, dates, `argparse`, logging handlers, and environment-based configuration.
3. **One real project.** A FastAPI service that validates input with Pydantic, stores data in SQLite or SQLAlchemy, reads config from the environment, logs structured lines, and has pytest coverage. This is the evidence a senior interview expects.
4. **Advanced runtime.** GIL, threads, processes, asyncio, descriptors, slots, garbage collection, and profiling.
5. **Interview drills.** Answer out loud: mutable defaults, `is` versus `==`, GIL, shallow versus deep copy, decorator mechanics, generator versus list, MRO, async versus threads, how you would test a function that calls HTTP, and how you would design a small CRUD API.

## Interview questions to be able to answer

- Why can a list not be a dict key, while a tuple sometimes can?
- What does a mutable default argument actually store?
- What is the difference between `is` and `==`?
- What does a `for` loop call on your object?
- How does a decorator change the function that gets called?
- When do you use a generator instead of a list?
- What problem does the GIL create, and what does it leave alone?
- When would you choose threads, processes, or `asyncio`?
- How does `super()` decide the next class?
- What is a race condition, and what is a deadlock?
- How do you test code that calls an external API?
- How do you keep secrets out of the repository?
- What is a transaction, and what happens if you skip the rollback?
- How would you structure a Python service a new teammate can run and test?
