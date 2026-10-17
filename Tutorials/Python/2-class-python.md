# Functions

## Contents

- [1. Create and call a simple function](#1-create-and-call-a-simple-function)
- [2. Function with parameters](#2-function-with-parameters)
- [3. Function that returns a value](#3-function-that-returns-a-value)
- [4. Function with a default parameter](#4-function-with-a-default-parameter)
- [1. Method Overloading](#1-method-overloading)
  - [But How can we achieve similar behavior in Python](#but-how-can-we-achieve-similar-behavior-in-python)
  - [2. Method Overriding](#2-method-overriding)
    - [Example](#example)
    - [Compare Python vs Java](#compare-python-vs-java)
- [this, in Python we have 'self'](#this-in-python-we-have-self)
- [How to define variables in Python](#how-to-define-variables-in-python)
  - [2. How scope works in Python](#2-how-scope-works-in-python)
    - [A. Local scope](#a-local-scope)
  - [B. Global scope](#b-global-scope)
  - [C. Enclosing scope (nested functions)](#c-enclosing-scope-nested-functions)
  - [3. Important difference: JavaScript `let` vs Python](#3-important-difference-javascript-let-vs-python)
  - [4. What about constants?](#4-what-about-constants)
  - [Quick summary](#quick-summary)
- [Class](#class)
  - [1. How to create a class and an object](#1-how-to-create-a-class-and-an-object)
    - [Why is there no `new` keyword?](#why-is-there-no-new-keyword)
  - [2. Public, protected, and private variables](#2-public-protected-and-private-variables)
  - [3. How to create private methods](#3-how-to-create-private-methods)
  - [4. Java vs Python: quick comparison](#4-java-vs-python-quick-comparison)
  - [5. One additional concept: class variables vs instance variables](#5-one-additional-concept-class-variables-vs-instance-variables)
- [Object || {}](#object--)
  - [2. Three ways to create objects in Python](#2-three-ways-to-create-objects-in-python)
  - [3. What about `Object`?](#3-what-about-object)
- [Data Types](#data-types)
  - [1. Basic data types in Python](#1-basic-data-types-in-python)
  - [2. Collection data types](#2-collection-data-types)
  - [4. Check a variable's data type](#4-check-a-variables-data-type)
  - [5. Python vs JavaScript data types](#5-python-vs-javascript-data-types)
  - [6. Convert between data types](#6-convert-between-data-types)
- [Python Strings — Notes](#python-strings--notes)
  - [1. Creating Strings](#1-creating-strings)
  - [2. Indexing and Slicing](#2-indexing-and-slicing)
  - [3. String Operators](#3-string-operators)
  - [4. Important String Methods](#4-important-string-methods)
  - [5. String Formatting](#5-string-formatting)
  - [6. Multiline Strings and Prompts](#6-multiline-strings-and-prompts)
  - [7. Useful String Modules](#7-useful-string-modules)
  - [8. JSON Strings](#8-json-strings)
  - [9. Common Mistakes](#9-common-mistakes)
- [Python List, Tuple & Dictionary — Quick Notes](#python-list-tuple--dictionary--quick-notes)
  - [1. List (`\[\]`)](#1-list-)
  - [2. Tuple (`()`)](#2-tuple-)
  - [3. Dictionary (`{key: value}`)](#3-dictionary-key-value)
  - [4. Comparison](#4-comparison)
  - [5. Common operations](#5-common-operations)
  - [6. Nested collections](#6-nested-collections)

In Python, you define a function using the `def` keyword and call it using its name followed by parentheses `()`.

## 1. Create and call a simple function

```
def greet():
    print("Hello, World!")

# Call the function
greet()
```

Output:

```
Hello, World!
```

- `def` — defines a function.
- `greet` — function name.
- `()` — holds parameters, if any.
- Indentation — defines the function body.
- `greet()` — calls or executes the function.

## 2. Function with parameters

Parameters let you pass values into a function.
```
def greet(name):
    print(f"Hello, {name}!")

greet("Mohit")
```

## 3. Function that returns a value

Use `return` when you want a function to produce a result that you can reuse.

```
def add(a, b):
    return a + b
```

## 4. Function with a default parameter

```
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()
greet("Mohit")
```

----

# 1. Method Overloading

Method overloading means defining multiple methods with the same name but different parameters.

In Java, this works:

```
add(int a, int b)   
add(int a, int b, int c)
```

In Python, if you define the same method multiple times in a class, the latest definition replaces the previous one.

```
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):
        return a + b + c

calc = Calculator()
print(calc.add(2, 3))
```

This raises a `TypeError` because the second `add()` definition replaces the first, and it requires three arguments.

### But How can we achieve similar behavior in Python

You can use default parameters:

```
class Calculator:
    def add(self, a, b, c=0):
        return a + b + c

calc = Calculator()

print(calc.add(2, 3))       # 5
print(calc.add(2, 3, 4))    # 9
```

You can also use `*args` when the number of arguments varies.

```
def add(*args):
    return sum(args)

print(add(2, 3))        # 5
print(add(2, 3, 4))     # 9
```

Python also supports `@overload` from the `typing` module for describing different type signatures to static type checkers, but it does not create multiple runtime implementations.

## 2. Method Overriding

Method overriding means a child class provides its own implementation of a method inherited from its parent class.

Python supports method overriding natively.

```
class Animal:
    def sound(self):
        print("Animal makes a sound")

class Dog(Animal):
    def sound(self):
        print("Dog barks")

animal = Animal()
dog = Dog()

animal.sound()
dog.sound()
```

Output:

```
Animal makes a sound
Dog barks
```

Here, `Dog` overrides the `sound()` method inherited from `Animal`.

You can also call the parent implementation using `super()`:

```
class Dog(Animal):
    def sound(self):
        super().sound()
        print("Dog barks")
```

Calling `Dog().sound()` prints both messages.
 
 ----

 # Inheritance

There is no separate `extends` keyword like Java. You specify the parent class name inside parentheses `()` when defining the child class.

### Example

Python:

```
class Parent:
    def show(self):
        print("I am the parent class")

class Child(Parent):  # Inheritance
    def display(self):
        print("I am the child class")

obj = Child()
obj.show()     # Inherited method
obj.display()  # Child's own method
```

Output:

```
I am the parent class
I am the child class
```

### Compare Python vs Java

| Concept                    | Python                 | Java                                   |
| -------------------------- | ---------------------- | -------------------------------------- |
| Inheritance syntax         | `class Child(Parent):` | `class Child extends Parent`           |
| Keyword                    | No `extends` keyword   | Uses `extends`                         |
| Call parent constructor    | `super().__init__()`   | `super()`                              |
| Multiple class inheritance | Supported              | Only one direct superclass for classes |

One important distinction: In `class Child(Parent):`, `Parent` is a base class, not an argument passed to a function. The parentheses specify inheritance.

So remember: Python inheritance = class definition + parent class in parentheses.

# this, in Python we have 'self' 

Python does have this-related concepts, In Python, we use self to refer to the current object.

self in Python serves the same purpose, but it is a conventional parameter name, not a Python keyword.

Python passes the object as the first argument to an instance method automatically when you call it through an object.

```java
class Student {
    String name;

    void setName(String name) {
        this.name = name;
    }
}
```

```python
class Student:
    def set_name(self, name):
        self.name = name

student = Student()
student.set_name("Mohit")
```

# How to define variables in Python

```py
name = "Mohit"
age = 34
is_active = True
```

You don't need to declare the variable type or use a special keyword.

| JavaScript           | Python                        |
| -------------------- | ----------------------------- |
| `var name = "Mohit"` | `name = "Mohit"`              |
| `let age = 34`       | `age = 34`                    |
| `const PI = 3.14`    | `PI = 3.14` (convention only) |

Important: Python doesn't have a built-in `const` keyword. Uppercase names such as `PI` are a convention indicating that a value should not be changed.

## 2. How scope works in Python

Python follows the LEGB rule for resolving variable names:

- L — Local: Inside the current function.
- E — Enclosing: Inside an outer function.
- G — Global: At the module/file level.
- B — Built-in: Python's built-in names, such as `print()` and `len()`.

### A. Local scope

A variable created inside a function is normally local to that function.

```py
def greet():    
    message = "Hello"    
    print(message)

greet() 
# print(message)  # NameError
```

`message` is accessible inside `greet()`, not outside it.

## B. Global scope

A variable defined at the top level of a Python file is available throughout that module.

```py
name = "Mohit"

def greet():
    print(name)

greet()  # Mohit
```

To reassign a global variable inside a function, use `global`:

```py
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1
```

Without `global`, assigning to `count` inside the function makes it a local variable instead.

## C. Enclosing scope (nested functions)

```py
def outer():
    message = "Hello"

    def inner():
        print(message)

    inner()

outer()  # Hello
```

The inner function can access the variable from its enclosing function.

To modify that enclosing variable, use `nonlocal`:

```py
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1

    inner()
    print(count)  # 1

outer()
```

## 3. Important difference: JavaScript `let` vs Python

JavaScript's `let` and `const` are block-scoped. Python does not create a new scope for ordinary `if`, `for`, or `while` blocks.

```py
if True:
    message = "Hello"

print(message)  # Hello
```

The variable remains accessible outside the `if` block because an `if` block does not create a separate scope in Python.

Compare that with a function:

```py
def example():
    message = "Hello"

example()
# print(message)  # NameError
```

A function does create a local scope.

## 4. What about constants?

Python has no ordinary variable declaration keyword that makes a value immutable.

```py
MAX_RETRIES = 3
MAX_RETRIES = 5  # Allowed
```

For type-checking tools, you can use `Final`:

```py
from typing import Final

MAX_RETRIES: Final[int] = 3
```

This indicates that the name should not be reassigned, but Python does not enforce it at runtime.

## Quick summary

| Feature                             | JavaScript             | Python                                          |
| ----------------------------------- | ---------------------- | ----------------------------------------------- |
| Variable declaration                | `let`, `const`, `var`  | Assignment (`=`)                                |
| Function scope                      | Yes                    | Yes                                             |
| `if`/`for` block scope              | Yes, for `let`/`const` | No separate scope                               |
| Global reassignment inside function | Different rules        | `global`                                        |
| Modify enclosing function variable  | Closures               | `nonlocal`                                      |
| Constant declaration                | `const`                | Uppercase convention; `Final` for type checkers |

----

# Class

In Python, you can create classes, constructors, instance variables, and methods just like in Java, but the syntax is simpler. The main difference is that Python uses naming conventions instead of strict access modifiers such as `private`, `protected`, and `public`.

## 1. How to create a class and an object

In Java, you use `new` to create an object. In Python, you call the class directly.

Python example:

```py
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")


# Create an object — no 'new' keyword
student = Student("Mohit", 34)

student.display()
```

Output:

```
Name: Mohit, Age: 34
```

What each part means:

- `class Student:` — defines a class.
- `__init__()` — initializes the object's attributes.
- `self` — refers to the current object.
- `Student("Mohit", 34)` — creates an object and initializes it.
- `display()` — an instance method.

### Why is there no `new` keyword?

Python's class-call syntax handles object creation directly. When you write `Student("Mohit", 34)`, Python creates an instance and initializes it.

Internally, Python's `__new__()` method is responsible for creating the instance, while `__init__()` initializes it. You normally don't need to implement `__new__()` yourself.

## 2. Public, protected, and private variables

Python doesn't have Java-style access modifiers. Instead, it uses naming conventions.

Public — `name`

Accessible from outside the class.

```py
self.name = "Mohit"
print(student.name)
```

Protected by convention — `_salary`

A single underscore signals that an attribute is intended for internal use. Python does not prevent outside access.

```py
self._salary = 50000
print(employee._salary)  # Still accessible
```

Name-mangled — `__balance`

A double underscore triggers name mangling, making accidental access and overriding less likely.

```
self.__balance = 1000
```

Accessing `account.__balance` from outside normally raises `AttributeError`.

Important: Python's double underscore does not create truly private variables like Java's `private`. It changes the attribute's internal name, which can still be accessed deliberately.

## 3. How to create private methods

The same naming rules apply to methods.

```py
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if self.__is_valid_amount(amount):
            self.__balance += amount

    def __is_valid_amount(self, amount):
        return amount > 0

    def get_balance(self):
        return self.__balance


account = BankAccount(1000)
account.deposit(500)

print(account.get_balance())  # 1500

# account.__is_valid_amount(100)  # AttributeError
```

Here:

- `deposit()` and `get_balance()` are public methods.
- `__is_valid_amount()` is a name-mangled method intended for internal use.
- `__balance` is a name-mangled attribute.
- `self.__balance` refers to the current object's balance.

Python internally mangles `__balance` to a name similar to `_BankAccount__balance`.

## 4. Java vs Python: quick comparison

| Concept            | Java                      | Python                        |
| ------------------ | ------------------------- | ----------------------------- |
| Define a class     | `class Student`           | `class Student:`              |
| Create an object   | `new Student()`           | `Student()`                   |
| Constructor        | `Student()`               | `__init__()`                  |
| Public variable    | `public String name`      | `self.name`                   |
| Protected variable | `protected`               | `self._name` (convention)     |
| Private variable   | `private String name`     | `self.__name` (name mangling) |
| Private method     | `private void validate()` | `def __validate(self):`       |
| Current object     | `this`                    | `self`                        |

## 5. One additional concept: class variables vs instance variables

```py
class Employee:
    company = "Nagarro"  # Class variable: shared by instances

    def __init__(self, name):
        self.name = name  # Instance variable: belongs to each instance


e1 = Employee("Mohit")
e2 = Employee("Rahul")

print(e1.company)  # Nagarro
print(e2.company)  # Nagarro
print(e1.name)     # Mohit
print(e2.name)     # Rahul
```
----

# Object || {} 

Python supports creating objects using curly braces {}, but that creates a dictionary, not an instance of a class.

## 2. Three ways to create objects in Python

A. Dictionary — `{}`

```py
emp = {"name": "Mohit", "age": 34}
print(emp["name"])
```

Best for simple key-value data.

B. Class instance

```py
class Employee:
    def __init__(self, name):
        self.name = name

emp = Employee("Mohit")
print(emp.name)
```

Best when you need methods, behavior, and structured instances.

C. `SimpleNamespace` — dot notation without defining a class

```py
from types import SimpleNamespace

emp = SimpleNamespace(name="Mohit", age=34)
print(emp.name)  # Mohit
```

Useful when you want JavaScript-like property access for simple data.

## 3. What about `Object`?

Python has a built-in base class named `object`, but you don't normally instantiate it to store arbitrary properties:

```py
obj = object()
```

This creates a basic object, but you cannot add arbitrary attributes to it.

----

# Data Types

Python has several built-in data types. Unlike JavaScript, Python uses different types for integers, floating-point numbers, lists, tuples, sets, and dictionaries.

## 1. Basic data types in Python

| Data type  | Example            | Description         |
| ---------- | ------------------ | ------------------- |
| `int`      | `age = 34`         | Integer numbers     |
| `float`    | `price = 99.5`     | Decimal numbers     |
| `complex`  | `x = 2 + 3j`       | Complex numbers     |
| `str`      | `name = "Mohit"`   | Text/string         |
| `bool`     | `is_active = True` | `True` or `False`   |
| `NoneType` | `result = None`    | Represents no value |


## 2. Collection data types

These are especially important when working with APIs, JSON, and LangChain.

A. List — `list`

Ordered, mutable, allows duplicates.

```py
languages = ["Python", "JavaScript", "Python"]
languages.append("Java")
print(languages[0])  # Python
```

Similar to a JavaScript array.

B. Tuple — `tuple`

Ordered, immutable, allows duplicates.

```py
coordinates = (10, 20)
print(coordinates[0])  # 10
```

Useful for a fixed collection of values.

C. Set — `set`

Stores unique values; does not guarantee positional order.

```py
numbers = {1, 2, 2, 3}
print(numbers)  # {1, 2, 3}
```

Useful for removing duplicates and set operations.

D. Dictionary — `dict`

Stores key-value pairs and is mutable.

```py
employee = {    "name": "Mohit",    "age": 34}
print(employee["name"])  # Mohit
```

Similar to a JavaScript object or a map of key-value pairs.

E. Range — `range`

Represents a sequence of integers, commonly used in loops.

```py
numbers = range(1, 5)
print(list(numbers))  # [1, 2, 3, 4]
```

## 4. Check a variable's data type

Use the built-in `type()` function:

```py
value = [1, 2, 3]
print(type(value))  # <class 'list'>
```

To check whether a value belongs to a particular type, use `isinstance()`:

```py
age = 34
print(isinstance(age, int))  # True
print(isinstance(age, str))  # False
```

## 5. Python vs JavaScript data types

| JavaScript                 | Python equivalent                                                           |
| -------------------------- | --------------------------------------------------------------------------- |
| `Number`                   | `int`, `float`, `complex`                                                   |
| `String`                   | `str`                                                                       |
| `Boolean`                  | `bool`                                                                      |
| `null`                     | `None`                                                                      |
| `undefined`                | No exact equivalent; a missing value may be represented by other mechanisms |
| `Array`                    | `list`                                                                      |
| Object `{}`                | Usually `dict` for key-value data                                           |
| `Set`                      | `set`                                                                       |
| No direct tuple equivalent | `tuple`                                                                     |

## 6. Convert between data types

```py
age = int("34")           # 34
price = float("99.50")    # 99.5
name = str(123)           # "123"
is_valid = bool(1)        # True

print(type(age))          # <class 'int'>
print(type(price))        # <class 'float'>
print(type(name))         # <class 'str'>
```

-----------

# Python Strings — Notes

## 1. Creating Strings

Strings store text. Use single quotes, double quotes, or triple quotes for multiline strings.

```python
name = "Mohit"
message = 'Hello World'

text = """This is a
multiline string."""

print(name)     # Mohit
print(text)
```

**Note:** Strings are immutable, meaning their characters cannot be changed in place.

## 2. Indexing and Slicing

Indexing accesses individual characters. Slicing extracts a portion of a string.

```python
text = "Python"

print(text[0])      # P
print(text[-1])     # n
print(text[0:3])    # Pyt
print(text[::-1])   # nohtyP
```

**Remember:** Indexing starts at `0`; negative indexes start from the end. The slice's ending index is excluded.

## 3. String Operators

```python
a = "Hello"
b = "World"

print(a + " " + b)  # Hello World (concatenation)
print(a * 2)        # HelloHello (repetition)
print("H" in a)     # True (membership)
print(len(a))       # 5 (length)
```

## 4. Important String Methods

Methods generally return a new string without modifying the original.

```python
text = "  Hello Python  "

print(text.upper())                  # "  HELLO PYTHON  "
print(text.lower())                  # "  hello python  "
print(text.strip())                  # "Hello Python"
print(text.replace("Python", "AI"))  # "  Hello AI  "
print(text.startswith("  He"))       # True
print(text.count("o"))               # 2
print(text.find("Python"))           # 8
```

More useful methods:

```python
print("a,b,c".split(","))       # ['a', 'b', 'c']
print("-".join(["a", "b", "c"])) # a-b-c
print("123".isdigit())          # True
print("Python".isalpha())       # True
print("file.pdf".endswith(".pdf")) # True
```

**Remember:** `split()` converts a string into a list; `join()` combines strings into one string.

## 5. String Formatting

**f-strings** are recommended for most modern Python code.

```python
name = "Mohit"
age = 34

print(f"My name is {name}, age {age}.")
# My name is Mohit, age 34.

price = 1234.567
print(f"{price:.2f}")  # 1234.57
```

Other approaches:

```python
print("Hello {}".format("Mohit"))  # Hello Mohit
print("Age: %d" % 34)             # Age: 34
```

## 6. Multiline Strings and Prompts

Triple quotes preserve line breaks and are useful for writing readable AI prompts.

```python
topic = "RAG"

prompt = f"""
Explain {topic} in simple terms.
Include one practical example.
"""

print(prompt)
```

## 7. Useful String Modules

Python's standard library includes these modules; no separate installation is needed.

**`re` — Regular expressions**

```python
import re

text = "My ID is 12345"
result = re.search(r"\d+", text)

print(result.group())  # 12345
```

**`textwrap` — Text formatting**

```python
import textwrap

text = "Python is useful for AI development."
print(textwrap.fill(text, width=15))
```

**`string.Template` — Placeholder-based templates**

```python
from string import Template

template = Template("Hello $name")
print(template.substitute(name="Mohit"))
# Hello Mohit
```

## 8. JSON Strings

Use the `json` module to convert between JSON text and Python data.

```python
import json

text = '{"name": "Mohit", "age": 34}'

data = json.loads(text)  # JSON string -> Python dictionary
print(data["name"])      # Mohit

json_text = json.dumps(data)  # Python data -> JSON string
print(json_text)
```

## 9. Common Mistakes

```python
text = "Python"

# text[0] = "J"  # TypeError: strings are immutable

text = "J" + text[1:]
print(text)  # Jython

print(bool(""))     # False
print(bool("   "))  # True
print(bool("   ".strip()))  # False
```

**Key takeaways:**
- Use `f-strings` for formatting.
- Use triple quotes for multiline text.
- Use `strip()` to remove surrounding whitespace.
- Use `split()` and `join()` to separate and combine text.
- Use `re` for pattern matching and `json` for JSON conversion.
- For LangChain, strings are commonly used to build prompts and process document text.

--------

# Python List, Tuple & Dictionary — Quick Notes

## 1. List (`[]`)

Stores multiple items. **Ordered, mutable, duplicates allowed.**

```
fruits = ["apple", "banana", "mango"]

fruits.append("grape")  # Add
fruits[0] = "orange"    # Update
fruits.remove("banana") # Remove

print(fruits)
# ['orange', 'mango', 'grape']
```

Methods: `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `sort()`.

## 2. Tuple (`()`)

Stores multiple items. **Ordered, immutable, duplicates allowed.**

```
colors = ("red", "green", "blue")

print(colors[0])          # red
print(colors.count("red"))  # 1
print(colors.index("blue")) # 2

# colors[0] = "black"  # TypeError: immutable
```

Single-item tuple: `item = ("apple",)` — the comma is required.

**Use:** Fixed collections such as coordinates.

## 3. Dictionary (`{key: value}`)

Stores **key-value pairs**. Mutable; keys must be unique and hashable.

```py
student = {"name": "Mohit", "age": 34}

print(student["name"])       # Mohit
print(student["grade"])       # Key Error, so to prevent this use get method
print(student.get("grade"))  # None

student["age"] = 35          # Update
student["city"] = "Noida"    # Add
student.pop("city")          # Remove

print(student)
# {'name': 'Mohit', 'age': 35}
```

Methods: `get()`, `keys()`, `values()`, `items()`, `update()`, `pop()`.

Loop through a dictionary:

```py
for key, value in student.items():
    print(key, value)
```

## 4. Comparison

| Feature    | List    | Tuple   | Dictionary     |
| ---------- | ------- | ------- | -------------- |
| Syntax     | `[]`    | `()`    | `{key: value}` |
| Mutable    | Yes     | No      | Yes            |
| Access     | Index   | Index   | Key            |
| Duplicates | Allowed | Allowed | Keys unique    |

## 5. Common operations

```py
numbers = [10, 20, 30]

print(len(numbers))    # 3
print(20 in numbers)   # True
print(numbers[0:2])    # [10, 20]

items = tuple(numbers)
print(items)           # (10, 20, 30)

print(list(items))     # [10, 20, 30]
```

## 6. Nested collections

```py
students = [
    {"name": "Mohit", "score": 90},
    {"name": "Amit", "score": 85}
]

print(students[0]["name"])   # Mohit
print(students[1]["score"])  # 85
```

**Remember:**

- **List:** Changeable collection.
- **Tuple:** Fixed collection.
- **Dictionary:** Key-value data, commonly used for API responses and structured data.

Add sets for a complete comparisonExplain dictionary key restrictions clearly