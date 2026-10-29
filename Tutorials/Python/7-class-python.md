## Contents

- [1. `TypedDict` — define a dictionary's structure](#1-typeddict--define-a-dictionarys-structure)
- [2. `TypedDict` — important options](#2-typeddict--important-options)
  - [`total=False` vs `NotRequired`](#totalfalse-vs-notrequired)
- [Pydantic library](#pydantic-library)
  - [Common `Field()` options](#common-field-options)

# `TypedDict` and `Pydantic`

Both `TypedDict` and `Pydantic` help you define the expected structure of data in Python, but they serve different purposes.

- `TypedDict` defines the expected dictionary structure for static type checking.
- `Pydantic` defines data models and validates data at runtime.

## 1. `TypedDict` — define a dictionary's structure

- Tells type checkers which keys a dictionary should contain and what types their values should have.
- It is used for static type checking.
- It does not automatically validate the dictionary at runtime.

```py

from typing import TypedDict, NotRequired, Literal

class User(TypedDict):
    name: Annotated[str, "Developer's name"]
    age: int | None    # Key required; value may be None
    email: NotRequired[str]   # Key may be omitted
    nickname: NotRequired[str]   # Key may be omitted
    role: Literal["admin", "user"],
    user_id: Required[int] # user_id must be present.

user: User = {
    "name": "Mohit",
    "age": 34,
    "role": "admin",
    "user_id": 111123
}

print(user["name"])
print(user["age"])

# Output:
# Mohit
# 34

```

If you put `"age": "34"` or omit `name`, Python itself will not automatically reject the dictionary. A static type checker can report these issues.


## 2. `TypedDict` — important options

| Option              | Purpose                                                | Example                              |
| ------------------- | ------------------------------------------------------ | ------------------------------------ |
| `TypedDict`         | Define dictionary structure                            | `class User(TypedDict)`              |
| `Required[T]`       | Key must be present                                    | `Required[int]`                      |
| `NotRequired[T]`    | Key may be omitted                                     | `NotRequired[str]`                   |
| `total=False`       | All keys defined in that class are optional by default | `class User(TypedDict, total=False)` |
| `Optional[T]`       | Value can be `None`                                    | `Optional[str]`                      |
| `T \\| None`        | Modern syntax for allowing `None`                      | `str \\| None`                       |
| `Literal[...]`      | Restrict values to specific literals                   | `Literal["admin", "user"]`           |
| `list[T]`           | List containing values of type `T`                     | `list[str]`                          |
| `dict[K, V]`        | Dictionary with key and value types                    | `dict[str, int]`                     |
| `Annotated[T, ...]` | Attach metadata to a type                              | `Annotated[int, "age"]`              |
| `ReadOnly[T]`       | Mark a key as read-only for type checkers              | `ReadOnly[str]`                      |

### `total=False` vs `NotRequired`

Use `total=False` for partial-update dictionaries. Use `NotRequired` when only a few fields may be omitted.

```py
from typing import TypedDict, Required

class UserUpdate(TypedDict, total=False):
    name: str
    age: int
    user_id: Required[int]

# name and age can be omitted.
# user_id must be present.
update: UserUpdate = {"user_id": 101}
```


# Pydantic library

Install Pydantic in your virtual environment:

```
# Run this in your terminal, not inside Python:
# pip install pydantic
```

Pydantic models use type annotations to parse and validate input data. The examples below use Pydantic V2, the modern API.

```py
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

user = User(name="Mohit", age="34")

# Pydantic normally converts compatible values, such as `"34"` to `34`. This is called coercion. You can enable strict validation when conversion should not be allowed.

print(user.name)
print(user.age)
print(type(user.age))

# Output:
# Mohit
# 34
# <class 'int'>

# Invalid input raises ValidationError:
try:
    User(name="Mohit", age="abc")
except ValidationError as error:
    print(error)

```

### `Field()` options

```py

from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0, default=1)
    sku: str = Field(pattern=r"^[A-Z0-9]+$"),
    tags: list[str] = Field(default_factory=list)

product = Product(
    name="Laptop",
    price=75000,
    sku="LAP123"
)
product.tags.append("Electronics")


print(product.model_dump())

# Output:
# {'name': 'Laptop', 'price': 75000.0,
#  'quantity': 1, 'sku': 'LAP123'}
```
----

# SQLite3 in Python: Basic Database Operations

Python provides a built-in package called `sqlite3` to work with SQLite databases. You do not need to install it using pip.

## Connect to a database

```py
import sqlite3
conn = sqlite3.connect("mobile_store.db") # create db of fetch existing
cursor = conn.cursor() #cursor is an object used to execute SQL queries and retrieve their results.
```

## Create a table

Let's create a `products` table.

```py
create_table_query = '''
        CREATE TABLE IF NOT EXISTS products 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_description TEXT NOT NULL,
            product_price REAL NOT NULL,
            in_stock INTEGER NOT NULL
        )
'''
# REAL - Stores decimal numbers 

# Create the table if it doesn't exist
cursor.execute(create_table_query)
conn.commit() # Commit changes to db
```

## Insert data into a table

```py
# Product Data
products = [
    ("iPhone 15", "The latest iPhone model", 1000, 100),
    ("Samsung Galaxy S23", "The latest Samsung Galaxy model", 900, 100),
]

# Insert products into the table
insert_products_query = '''
INSERT INTO products (product_name, product_description, product_price, in_stock)
VALUES (?, ?, ?, ?)
'''
#Execute the insert_products_query for each product in the products list
cursor.executemany(insert_products_query, products)

# execute  = for single record
# executemany = multiple records
# The `?` placeholders are filled with the supplied values in order.
```

## Read or fetch data from a table

Use `SELECT` to retrieve data.

### Fetch all records

```py
cursor.execute("SELECT * FROM products")
rows = cursor.fetchall() # fetch all rows
for row in rows:    
    print(row)

# cursor.fetchone() = fetch one record
cursor.execute("SELECT * FROM products WHERE id = ?", (1,))
row = cursor.fetchone()
print(row)
```

## Update

```py
cursor.execute("UPDATE products SET price = ?, in_stock = ? WHERE id = ?", (74900, 1, 1))
conn.commit()
```

## Delete the complete database

SQLite does not provide a SQL command such as `DROP DATABASE` for deleting a database file.

Instead, close the connection and remove the database file using Python's `os` module.

```py

conn.close()
if os.path.exists(db_path):    
    os.remove(db_path)
```

------------

# NumPy - Python library

NumPy is a Python library used for working efficiently with numerical data, arrays, and mathematical operations.

```py
python -m pip install numpy

# use 
import numpy as np
```

NumPy provides `an array` instead of using a regular Python list for numerical operations.

```py
# Python list
numbers_list = [10, 20, 30, 40]

# NumPy array
import numpy as np
numbers_array = np.array([10, 20, 30, 40])

python_list = numbers_array.tolist() # Use .tolist() to convert a NumPy array into a Python list.
```

## One example: Multiply each number by 2

```py
# Python list
numbers = [10, 20, 30]
print(numbers * 2) # [10, 20, 30, 10, 20, 30] (The list is repeated twice.)

# numpy array
import numpy as np
numbers = np.array([10, 20, 30])
print(numbers * 2) # [20 40 60] (Each element is multiplied by 2.)

print(type(numbers)) # <class 'numpy.ndarray'>
```

## Useful operations

`arr = [1, 2, 3, 4, 5]`

First, convert the Python list into a NumPy array.

```py
import numpy as np
arr = [1, 2, 3, 4, 5]
np_arr = np.array(arr)
```

## 1. Basic properties

| Property             | Example         | Output               |
| -------------------- | --------------- | -------------------- |
| Data type            | `np_arr.dtype`  | `int64` (may vary)   |
| Number of dimensions | `np_arr.ndim`   | `1`                  |
| Array shape          | `np_arr.shape`  | `(5,)`               |
| Total elements       | `np_arr.size`   | `5`                  |
| Total bytes          | `np_arr.nbytes` | Depends on data type |

## 2. Mathematical operations

| Method / Function  | Example             | Output                                   |
| ------------------ | ------------------- | ---------------------------------------- |
| Sum                | `np.sum(np_arr)`    | `15`                                     |
| Mean (average)     | `np.mean(np_arr)`   | `3.0`                                    |
| Minimum            | `np.min(np_arr)`    | `1`                                      |
| Maximum            | `np.max(np_arr)`    | `5`                                      |
| Standard deviation | `np.std(np_arr)`    | `1.414...`                               |
| Variance           | `np.var(np_arr)`    | `2.0`                                    |
| Product            | `np.prod(np_arr)`   | `120`                                    |
| Cumulative sum     | `np.cumsum(np_arr)` | `[1, 3, 6, 10, 15]`                      |
| Square root        | `np.sqrt(np_arr)`   | `[1., 1.414..., 1.732..., 2., 2.236...]` |
| Sort               | `np.sort(np_arr)`   | `[1, 2, 3, 4, 5]`                        |

## 3. Indexing and filtering

```py
print(np_arr[0])             # 1
print(np_arr[-1])            # 5
print(np_arr[1:4])           # [2 3 4]

# Filtering 

print(np_arr[np_arr > 3])    # [4 5]
print(np.where(np_arr > 3))  # (array([3, 4]),)
```

## 4. Array modification and transformation

```py
print(np_arr * 2)                 # [ 2  4  6  8 10]
print(np_arr + 10)                # [11 12 13 14 15]

print(np_arr.reshape(5, 1))       # 5 rows, 1 column
print(np_arr.astype(float))       # Convert elements to float
print(np.unique([1, 2, 2, 3, 3])) # [1 2 3]
```

Note that arithmetic operations on NumPy arrays usually work element by element, unlike Python lists.


## 5. shape property

```py
import numpy as np
arr = np.array([1, 2, 3, 4, 5])
print(arr.shape) # (5,)

# The comma indicates that the shape is a tuple with one value. This is a 1D array of 5 elements.

arr = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(arr.shape) # (2,3)   => (row, column)
```

---------------