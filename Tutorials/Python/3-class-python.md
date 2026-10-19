# Python control flow statements

## Contents

- [1. `if`, `elif`, and `else`](#1-if-elif-and-else)
- [2. `for` loop](#2-for-loop)
  - [Using `range()`](#using-range)
  - [Using `enumerate()`](#using-enumerate)
- [3. `while` loop](#3-while-loop)
- [4. `break`, `continue`, and `pass`](#4-break-continue-and-pass)
  - [A. `break` — exit the loop](#a-break--exit-the-loop)
  - [B. `continue` — skip the current iteration](#b-continue--skip-the-current-iteration)
  - [C. `pass` — do nothing](#c-pass--do-nothing)
- [5. `match-case` — Python's switch-like statement](#5-match-case--pythons-switch-like-statement)
- [6. Other useful control flow concepts](#6-other-useful-control-flow-concepts)
  - [A. `in` — check membership](#a-in--check-membership)
  - [B. `and`, `or`, and `not` — combine conditions](#b-and-or-and-not--combine-conditions)
  - [C. `for-else` and `while-else`](#c-for-else-and-while-else)
- [Input and Output (`input()`, `print()`)](#input-and-output-input-print)
  - [Quick revision](#quick-revision)
- [f-string and str.format()](#f-string-and-strformat)
- [Python Lambda Functions](#python-lambda-functions)
  - [1. What is a lambda function?](#1-what-is-a-lambda-function)
  - [2. Syntax](#2-syntax)
  - [3. Examples](#3-examples)
  - [4. Lambda vs. normal function](#4-lambda-vs-normal-function)
  - [5. Why do we use lambda in LangChain?](#5-why-do-we-use-lambda-in-langchain)
- [Python map and filter function](#python-map-and-filter-function)
  - [1. Understanding `map()`](#1-understanding-map)
  - [2. Understanding `filter()`](#2-understanding-filter)
  - [4. Combining `filter()` and `map()`](#4-combining-filter-and-map)
- [dictionary unpacking (**) with Python's string formatting.](#dictionary-unpacking--with-pythons-string-formatting)
- [`and`, `or`, and `not`](#and-or-and-not)
  - [1. `and` operator](#1-and-operator)
  - [2. `or` operator](#2-or-operator)
  - [3. `not` operator](#3-not-operator)
  - [4. Practical example](#4-practical-example)
  - [5. Important difference: `and` vs `&`](#5-important-difference-and-vs-)
- [Define types for a variable](#define-types-for-a-variable)
  - [1. How to define a type for a variable](#1-how-to-define-a-type-for-a-variable)
  - [2. How to define types for collections](#2-how-to-define-types-for-collections)
  - [A. List — `list\[type\]`](#a-list--listtype)
  - [B. Dictionary — `dict\[key_type, value_type\]`](#b-dictionary--dictkey_type-value_type)
  - [C. Tuple — `tuple\[type, ...\]`](#c-tuple--tupletype-)
  - [D. Set — `set\[type\]`](#d-set--settype)
  - [E. Other important type hints](#e-other-important-type-hints)
  - [4. How to define types for functions](#4-how-to-define-types-for-functions)
- [Inheritance](#inheritance)
  - [Code Example](#code-example)
  - [Compare Python vs Java](#compare-python-vs-java)
- [Abstract Class and Abstract Method in Python](#abstract-class-and-abstract-method-in-python)
  - [1. Simple example](#1-simple-example)
  - [2. What happens if we don't implement the abstract method?](#2-what-happens-if-we-dont-implement-the-abstract-method)
- [Encapsulation](#encapsulation)
  - [Without encapsulation](#without-encapsulation)
  - [With encapsulation](#with-encapsulation)
- [@property & @property.setter decorator](#property--propertysetter-decorator)
  - [The bigger real-world benefit: Changing implementation without breaking callers](#the-bigger-real-world-benefit-changing-implementation-without-breaking-callers)
- [`@property.deleter`](#propertydeleter)
  - [1. Without a property deleter](#1-without-a-property-deleter)
  - [2. With `@price.deleter`](#2-with-pricedeleter)
- [`@staticmethod` decorator](#staticmethod-decorator)
  - [Lets deep more - What Python do automatically when you call a method?](#lets-deep-more---what-python-do-automatically-when-you-call-a-method)
    - [1. Regular method without `self`](#1-regular-method-without-self)
    - [2. With `@staticmethod`](#2-with-staticmethod)
- [`@dataclass`](#dataclass)
  - [1. Without `@dataclass`](#1-without-dataclass)
  - [2. With `@dataclass`](#2-with-dataclass)
- [Understand `__repr__() & `__eq__()`](#understand-__repr__--__eq__)
  - [1. `__repr__()` — Useful object representation](#1-__repr__--useful-object-representation)
    - [Without `__repr__()`:](#without-__repr__)
    - [With `__repr__()`:](#with-__repr__)
  - [2. `__eq__()` — Compare objects by their data](#2-__eq__--compare-objects-by-their-data)

# 1. `if`, `elif`, and `else`

Used to execute different code based on conditions.

```py
age = 20

if age < 18:
    print("Minor")
elif age < 60:
    print("Adult")
else:
    print("Senior citizen")

# Output:
# Adult
```

- `if`: Checks the first condition.
- `elif`: Checks another condition if previous conditions are false. You can use multiple `elif` blocks.
- `else`: Runs when all previous conditions are false.
- Indentation matters: Python uses indentation instead of `{}` to define code blocks.

# 2. `for` loop

Used to iterate over a sequence, such as a list, string, or range of numbers.

```py
fruits = ["Apple", "Banana", "Mango"]

for fruit in fruits:
    print(fruit)

# Output:
# Apple
# Banana
# Mango
```

### Using `range()`

`range(start, stop, step)` generates a sequence of integers. The `stop` value is excluded.

```py
for i in range(1, 6):
    print(i)

# Output:
# 1
# 2
# 3
# 4
# 5
```

### Using `enumerate()`

Use `enumerate()` when you need both the index and the value.

```py
fruits = ["Apple", "Banana", "Mango"]

for index, fruit in enumerate(fruits):
    print(index, fruit)

# Output:
# 0 Apple
# 1 Banana
# 2 Mango
```

To start indexing from 1:

```py
for index, fruit in enumerate(fruits, start=1):
    print(index, fruit)

# Output:
# 1 Apple
# 2 Banana
# 3 Mango
```

# 3. `while` loop

Repeats code as long as the condition is `True`.

```py
count = 1

while count <= 3:
    print(count)
    count += 1

# Output:
# 1
# 2
# 3
```

# 4. `break`, `continue`, and `pass`

These statements control loop execution.

### A. `break` — exit the loop

```py
for i in range(1, 6):
    if i == 3:
        break
    print(i)

# Output:
# 1
# 2
```

The loop stops completely when `i == 3`.

### B. `continue` — skip the current iteration

```py
for i in range(1, 6):
    if i == 3:
        continue
    print(i)

# Output:
# 1
# 2
# 4
# 5
```

The loop skips printing `3` but continues with the remaining numbers.

### C. `pass` — do nothing

```py
for i in range(1, 4):
    if i == 2:
        pass
    print(i)

# Output:
# 1
# 2
# 3
```

`pass` is a placeholder. It does not skip an iteration or stop the loop.

# 5. `match-case` — Python's switch-like statement

Python introduced `match-case` in Python 3.10. It is the closest built-in equivalent to a traditional `switch` statement.

```py
day = 2

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case _:
        print("Invalid day")

# Output:
# Tuesday
```

- `match`: Checks the value against patterns.
- `case`: Defines a matching pattern.
- `case _`: Acts as the default case.

# 6. Other useful control flow concepts

## A. `in` — check membership

```py
languages = ["Python", "JavaScript", "Java"]

if "Python" in languages:
    print("Python is available")

# Output:
# Python is available
```

## B. `and`, `or`, and `not` — combine conditions

```py
age = 25
has_id = True

if age >= 18 and has_id:
    print("Access granted")

if age < 18 or not has_id:
    print("Access denied")

# Output:
# Access granted
```

- `and`: Both conditions must be true.
- `or`: At least one condition must be true.
- `not`: Reverses a Boolean value.

## C. `for-else` and `while-else`

The `else` block runs when the loop finishes normally, but not when it exits through `break`.

```py
for i in range(1, 4):
    print(i)
else:
    print("Loop completed")

# Output:
# 1
# 2
# 3
# Loop completed
```

Example with `break`:

```py
for i in range(1, 4):
    if i == 2:
        break
else:
    print("Loop completed")

# Output:
# No output
```

This is useful when searching a list and you want to know whether an item was found.

----


# Input and Output (`input()`, `print()`)

- `print()` displays information on the screen.
- `input()` accepts user input and always returns it as a string (`str`), even when the user enters a number.

```py
# 1. print() - Display output
print("Hello, Python!")
print(100)

# Output:
# Hello, Python!
# 100


# 2. input() - Accept user input
name = input("Enter your name: ")
print("Hello", name)

# Example input: Mohit
# Output: Hello Mohit


# 3. input() returns a string
age = input("Enter your age: ")
print(type(age))

# Example input: 25
# Output: <class 'str'>


# 4. Convert input to an integer
age = int(input("Enter your age: "))
print(age + 1)

# Example input: 25
# Output: 26


# 5. Convert input to a float
price = float(input("Enter price: "))
print(price)

# Example input: 99.5
# Output: 99.5


# 6. Take multiple inputs using split()
first_name, last_name = input("Enter full name: ").split()
print(first_name)
print(last_name)

# Example input: Mohit Saxena
# Output:
# Mohit
# Saxena

# 7. print() separator and end
print("Python", "Java", "JavaScript", sep=" | ")
print("Hello", end=" ") #by default end make new lines but here end is space.
print("World")

# Output:
# Python | Java | JavaScript
# Hello World


# 9. Calculate using user input
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Sum:", a + b)

# Example inputs: 10 and 20
# Output: Sum: 30

```
----

# f-string and str.format() 

```py
# f-string need variable upfront to format string.
# f-strings evaluate variables immediately; they don't remain dynamic templates automatically.
topic="angular"
level="junior"
str1 = f"Explain {topic} for {level} developer."
print(str1)

# how can we pass dynamically variables in f-string?
# We can create a method and call that with variables
def formatString(topic, level):
    str2 = f"Explain {topic} for {level} developer."
    return str2

print(formatString("Java", "senior"))

# string.format

# string.format does not modify origional string, it returns new string.
str = "Explain {topic} for {level} developer."
output = str.format(topic="angular", level="beginner") 
print(output)

# use string.format in a function
str3 = "Explain {topic} for {level} developer."
def formatString1(topic, level):
    return str3.format(topic=topic, level=level)

print(formatString1('React', "Expert"))
```

---


# Python Lambda Functions

## 1. What is a lambda function?

A lambda function is a small, anonymous function written in a single expression. It is useful when you need a short function without defining it using `def`.

Normal function using `def`:

```py
def add(a, b):
    return a + b

print(add(10, 20))
```

Output: `30`

The same function using `lambda`:

```py
add = lambda a, b: a + b

print(add(10, 20))
```

Output: `30`

Both perform the same operation.

## 2. Syntax

```
lambda arguments: expression
```

- `lambda` — keyword to create the function.
- `arguments` — inputs passed to the function.
- `expression` — the single expression whose result is returned automatically.

Unlike a normal function, a lambda doesn't require an explicit `return`.

## 3. Examples

```py
# Example 1: No arguments
greet = lambda: "Hello Python"
print(greet())

# Example 2: One argument
square = lambda x: x * x
print(square(5))

# Example 3: Two arguments
add = lambda a, b: a + b
print(add(10, 20))

# Example 4: Multiple arguments
calculate = lambda a, b, c: a + b + c
print(calculate(10, 20, 30))

# Example 5: Conditional expression
check_number = lambda n: "Even" if n % 2 == 0 else "Odd"
print(check_number(8))
print(check_number(7))

```

## 4. Lambda vs. normal function

| Feature    | `def` function              | `lambda` function                           |
| ---------- | --------------------------- | ------------------------------------------- |
| Definition | `def` keyword               | `lambda` keyword                            |
| Body       | Multiple statements allowed | One expression                              |
| Return     | Usually explicit `return`   | Automatically returns expression result     |
| Name       | Usually named               | Can be anonymous, or assigned to a variable |
| Best use   | Complex/reusable logic      | Small, simple operations                    |

Best practice: Use `def` for complex logic. Use lambda when a small function makes the code easier to read.

## 5. Why do we use lambda in LangChain?

LangChain's RunnableLambda lets you wrap a Python function so it can be used as a step in a chain.

For example, imagine you want to convert text to uppercase before sending it to a model.

```py

from langchain_core.runnables import RunnableLambda

uppercase = RunnableLambda(lambda text: text.upper())

result = uppercase.invoke("learn langchain")

print(result)

```

Output:

```
LEARN LANGCHAIN
```

---


# Python map and filter function

Both `map()` and `filter()` are Python built-in functions that work with collections such as lists. They are often used with `lambda` functions to process data with less code.


The main difference is:

- `map()` transforms every item.
- `filter()` selects items that satisfy a condition.

## 1. Understanding `map()`

Image you have to square of each item of the list

Without `map()`:

```py
numbers = [1, 2, 3, 4]
def square(x):
    return x * x

output = []
for number in numbers:
    output.append(square(number))

print(output) #[1, 4, 9, 16]
```

With `map()`:

Syntax:

```
map(function, iterable)
```

- `function`: the operation to perform on each item.
- `iterable`: the collection to process, such as a list.
- `list(...)`: converts the result into a list so you can see all the values immediately.


```py
print('with map:', list(map(square, numbers))) #[1, 4, 9, 16]

print('map with lamda', list(map(lambda x: x * x, numbers))) #[1, 4, 9, 16]
```

## 2. Understanding `filter()`

Without `filter()`:

```py
numbers = [1, 2, 3, 4, 5, 6]

even_numbers = []

for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)

print(even_numbers)
```

With `filter()`:


Syntax:

```
filter(function, iterable)
```

- `function`: checks each item and returns a truthy or falsy result.
- `iterable`: the collection to examine.
- `filter()` keeps the original items for which the function returns a truthy value.


```py
numbers = [1, 2, 3, 4, 5, 6]

even_numbers = list(filter(lambda number: number % 2 == 0, numbers))

print(even_numbers)
```

## 4. Combining `filter()` and `map()`

This is particularly useful in data-processing pipelines.

Suppose you have prices and want to double only those greater than ₹1,000.

```py

prices = [500, 1200, 800, 2500, 1500]

result = list(
    map(
        lambda price: price * 2,
        filter(lambda price: price > 1000, prices)
    )
)

print(result)

```

Output:

```
[2400, 5000, 3000]
```
---

# dictionary unpacking (**) with Python's string formatting.

`string.format(**input_dict)` uses dictionary unpacking (**) with Python's string formatting.

It takes the key-value pairs from a dictionary and passes them to format() as named arguments.

```py
template = "My name is {name} and I am {age} years old."

input_dict = {
    "name": "Mohit",
    "age": 34
}

result = template.format(**input_dict)

print(result)
```

`template.format(**input_dict)`

is equivalent to:

`template.format(name="Mohit", age=34)`

---
# `and`, `or`, and `not`

In Python, `and`, `or`, and `not` are logical operators used to combine or reverse conditions.

## 1. `and` operator

Returns `True` only when both conditions are True.

```py
age = 25
has_id = True

print(age >= 18 and has_id)  # True
print(age >= 18 and False)   # False
```

## 2. `or` operator

Returns `True` when at least one condition is True.

```py
age = 16
has_permission = True

print(age >= 18 or has_permission)  # True
print(age >= 18 or False)           # False
```

## 3. `not` operator

Reverses the Boolean value: `True` becomes `False`, and `False` becomes `True`.

```py
is_logged_in = True

print(not is_logged_in)  # False
print(not False)         # True
```

## 4. Practical example

```py
age = 25
is_student = False

if age >= 18 and not is_student:
    print("Eligible")

if age < 18 or is_student:
    print("Special conditions apply")
```

## 5. Important difference: `and` vs `&`

- `and`, `or`, `not` are logical operators.
- `&`, `|`, `~` are bitwise operators and can behave differently, especially with integers and Boolean arrays.
---

# Define types for a variable

## 1. How to define a type for a variable

Python allows you to write type hints using `variable: type = value`.

## 2. How to define types for collections

Collections hold multiple values. The most common ones are lists, dictionaries, tuples, and sets.

## A. List — `list[type]`

- `list[str | int]` → each item can be a string or an integer.
- `list[str]` → list of strings.

```py
prices: list[float] = [10.5, 20.0]

mixed: list[str | int] = ["Mohit", 34, "Delhi"]
```

## B. Dictionary — `dict[key_type, value_type]`

A dictionary stores key-value pairs.

```py
from typing import Any # Any type comes in typing package

user: dict[str, str] = {
    "name": "Mohit",
    "city": "Delhi"
}

data: dict[str, Any] = {
    "name": "Mohit",
    "age": 34,
    "skills": ["Python", "React"],
    "is_developer": True
}
```

## C. Tuple — `tuple[type, ...]`

A tuple is ordered and generally used for a fixed collection of values.

```py
user: tuple[str, int] = ("Mohit", 34)
```

The first item is expected to be a string, and the second an integer.

For a tuple containing any number of integers:

```py
numbers: tuple[int, ...] = (10, 20, 30, 40)
```
## D. Set — `set[type]`

A set stores unique values.

```py
ids: set[int] = {101, 102, 103}

skills: set[str] = {"Python", "React", "Angular"}
```

Duplicate values are automatically removed.

## E. Other important type hints

`Any` — any type
`str | int` — multiple possible types
`str | None` — a value may be missing
`Literal` — only specific values allowed

```py
user_id: str | int = 101
user_id = "USER101"
city: str | None = Nonecity = "Delhi"

from typing import Literal
sentiment: Literal["positive", "negative", "neutral"] = "positive"
```

## 4. How to define types for functions

You can specify both input and return types.

```py
def add(a: int, b: int) -> int:
    return a + b

result: int = add(10, 20)

# For a function returning a dictionary:
def get_user() -> dict[str, str]:
    return {"name": "Mohit", "city": "Delhi"}
```

Here:

- `a: int` → first parameter should be an integer.
- `b: int` → second parameter should be an integer.
- `-> int` → the function is expected to return an integer.

----

# Inheritance

There is no separate `extends` keyword like Java. You specify the parent class name inside parentheses `()` when defining the child class.

## Code Example

Python:

```py
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

```py
I am the parent class
I am the child class
```

## Compare Python vs Java

| Concept                    | Python                 | Java                                   |
| -------------------------- | ---------------------- | -------------------------------------- |
| Inheritance syntax         | `class Child(Parent):` | `class Child extends Parent`           |
| Keyword                    | No `extends` keyword   | Uses `extends`                         |
| Call parent constructor    | `super().__init__()`   | `super()`                              |
| Multiple class inheritance | Supported              | Only one direct superclass for classes |

One important distinction: In `class Child(Parent):`, `Parent` is a base class, not an argument passed to a function. The parentheses specify inheritance.

So remember: Python inheritance = class definition + parent class in parentheses.

# Abstract Class and Abstract Method in Python

An abstract class is a blueprint for other classes. It defines methods that child classes are required to implement.

An abstract method is a method declared in the parent class without a complete implementation that child classes must provide.

In Python, we typically use the `ABC` class and `@abstractmethod` decorator from the built-in `abc` module.

## 1. Simple example

Suppose you're building an application that supports different payment methods: credit cards, UPI, and PayPal.

Each payment method should provide a `pay()` method. An abstract class enforces that requirement.

```py

from abc import ABC, abstractmethod

class Payment(ABC):

    @abstractmethod
    def pay(self, amount):
        pass


class UpiPayment(Payment):
    def pay(self, amount):
        return f"Paid ₹{amount} using UPI"


class CardPayment(Payment):
    def pay(self, amount):
        return f"Paid ₹{amount} using Card"

# Now suppose we have payment list like below
payments = [UpiPayment(), CardPayment()]

# so because of abstract pattern, we can call pay method for each above list item.
for payment in payments:
    print(payment.pay(500))
```

## 2. What happens if we don't implement the abstract method?

Python raises a error while creating object  - 

You cannot instantiate an abstract class while it has unimplemented abstract methods.

----

# Encapsulation

Encapsulation means protecting an object's data by controlling how it can be changed.

Imagine a bank account with a balance of ₹1,000. You should deposit or withdraw money through proper methods rather than changing the balance to any value directly.

## Without encapsulation

```py
class BankAccount:
    def __init__(self, balance):
        self.balance = balance


account = BankAccount(1000)
account.balance = -5000
print(account.balance) 
 # -5000
```

Problem: Anyone can change the balance without validation.

## With encapsulation

```py

class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance


account = BankAccount(1000) # 1000 initial amount
account.deposit(500) # now deposit 500 more
print(account.get_balance())  # 1500

# print(account.__balance) 
# AttributeError: 'BankAccount' object has no attribute '__balance'  

account.deposit(-100) # try with invalid value, (nothing will happen)
print(account.get_balance())  # 1500
```

self.__balance	- Name mangling — Python changes the attribute name to reduce accidental access or clashes

**Easy way to remember: Data + controlled access = Encapsulation.**

---

# @property & @property.setter decorator

`@property` does let you access a method like an attribute. Second it helps to convert instance attribute to a property.

`@property.setter` allow us to validate a property without changing existing interface or code structure.

`@property` controls how you read or update an existing object's attribute.

Note - `@property.setter` requires a property to be defined first. It uses the `property` object's name to attach the setter.

## The bigger real-world benefit: Changing implementation without breaking callers

Imagine you initially expose a simple attribute:

```py
class Product:
    def __init__(self, price):
        self.price = price

product = Product(500)
print(product.price)
```
Later, you need to add validation whenever the price is changed. You could convert price into a property while keeping the same public interface, product.price:

```py
class Product:
    def __init__(self, price):
        self._price = price # _variable just tells that this attribute is only for internal purpose.

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        elif value < 100:
            print('Warning: Minimum deposit is allowed 500.')
        else: 
          self._price = value

product = Product(500) # initial amount
print(product.price)  # 500

product.price = 700   # Validation runs
print(product.price)  #  700

product.price = 80  # Validation runs
# Warning: Minimum deposit is allowed 500.

product.price = -100  # Raises ValueError

```

Existing code that reads or writes `product.price` doesn't need to change. The property adds behavior behind the same interface.

One important detail: in Python, _price is still accessible directly. The validation is guaranteed when assigning through price, not when assigning directly to _price.

----

# `@property.deleter` 

**Purpose:** It lets you control what happens when someone deletes a property using `del`.

Imagine a `Product` class where you have a `price` property. You want to control whether the price can be deleted and what cleanup should happen if it is.

## 1. Without a property deleter

```py
class Product:
    def __init__(self, price):
        self.price = price

product = Product(500)

del product.price  # Deletes the attribute
```

Here, Python deletes the `price` attribute directly. There's no custom cleanup or validation logic.

## 2. With `@price.deleter`

```py
class Product:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        return self._price

    @price.deleter
    def price(self):
        raise AttributeError("Product price cannot be deleted")

product = Product(500)

del product.price  # Raises AttributeError
```

-----

# `@staticmethod` decorator

**Problem it solves:** You have a function related to a class, but it doesn't need to access either the object's data (`self`) or the class's data (`cls`).

Imagine an e-commerce application where you need to validate a product code.

```py
class Product:
    @staticmethod
    def is_valid_code(code):
        return code.startswith("PROD-")

print(Product.is_valid_code("PROD-123"))  # True
print(Product.is_valid_code("ABC-123"))   # False
```

Here, `is_valid_code()` doesn't need a product object or any class-specific data. It only needs the supplied `code`.

Without `@staticmethod`, you could define this as a regular function outside the class. The decorator is useful when you want to logically group this utility with `Product`.

You can also call it through an instance:

```py
product = Product()
print(product.is_valid_code("PROD-123"))
```

## Lets deep more - What Python do automatically when you call a method?

Let's compare three approaches.

### 1. Regular method without `self`

```py
class Product:
    def validate_code(code):
        return code.startswith("PROD-")

# This works when called through the class. But try calling it through an instance:
Product.validate_code("PROD-123")  # Works

# through instance
product = Product()
product.validate_code("PROD-123") #TypeError

# This raises a TypeError because Python automatically passes product as the first argument. The method receives two arguments, but accepts only one.
```

### 2. With `@staticmethod`

```py
class Product:
    @staticmethod
    def validate_code(code):
        return code.startswith("PROD-")

# acess by bdirect class
print(Product.validate_code("PROD-123"))  # True

# access through instance
product = Product()
print(product.validate_code("PROD-123"))  # True
```

So with `@staticmethod` Python does not automatically pass the instance as an argument. The method works when called through either the class or an instance.
 
----

# `@dataclass`

**Purpose:** It saves you from writing repetitive code when a class is mainly used to store data.

Python automatically generates common methods for you, including:

- `__init__()` — initializes the object.
- `__repr__()` — provides a useful string representation.
- `__eq__()` — compares objects by their fields.

Imagine you're creating a `Product` class with a name, price, and quantity.

## 1. Without `@dataclass`

You typically write an `__init__` method to assign all the values.

```py
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

product = Product("Laptop", 50000, 2)

print(product.name)
```

## 2. With `@dataclass`

```py
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int

product = Product("Laptop", 50000, 2)

print(product.name)  # Laptop
print(product)       # Product(name='Laptop', price=50000, quantity=2)
```

# Understand `__repr__() & `__eq__()`

## 1. `__repr__()` — Useful object representation

**Problem:** By default, printing an object doesn't show its actual data in a readable way.

### Without `__repr__()`:

```py
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

product = Product("Laptop", 50000)

print(product)

# Output (similar to): 
#<__main__.Product object at 0x...>

# This tells you the object exists, but not its data.
```

### With `__repr__()`:

```py
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price})"

product = Product("Laptop", 50000)

print(product)
# Product(name='Laptop', price=50000)
```

Real-world use: Easier debugging and inspecting objects in logs or an interactive Python session.

## 2. `__eq__()` — Compare objects by their data

**Problem:** By default, two separate instances of a regular class usually compare as unequal, even when their fields contain identical values.

Without `__eq__()`:

```py
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

p1 = Product("Laptop", 50000)
p2 = Product("Laptop", 50000)

print(p1 == p2)  # False
```

Why? The default comparison checks object identity rather than comparing these fields.

With `__eq__()`:

```py
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price

p1 = Product("Laptop", 50000)
p2 = Product("Laptop", 50000)
p3 = Product("Mobile", 20000)

print(p1 == p2)  # True
print(p1 == p3)  # False
```

Real-world use: Comparing data objects, such as checking whether two API response models or configuration objects contain equivalent values.

---