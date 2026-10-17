# Python: `TypedDict` vs Pydantic

## Contents

- [1. `TypedDict` — define a dictionary's structure](#1-typeddict--define-a-dictionarys-structure)
- [2. `TypedDict` — important options](#2-typeddict--important-options)
  - [`total=False` vs `NotRequired`](#totalfalse-vs-notrequired)
- [Pydantic library](#pydantic-library)
  - [Common `Field()` options](#common-field-options)
- [Abstract Class and Abstract Method in Python](#abstract-class-and-abstract-method-in-python)
  - [1. Simple example](#1-simple-example)
  - [2. What happens if we don't implement the abstract method?](#2-what-happens-if-we-dont-implement-the-abstract-method)

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

### Common `Field()` options

`Field()` lets you add constraints, defaults, descriptions, and other metadata.

| Option                     | Purpose                                 | Example                          |
| -------------------------- | --------------------------------------- | -------------------------------- |
| `default`                  | Provide a default value                 | `Field(default=18)`              |
| `default_factory`          | Generate a default value                | `Field(default_factory=list)`    |
| `gt`, `ge`                 | Greater than / greater than or equal to | `Field(gt=0)`                    |
| `lt`, `le`                 | Less than / less than or equal to       | `Field(le=100)`                  |
| `min_length`, `max_length` | Constrain string or collection length   | `Field(min_length=2)`            |
| `pattern`                  | Match a regular expression              | `Field(pattern=r"^[A-Z]+$")`     |
| `strict`                   | Control type coercion                   | `Field(strict=True)`             |
| `alias`                    | Accept an alternative field name        | `Field(alias="userId")`          |
| `description`, `title`     | Document the field                      | `Field(description="User name")` |

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