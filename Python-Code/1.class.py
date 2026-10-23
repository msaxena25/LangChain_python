"""

# map function

# First lets do below operation without map function

numbers = [1, 2, 3, 4]

# print square of each item of above list

def square(x):
    return x * x

output = []

for number in numbers:
    output.append(square(number))

print(output)

# Use of map

print('with map:', list(map(square, numbers)))

# Use of map with lamda
squareFn = lambda x: x * x

print(map(squareFn, numbers)) #<map object at 0x000001883DFF4610>
print(list(map(squareFn, numbers))) #[1, 4, 9, 16]

# in single line
print('map with lamda', list(map(lambda x: x * x, numbers))) #[1, 4, 9, 16]



#-------------------------------

# pathlib

from pathlib import Path

file_path = Path('test-document/time-table.md')
#file_path = Path('test.txt')
print(file_path.exists())
print(file_path.is_file())
print(file_path.is_dir())
print(file_path.is_absolute())

# create a folder
folder = Path("data/reports")
folder.mkdir(parents=True, exist_ok=True)

# create a file
file = folder / "report.txt"
file.touch() # method is used to create a file
print(file.exists())

# write and read a file

file_path = Path("test-document/sample-text.txt")
file_path.write_text("Learning pathlib", encoding="utf-8")
content = file_path.read_text(encoding="utf-8")
print(content)

print(file_path.name)    # notes.txt
print(file_path.stem)    # notes
print(file_path.suffix)  # .txt
print(file_path.parent)  # data
print(Path.cwd()) #current working directory

print('resolve:', file_path.resolve())

print('find all files in test-document folder:')
data_folder = Path("test-document")
print('total files', len(list(data_folder.glob("*"))))
for file_path in data_folder.glob("*"):
    print(file_path.name)



#---------------------------------------------------

# Slicing with [:] and [::]

# In Python, [:] and [::] are forms of slicing. Slicing lets you extract elements from a string, list, tuple, or other sequence.

# Example of slicing

my_list = [1, 2, 3, 4, 5]
print(my_list[1:3]) # [2, 3]
print(my_list[::2]) # [1, 3, 5]

# Example of slicing with step

my_list = [1, 2, 3, 4, 5]
print(my_list[1:3:2]) # [2]
print(my_list[::-1]) # [5, 4, 3, 2, 1] - reverse the list

# can we write full syntex for reverse the list?
print(my_list[-1:-6:-1]) # [5, 4, 3, 2, 1] - reverse the list

print(my_list[::-2]) # [5, 3, 1]

print(my_list[-2::]) # [4, 5]

print(my_list[1::-1]) # [2, 1]
print(my_list[1:1:-1]) # [] - empty list because stop is 1 and start is 1, so no elements to reverse

# Palindrome program

word  = 'MADAM'
revese_word = word[::-1]
print('Palindrome' if word == revese_word else 'Not a Palindrome')

# Factorial program

## with recursion

def factorial(n):
    if (n < 0):
        return 'Factorial is not defined for negative numbers'
    elif (n == 0):
        return 1
    else:
        return n * factorial(n-1)

number: str = input('Enter a positive number: ')
print(factorial(int(number)))

# without recursion

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

"""

#-----------------------------

# Positional argument and Keyword argument

def show_details(name, *args, **kwargs):
    print("Name:", name)
    print("Extra values:", args)
    print("Named values:", kwargs)

show_details("Mohit", 10, 20, city="Noida", role="Engineer")


# show_details("Mohit", city="Noida", role="Engineer", 10, 20)
# SyntaxError: positional argument follows keyword argument

def display_job(job, age):
    print('I am in my', job, 'age is', age)

display_job('Engineer', 34) # Positional argument
# display_job(job='Engineer', 34) # SyntaxError: positional argument follows keyword argument
display_job(job='Engineer', age=34) # Keyword argument
display_job(age=34, job='Engineer') # Keyword argument


from array import array

numbers = array('i', [1, 2, 3, 4, 5])