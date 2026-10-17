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