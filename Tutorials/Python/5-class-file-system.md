**Python Learning: File System**

## Python provides built-in functionality to interact with this file system.

- Text files (`.txt`) — read ordinary text.
- PDF files (`.pdf`) — read document content using a `PDF library`.
- JSON files (`.json`) — read structured data.
- CSV files (`.csv`) — read tabular data.

## Read a text file using `open()`

```py
file = open("notes.txt", "r")
content = file.read()
print(content)
file.close()
```

Understand each part:

- `"notes.txt"` — the file path.
- `"r"` — opens the file in read mode.
- `file.read()` — reads all remaining content and returns it as a string.
- `file.close()` — closes the file and releases its resources.

## Recommended way: Use `with open()`

In real projects, we usually use `with open()` instead of manually calling `close()`.

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
```
**Why is this better?**

Python automatically closes the file when the `with` block finishes, even if an exception occurs inside it.

- `with` — manages the file's lifetime.
- `as file` — stores the file object in the variable `file`.
- `encoding="utf-8"` — specifies how text should be decoded.

# Different methods to read a text file

### Method 1 — `read()`

Use this when you need the entire file as one string.

You can also specify the number of characters to read:

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read(10) #define number of chars to read

print(content)
```

### Method 2 — `readline()`: Read one line at a time

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    first_line = file.readline()
    second_line = file.readline()

print(first_line)
print(second_line)
```

Each call reads the next line. The returned line normally includes its newline character (`\n`) when one is present.

### Method 3 — `readlines()`: Read all lines into a list

Use this when you need all lines stored in memory and want to access them later.

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

print(lines)

[
    "Python is a programming language.\n",
    "We are learning file handling.\n",
    "It is useful for AI and LangChain."
]

```

### Method 4 — Iterate directly over the file

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```
Here, `strip()` removes leading and trailing whitespace, including the newline at the end of each line.


This is generally the preferred approach for processing large text files because Python reads the file line by line instead of loading everything into memory.

One important detail: after reading a file to its end, calling `read()` again on the same file object normally returns an empty string (`""`). You must reopen the file or reposition the file pointer using `seek()` to read it again.

----

# Understand File Pointer  

## Example of two read method

```py
file = open("requirements.txt", "r")
content = file.read()
content1 = file.read() # this will print empty
print('content', content) # content langchain
print('content 1 ', content1)  # content 1 
```

In above example, when second time read() method called, You get empty data.

## Example of one readLine and then read

```py
file = open("requirements.txt", "r")
content3 = file.readline()
content4 = file.read()
print('content 3', content3) # content langchain
print('content 4', content4) # content langchain-openai python-dotenv
```

In avove example, first time we called readline method and second time read method, so here you get some data in second read method as well.

The important concept here is the `file pointer`. Think of a file pointer as a cursor that tracks your current reading position in the file.

**Second example steps -**

- The pointer is at the beginning of the file.
- The first line has been consumed. The pointer moves to the next line.
- read() consumes all remaining content, starting from the current pointer position.

**While in first example -**

- First method is read so the pointer is already at the end of the file.

---------

# `seek()` method 

The seek() method is used to move the file pointer to a specific position in a file. This lets you reread content or start reading from a particular position.

```py
with open("requirements.txt", "r") as file:
    print(file.readline())  # langchain
    file.seek(0)            # Move to the beginning
    print(file.read())      # Read the entire file again
```
seek(0) moves the pointer back to position 0, the beginning of the file.

seek(n) moves the pointer to position n.

-----

# Read PDF

A PDF is different from a plain text file. Although both are files on your computer, a PDF has its own document format.

For PDF text extraction, you can use the **`pypdf`** library.

Install it first:

```py
pip install pypdf
```

Suppose you have an existing file called `report.pdf`.

```py
from pypdf import PdfReader

reader = PdfReader("report.pdf")

for page in reader.pages:
    text = page.extract_text()
    print(text)
```

This extracts text from each page and prints it.

Important points:

- `PdfReader()` opens the PDF for reading.
- `reader.pages` provides access to its pages.
- `page.extract_text()` extracts text where available.
- Scanned PDFs containing only images may require OCR (optical character recognition). Text extraction alone might not work.

--------

# PDF Read

## PDF read with open method and rb mode (read binary mode)

The PDF example uses "rb" — read binary mode. This reads raw bytes, not extracted PDF text.

For extracting readable PDF content, we need to use pypdf library.

```py
with open("test-pdf.pdf", 'rb') as file:
    print(file.readline()) 
    # b'%PDF-1.7\r\n'
```

## pypdf lib

```py

print("read pdf file with pypdf lib..")

from pypdf import PdfReader

reader = PdfReader("test-pdf.pdf")

for page in reader.pages:
    text = page.extract_text()
    print(text)

# Number of pages
print("Pages:", len(reader.pages))
# Document metadata
print("Metadata:", reader.metadata)

# Extract text from the first page
if len(reader.pages) > 0:
    print('read first page', reader.pages[0].extract_text())

reader.close()
```
----

# Read JSON file

Python provides a built-in `json` module, so you don't need to install any additional library.

## 1. Example JSON file

Suppose you have a file named `user.json` containing:

```py
{
    "name": "Mohit",
    "age": 34,
    "skills": ["Python", "React", "LangChain"],
    "is_learning": true
}
```

## 2. Read JSON using `json.load()`

Use `json.load()` to read JSON data directly from an open file.

```py
import json

with open("user.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(data)
print(data["name"]) # Access the JSON data
print(data["age"])
print(data["skills"])

print(type(data)) # <class 'dict'>
```


## 3. Difference between `json.load()` and `json.loads()`

This is an important distinction.

`json.load()` reads JSON from a file object.

```py
with open("user.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

`json.loads()` reads JSON from a string.

```py
import json

json_string = '{"name": "Mohit", "age": 34}'

data = json.loads(json_string)
print(data["name"])
# Mohit
```

# Handle JSON file Errors

Incase of Invalid JSON - Python raises `json.JSONDecodeError`

```py
import json

try:
    with open("user.json", "r", encoding="utf-8") as file:
        data = json.load(file)

except json.JSONDecodeError as error:
    print("Invalid JSON:", error)

except FileNotFoundError:
    print("File does not exist.")
```

-----

# Update txt File

Let's understand how to `update an existing text file` in Python. There are three common operations:

1. Overwrite — replace the existing content.
2. Append — add new content at the end.
3. Modify specific content — replace or update particular text inside the file.

## 1. Overwrite the file using `"w"`

The `"w"` mode overwrites the existing content. If the file doesn't exist, Python creates it.

```py
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Hello Python\n")
    file.write("Learning AI\n")
```
Important: write() does not add a newline automatically. So To place the text on separate lines, include \n.

Important: The previous content is removed as soon as the file is opened in write mode. Use `"w"` carefully.


## 2. Append content using `"a"`

The `"a"` mode adds content to the end of the file without removing existing content.

```py
with open("notes.txt", "a", encoding="utf-8") as file:
    file.write("Learning LangChain\n")
```


## 3. Replace specific text in a file

```py
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()

# replace what you want
content = content.replace("Learning AI", "Learning Python")

# then again overwrite same file with replaced content
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write(content)
``` 

----

# Create Files

## Create a text file (`.txt`)

You can use the built-in `open()` function with write mode (`"w"`).

```py
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Learning Python file handling.\n")
    file.write("Next, I will learn LangChain.")
```

- If `notes.txt` doesn't exist, Python creates it.
- If it already exists, `"w"` overwrites its existing content.
- `with` automatically closes the file.

## Create a CSV file (`.csv`)

Python provides **a built-in `csv` module**.

```py
import csv

with open("employees.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["Name", "Department", "Salary"])
    writer.writerow(["Amit", "Engineering", 80000])
    writer.writerow(["Priya", "HR", 60000])
```

The resulting file contains:

```
Name,Department,Salary
Amit,Engineering,80000
Priya,HR,60000
```

## Create a PDF file (`.pdf`)

Unlike text and CSV files, `PDFs have a structured binary format`. You generally use a library to create them.

One option is `fpdf2`.

First, install it in your terminal:

```py
python -m pip install fpdf2
```

Then create the PDF:

```py
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=16)

pdf.cell(0, 10, text="Learning Python File Handling")
pdf.ln(10)
pdf.set_font("Helvetica", size=12)
pdf.multi_cell(0, 10, text="This is my first PDF created using Python.")

pdf.output("notes.pdf")
```
**Note** - pypdf can be used to create PDF files, but its main purpose is reading, manipulating, merging, splitting, and extracting content from existing PDFs.
-------------

# What is pathlib?

`pathlib` is a built-in Python module that provides an object-oriented way to work with file and directory paths.

## Check files 

```py

from pathlib import Path

file_path = Path('test-document/time-table.md')
#file_path = Path('test.txt')

print(file_path.name) # time-table.md
print(file_path.parent)  # test-document
print(file_path.suffix)  # .md
print(file_path.exists())
print(file_path.is_file())
print(file_path.is_dir())
print(file_path.is_absolute())
print(Path.cwd()) #C:\Users\mohitsaxena\MY WORK BLOCK\LEARNING\LangChain_python # current working directory
```

## Create file and dir

```py
# create a folder
folder = Path("data/reports")
folder.mkdir(parents=True, exist_ok=True)

parents=True creates missing parent directories.
exist_ok=True avoids an error if the directory already exists.

# create a file
file = folder / "report.txt"
file.touch() # method is used to create a file
print(file.exists())
```
##  Read and write a file

`pathlib` provides convenient methods so you don't always need `open()` for simple text-file operations.

Important: write_text() overwrites existing content. Also, the parent directory must already exist.

```py
file_path = Path("test-document/sample-text.txt")
file_path.write_text("Learning pathlib", encoding="utf-8")
content = file_path.read_text(encoding="utf-8")
print(content)
```

## resolve method

resolve() returns an absolute path.

```py
relative_path = Path("test-document/sample-text.txt")
absolute_path = relative_path.resolve()
print(absolute_path)
# resolve: C:\Users\mohitsaxena\MY WORK BLOCK\LEARNING\LangChain_python\test-document\sample-text.txt
```

## glob and rglob methods

**glob - Find all files in a folder**

```py
data_folder = Path("test-document") # folder
print('total files', len(list(data_folder.glob("*"))))

for file_path in data_folder.glob("*"):
    print(file_path.name)

# for txt files only - data_folder.glob("*.txt")
```


**rglob - Find all files in a folder & its nested folder as well**

```py
data_folder = Path("test-document") # folder
for file_path in data_folder.rglob("*.pdf"):
    print(file_path)
```

--------------