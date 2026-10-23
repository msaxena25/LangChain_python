import langchain

# Test langchain version
print(langchain.__version__)

# f-string need variable upfront to format string.
# f-strings evaluate variables immediately; they don't remain dynamic templates automatically.
topic="angular"
level="junior"
str1 = f"Explain {topic} for {level} developer."
print(str1)

# how can we pass dynamically variables in f-string
# We can create a method and call that with variables
def formatString(topic, level):
    str2 = f"Explain {topic} for {level} developer."
    return str2

print(formatString("Java", "senior"))

# string.format
str = "Explain {topic} for {level} developer."
output = str.format(topic="angular", level="beginner")
print(output)

# use string.format in a function
str3 = "Explain {topic} for {level} developer."
def formatString1(topic, level):
    return str3.format(topic=topic, level=level)

print(formatString1('React', "Expert"))

#--------------------------------

class Product:
    def __init__(self, price):
        self._price = price # _variable just tells that this attribute is only for internal purpose.

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        elif value < 100:
            print('Warning: Minimum deposit is allowed 500.')
        else: 
          self._price = value

product = Product(500) # initial amount
print(product.price)  # 500

product.price = 700   # Validation runs
print(product.price)  #  700

product.price = 80  # Validation runs
# Warning: Minimum deposit is allowed 500.

# product.price = -100  # ValueError: Price cannot be negative

#------------------------------------------------------------------------------

import sys

print('Version:', sys.version)       # Python version
print('Platform:', sys.platform)      # Operating system platform
print('Arguments:', sys.argv)          # Command-line arguments

import textwrap

text = "Python is useful for AI development."
print('textwrap' ,textwrap.fill(text, width=15))
'''
Python is
useful for AI
development.
'''
