# List Comprehension

List comprehension is a short way to create a new list by iterating over an existing collection, transforming its items, or filtering them using conditions.

Instead of writing multiple lines with a for loop and append(), you can often write the same logic in one line.

**Syntex:**

```py
new_list = [expression for item in iterable]

[new_value for item in collection if condition]
```

## Examples

```py
numbers = [1, 2, 3, 4, 5]

squares = [number ** 2 for number in numbers]

even_numbers = [ number for number in numbers if number % 2 == 0]

```

## Transformation and filtering together

```py
employees = [
    {"name": "Amit", "salary": 60000},
    {"name": "Neha", "salary": 90000},
    {"name": "Rahul", "salary": 75000},
    {"name": "Priya", "salary": 100000},
    {"name": "Karan", "salary": 50000}
]

updated_salaries = [
    {
        "name": employee["name"],
        "salary": employee["salary"] * 1.10
    }
    for employee in employees
    if employee["salary"] < 80000
]

print(updated_salaries)

[
    {'name': 'Amit', 'salary': 66000.0},
    {'name': 'Rahul', 'salary': 82500.0},
    {'name': 'Karan', 'salary': 55000.0}
]
```

## if and not in

```py
embeddings_ids = ["doc1", "doc3"]

new_ids = [
    doc.id
    for doc in documents
    if doc.id not in embeddings_ids
]

print(new_ids)
```

## Nested list comprehension

```py
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

flattened = [
    number
    for row in matrix
    for number in row
]

# Single line expression - 
# flattened = [ number for row in matrix for number in row ]

print(flattened)
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

----------

# try, except Error handling

**What does each block do?**

- try — contains the code that might fail.
- except — handles a matching exception.
- else — runs only if the try block completes without an exception.
- finally — runs whether an exception occurred or not, making it useful for cleanup.

**Required props**

| Block     | Required or optional?                            |
| --------- | ------------------------------------------------ |
| `try`     | Required                                         |
| `except`  | At least one `except` or a `finally` is required |
| `else`    | Optional                                         |
| `finally` | Optional                                         |

## Valid combinations:

```py
try:
    risky_operation()
except ValueError:
    handle_error()

try:
    risky_operation()
finally:
    cleanup()

try:
    risky_operation()
except ValueError:
    handle_error()
else:
    handle_success()
finally:
    cleanup()

# Invalid - This raises a `SyntaxError`.
# Python requires a `try` statement to have at least one `except` or a `finally` block.
try:
    print("Hello")
else:
    print("Success")
```
## Examples of common exceptions:

- ZeroDivisionError — dividing by zero.
- TypeError — using incompatible types.
- ValueError — a value has the wrong format.
- FileNotFoundError — trying to open a missing file.
- KeyError — accessing a missing dictionary key.

----------

# Slicing with [:] and [::]

In Python, `[:] and [::] `are forms of slicing. Slicing lets you extract elements from a string, list, tuple, or other sequence.

Syntex: sequence[start:stop:step]

- start — index where slicing begins (included).
- stop — index where slicing ends (excluded).
- step — how many positions to move each time.

## examples

```py
my_list = [1, 2, 3, 4, 5]

print(my_list[1:3]) # [2, 3]
print(my_list[::2]) # [1, 3, 5]
print(my_list[1:3:2]) # [2]
```

## understand reverse (step will be in negative)

```py
my_list = [1, 2, 3, 4, 5]
print(my_list[::-1]) # [5, 4, 3, 2, 1] - reverse the list
```

- Start: omitted → starts from the last element.
- Stop: omitted → continues to the beginning.
- Step: -1 → moves backward one position.

```py
print(my_list[-1:-6:-1]) # [5, 4, 3, 2, 1] - reverse the list

print(my_list[::-2])  # [5, 3, 1]

print(my_list[-2::]) # [4, 5]

print(my_list[1::-1]) # [2, 1]

print(my_list[1:1:-1]) # [] - empty list because stop is 1 and start is 1, so no elements to reverse
```

# Palindrome program

```py
word  = 'MADAM'
revese_word = word[::-1]
print('Palindrome' if word == revese_word else 'Not a Palindrome')
```

# Factorial program

## with recursion

```py
def factorial(n):
    if (n < 0):
        return 'Factorial is not defined for negative numbers'
    elif (n == 0):
        return 1
    else:
        return n * factorial(n-1)

number: str = input('Enter a positive number: ')
print(factorial(int(number)))
```
# without recursion

```py
def factorial(n):
    if (n < 0):
        return 'Factorial is not defined for negative numbers'
    elif (n == 0):
        return 1
    else:
        result = 1
        # In range(1, n + 1), n + 1 is used because Python excludes the stop value.
        for i in range(1, n + 1):
            result *= i
        return result

number: str = input('Enter a positive number: ')
print('factorial with range loop:', factorial(int(number)))
```

---

# Magic Methods in python

Magic methods are special methods whose `names start and end with double underscores`, like `__init__()`.

Because of the double underscores, they are also called `dunder methods` (short for "double underscore").

**Purpose**- They allow your objects to `work with Python's built-in operations`, such as printing, addition, comparison, length and object creation etc.

There are numbers of magic methods in Python like `__add__()`, `__str__()`, `__init__()`, `__del__()`, `__contains__()`,` __mul__()`,` __gt__()` etc..

## `__add__()`

```py
class Number:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value


a = Number(10)
b = Number(20)

print(a + b) # 30
# Here, a + b triggers a.__add__(b).
```
## `__len__()`  

```py
class Company:
  def __init__(self, employees):
    self.employees = employees

  def __len__(self):
    return len(self.employees)

c1 = Company(["Emil", "Tobias", "Linus"])

print(len(c1)) # 3
```

**Note:** Without __len__(), calling len(c1) would raise a TypeError, since Python would not know what "length" means for a Company.

-----