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
