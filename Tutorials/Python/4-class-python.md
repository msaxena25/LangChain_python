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

# datetime module

## Current date and time

```py
from datetime import datetime, date, time, timezone

now = datetime.now()

print(now)           # Current date and time
print(date.today())  # Current date only
print(now.year)
print(now.hour)
print(now.minute)

date_object = now.date()
print(date_object)           # Date object: 2026-10-26

# UTC time
utc_now = datetime.now(timezone.utc)
print(utc_now)
print(utc_now.strftime("%Y-%m-%d %H:%M:%S %Z"))
```

## Format date and time into different formats

```py
from datetime import datetime
now = datetime.now()

# strftime() formats a date-time as a string.

print(now.strftime("%d-%m-%Y"))          # 26-10-2026
print(now.strftime("%d/%m/%Y"))          # 26/10/2026
print(now.strftime("%d-%m-%Y %H:%M:%S")) # 26-10-2026 17:30:45
print(now.strftime("%I:%M %p"))          # 05:30 PM
print(now.strftime("%b %d, %Y"))         # Oct 26, 2026
print(now.strftime("%A, %d %B %Y"))      # Monday, 26 October 2026
```

%B - Full month name, %b - Abbreviated month, %A - Full weekday name, %a	- Abbreviated weekday

------------

# Timer(), timer.start(), and time.sleep()

## Timer() and timer.start()

```py
from threading import Timer

def say_hello():
    print("Hello!")

timer = Timer(5, say_hello) # Timer Class with 5 sec delay
timer.start()
```
- `Timer(5, say_hello)` - creates a 5 seconds timer
- `timer.start()` - starts the timer countdown.
- After approximately 5 seconds, Python executes say_hello() in a separate thread.
- By default we provide time in seconds. But you can use `milliseconds` by dividing by 1000.
Think of it like JavaScript's setTimeout(say_hello, 5000).

## time.sleep()

`time.sleep(5)` pauses the current thread. It doesn't schedule a separate thread to run after the delay.

Pauses synchronous execution.

```py
import time

print("Start")
time.sleep(5) #  Wait for 5 min to perform next line (Sleep here)
print("End")
```

## timer.cancel()

`timer.cancel()` only prevents a pending timer from executing; it cannot undo or stop a function that has already run. Same like clearTimeout() in JavaScript.

```py
timer = Timer(5, say_hello)
timer.start()
timer.cancel()
# Here timer will not execute because we have cancelled it before 5 seconds.

timer = Timer(2, say_hello) # 2 seconds of timer
timer.start()
timer.sleep(3) # sleep for 3 seconds
timer.cancel() # after 3 sec, call cancel, while timer have 2 secs so that will execute.

# 'Hello'

```

# Create set interval 

```py
import time

while True:
    print("Running...")
    time.sleep(2)

print("after while")
```

**What happens step by step?**
1. while True: — starts a loop that continues indefinitely because the condition is always True.
2. print("Running...") — prints the message.
3. time.sleep(2) — pauses the current thread for approximately 2 seconds.
4. The loop repeats and prints "Running..." again.
5. print("after while") — never executes because the loop never ends normally.

**How can you execute print("after while")?**

You need to stop the loop using break or another stopping condition.

## How to prevent this and run internal in seperate thread?

Use `threading` — run the task in a separate thread

```py
import threading
import time

def repeat_task():
    while True:
        print("Running...")
        time.sleep(2)

thread = threading.Thread(target=repeat_task, daemon=True) # create seperate thread
thread.start() # start thread

print("Main thread is free!")
```

----

# Threading in Python

`threading` is a built-in Python module that lets you run multiple threads within the same process.

For example:
- Call an API.
- Download a file.
- Run a task repeatedly every few seconds.

Without threading, a blocking operation may hold up the current thread. With threading, you can run certain tasks in separate threads.

## Important methods in Python `threading`

| Method / property            | Purpose                                              |
| ---------------------------- | ---------------------------------------------------- |
| `threading.Thread()`         | Create a thread                                      |
| `thread.start()`             | Start execution in a separate thread                 |
| `thread.join()`              | Wait for a thread to finish                          |
| `thread.is_alive()`          | Check whether a thread is running                    |
| `thread.name`                | Get or set the thread's name                         |
| `thread.daemon`              | Configure whether the thread keeps the process alive |
| `threading.Timer()`          | Execute a function after a delay                     |
| `timer.cancel()`             | Cancel a pending timer                               |
| `threading.Event()`          | Communicate a signal between threads                 |
| `threading.Lock()`           | Protect shared data from concurrent access           |
| `threading.current_thread()` | Get the currently executing thread                   |
| `threading.enumerate()`      | Get the active thread objects                        |

## 4. First example: `Thread()`, `start()` and `join()`

```py
import threading
import time

def task():
    print("Task started")
    time.sleep(2)
    print("Task completed")

thread = threading.Thread(target=task) # create thread

thread.start() # start thread
print("Main thread continues")

thread.join() # Wait for a thread to finish 
print("Main thread finished")
```
----

## Passing more parameters with Thread

```py
import threading
import time

# this function requires username, message and delay
def task(username, message, delay=1):
    time.sleep(delay)
    print(f"{username}: {message}")

thread = threading.Thread(
    target=task,
    name="MyWorker", # Custom name for the thread
    args=("Mohit", "Hello"), # Positional arguments passed to the function
    kwargs={"delay": 2}, # Keyword arguments
    daemon=True
)
```

## Multiple functions inside the same thread

`target` takes one callable. You can pass a wrapper function.

```py
import threading
import time

def task1(): # create first function

def task2(): # create second function

def run_all_tasks(): # comb
    task1()
    task2()

thread = threading.Thread(target=run_all_tasks)
```

**Important distinction:** If you want two functions to run at the same time, create two separate threads.

----

# 1. What is a daemon thread?

A daemon thread is a `background thread` that does not prevent the Python program from exiting when only daemon threads remain.

Example:

```py
thread = threading.Thread(
    target=background_task,
    daemon=True # Does not keep the main program running by itself, Useful for background tasks that can stop at shutdown
)
```

Here, the background task runs repeatedly, but the program can exit when the main thread finishes.

-----

## `threading.Event()`

`threading.Event()` allows one thread to signal another thread to start, wait, continue, or stop working.

### 1. Example: Stop a background thread with set method

```py
import threading
import time

event = threading.Event() # creates a signal that is initially `False`.

# This background thread continues while the signal is `False` or not set.
def background_task():
    while not event.is_set(): # check for signal is set.
        print("Task is running...")
        time.sleep(1)

    print("Task stopped")

thread = threading.Thread(target=background_task)
thread.start()

time.sleep(3)

event.set()  # Signal the thread to stop
thread.join()

print("Main program finished")
```
### 2. Important methods

| Method     | Purpose                            |
| ---------- | ---------------------------------- |
| `Event()`  | Creates an event; initially unset. |
| `set()`    | Sets the signal to `True`.         |
| `clear()`  | Resets the signal to `False`.      |
| `is_set()` | Checks whether the signal is set.  |
| `wait()`   | Waits until the signal is set.     |

### 2. Event wait

Wait until another thread finishes a task.

```py
import threading
import time

event = threading.Event()

def task():
    print("Task started")
    time.sleep(3)  # Simulate some work
    print("Task completed")
    event.set()  # Notify the waiting thread of wait over.

thread = threading.Thread(target=task)
thread.start()

print("Main thread waiting...")
event.wait()  # Wait until event.set() is called

print("Main thread continues")

thread.join()

Task started
Main thread waiting...
Task completed
Main thread continues
```

Use `event.wait()` when you need to wait for a particular signal, such as data becoming available. Use `thread.join()` when you need to wait for a thread to finish.

-----

## Cancel thread

In Python, you `cannot` directly force-stop a running Thread using any built-in cancel() or stop() method. The recommended approach is cooperative cancellation using `threading.Event()`.

```py
stop_event = threading.Event()
print("Requesting cancellation...")
stop_event.set()

# We already have set() method details above.

```

# Thread LOCK

`threading.Lock()` allows only one thread at a time to execute a protected (critical or sensitive) section of code. 
It helps prevent multiple threads from modifying shared data or sensitive data simultaneously.

"**Create lock -**: lock = threading.Lock()

## What is a race condition?

A `race condition` happens when two or more threads (or processes) try to change shared data at the same time. Because their actions overlap, the result can be `unpredictable` or wrong.

For example, if two threads withdraw from a bank account at the same time, they might both see enough money and let both withdrawals happen, even though there isn't enough balance.

`Thread Lock` solve this race condition problem.

**Example where lock is used -**

Let's understand the use of thread locks with a banking transaction example:

1. Suppose an account has a balance of ₹1000.

2. Two withdrawal transactions are attempted simultaneously:
   - First transaction: withdraw ₹500
   - Second transaction: withdraw ₹700

3. According to banking rules, after withdrawing ₹500, the balance should be ₹500. The next attempt to withdraw ₹700 should be denied due to insufficient funds.

4. **Without using a LOCK:**
   - Both transactions may run at the same time.
   - This can lead to both transactions being approved, resulting in an incorrect final balance of ₹-200.

5. **With a LOCK in place:**
   - The first transaction `acquires the lock` and processes the withdrawal.
   - While the lock is held, any other transaction (like the second withdrawal) must wait.
   - After the first transaction completes and` releases the loc`k, the second transaction checks the updated balance and is denied due to insufficient funds.
   - The correct final balance is ₹500, and the system maintains data integrity.

In summary:
- **LOCK** ensures that shared data (account balance) is `accessed/modified by only one thread at a time`, preventing race conditions and inconsistent states.

```py
lock = threading.Lock() # first create lock object

# define function to check and deduct balance
def withdraw_with_lock(amount: int, transaction_name: str):
  with lock:
    # transaction code..
```