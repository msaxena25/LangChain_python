# Read file with open() function

file  = open("requirements.txt", "r")
content = file.read()
file.close()
print('Read whole file as a string', content)

# Read 10 characters from the file

file = open("requirements.txt", "r")
content = file.read(10)
file.close()
print('Read 10 characters from the file:', content)

# Lets try read method 2 times to see the difference

file = open("requirements.txt", "r")
content = file.read()
content1 = file.read()
print('content', content) # content langchain
print('content 1 ', content1)  # content 1 

'''
One important detail: after reading a file to its end, calling `read()` again on the same file object normally returns an empty string (`""`). You must reopen the file or reposition the file pointer using `seek()` to read it again.
'''

# Another example of 2 reads.

file = open("requirements.txt", "r")
content3 = file.readline()
content4 = file.read()
print('content 3', content3) # content langchain
print('content 4', content4) # content langchain-openai python-dotenv

# Try read again after close file

file = open("requirements.txt", "r")
content = file.read()
file.close()
# content2 = file.read() # ValueError: I/O operation on closed file.

# use of with (no need to call close method)

with open("requirements.txt", 'r') as file:
    content = file.read()
    print('use with ', content)
    
with open("requirements.txt", 'r') as file:
    content = file.readlines()
    print('use with and read lines ', content)
    # use with and read lines  ['langchain\n', 'langchain-openai\n', 'python-dotenv']
    
# now try to read md file

with open("README.md", 'r') as file:
    print('read readme file', file.read())
    
# now try to read pdf file (You cannot directly read pdf file like text files)

'''
with open("test-pdf.pdf", 'r') as file:
    print('read file ', file.readline())
    UnicodeDecodeError: 'charmap' codec can't decode byte 0x8d in position 741: character maps # to <undefined>
'''

print("read test-pdf.pdf with rb mode..")

# The PDF example uses "rb" — read binary mode. This reads raw bytes, not extracted PDF text.

with open("test-pdf.pdf", 'rb') as file:
    print(file.readline()) # b'%PDF-1.7\r\n'

# Now read pdf file with pypdf library
'''
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

'''

# Read JSON

print('reading  json file..')

import json

with open('test-json.json', 'r', encoding='utf-8') as file:
    content = json.load(file)
    print(content)
    
# json.loads() method

print('json.loads() method..')

# json.loads() reads JSON from a string, not JSON object.

'''
    with open('test-json.json', 'r', encoding='utf-8') as file:
    content = json.loads(file) # TypeError: the JSON object must be str, bytes or bytearray, not TextIOWrapper
    print(content)
   
'''

# json.loads() method with json string

json_string =  '{"name": "Mohit", "age": 34}' 
data  = json.loads(json_string)
print(data)

# handle json errors

print('handling json error with try & except..')

try:
    with open('test-json.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        print(data)
except json.JSONDecodeError as error:
    print('Invalid JSON', error)
except FileNotFoundError:
    print('File not found')
    
# update files
    
with open("notes.txt", "w", encoding="utf-8") as file:
    file.write("Hello Python\n")
    file.write("Learning AI\n") 