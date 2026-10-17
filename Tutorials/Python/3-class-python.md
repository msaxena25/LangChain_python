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

### Quick revision

| Function / method | Purpose                                                |
| ----------------- | ------------------------------------------------------ |
| `print()`         | Display output                                         |
| `input()`         | Accept user input as a string                          |
| `int()`           | Convert to an integer                                  |
| `float()`         | Convert to a decimal number                            |
| `str()`           | Convert to a string                                    |
| `.split()`        | Split a string into parts                              |
| `sep`             | Set the separator between printed values               |
| `end`             | Set what gets printed at the end; default is a newline |
| `f"..."`          | Insert variables or expressions into a string          |

Important: `input()` returns a string, so convert it before performing numeric calculations. For example, `int(input())` for whole numbers and `float(input())` for decimal numbers. Invalid numeric input raises a `ValueError`.

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