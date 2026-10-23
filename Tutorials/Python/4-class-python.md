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