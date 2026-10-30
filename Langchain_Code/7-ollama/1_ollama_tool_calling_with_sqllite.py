# Use Ollama Model with tools without Langchain library

'''
Let's build this as a practical Ollama tool-calling example using Python, SQLite, and two tools: check_stock and check_price.

The important learning objective is to see the complete flow:

1. Store three mobile phones in a SQLite database.
2. Store discounts in a separate table.
3. Define Python tools that query the database.
4. Give the tools to an Ollama model.
5. Inspect the tool schemas sent to the LLM.
6. Execute requested tools and send their results back to the model.
'''

# Install packages

'''
pip install -U ollama
'''

# We will use SQLLite here to store and get data. (Purpose - to Learn how to work with SQLLite in Python)


# SQLite Package 
# In Python, the SQLite package is sqlite3, and it is included in Python's standard library.

import sqlite3
import ollama

db_path = "products.db" # path to the database file

# connect(): If the database file does not exist, it will be created And If it exists, it will be connected to the database.
conn = sqlite3.connect(db_path)

# a cursor is an object used to execute SQL queries and retrieve their results from a database connection.
cursor = conn.cursor() 

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

# Create the table if it doesn't exist
cursor.execute(create_table_query)

discount_query = '''
    CREATE TABLE IF NOT EXISTS discounts
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discount_name TEXT NOT NULL,
    discount_description TEXT NOT NULL,
    discount_percentage REAL NOT NULL
)
'''
# Create the table if it doesn't exist
cursor.execute(discount_query)

# Product Data
products = [
    ("iPhone 15", "The latest iPhone model", 1000, 100),
    ("Samsung Galaxy S23", "The latest Samsung Galaxy model", 900, 100),
    ("Google Pixel 8", "The latest Google Pixel model", 800, 100),
]

# Delete existing products from the table || Reset the table
delete_products_query = "DELETE FROM products"
cursor.execute(delete_products_query)

# Delete existing discounts from the table || Reset the table
delete_discounts_query = "DELETE FROM discounts"
cursor.execute(delete_discounts_query)

# Insert products into the table
insert_products_query = '''
INSERT INTO products (product_name, product_description, product_price, in_stock)
VALUES (?, ?, ?, ?)
'''
#Execute the insert_products_query for each product in the products list
cursor.executemany(insert_products_query, products)

# Discount Data
discounts = [
    ("Savings Discount", "10% discount on all products", 10),
    ("UPI Discount", "20% discount on all products", 20),
    ("Credit Card Discount", "30% discount on all products", 30),
]

# Insert discounts into the table
insert_discounts_query = '''
INSERT INTO discounts (discount_name, discount_description, discount_percentage)
VALUES (?, ?, ?)
'''

#Execute the insert_discounts_query for each discount in the discounts list
cursor.executemany(insert_discounts_query, discounts)


# Commit the changes to the database
conn.commit()

# Select all products from the products table
select_products_query = "SELECT * FROM products"
cursor.execute(select_products_query)
rows = cursor.fetchall() # fetchall() is a method that retrieves all the rows from the result set of a query.

print("Products:")
for row in rows:
    print(row)

# Select all discounts from the discounts tabl
select_discounts_query = "SELECT * FROM discounts"
cursor.execute(select_discounts_query)
rows = cursor.fetchall() # fetchall() is a method that retrieves all the rows from the result set of a query.

print("Discounts:")
for row in rows:
    print(row)

# Close the connection
conn.close()

#-------------------------------------------------------------------

# Above we only did the data manipulation part with SQLite, now we will do the tool calling part.

# Define Simple Python functions that query the database

def check_stock(product_name: str) -> int:
    # with statement is used to ensure that the connection is closed after the block of code is executed.
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT in_stock FROM products WHERE product_name = ?", (product_name,))
        result = cursor.fetchone()
    return result[0] if result else 0

def check_price(product_name: str) -> float:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_price FROM products WHERE product_name = ?", (product_name,))
        result = cursor.fetchone()
    return float(result[0]) if result else 0

messages = [
    {
        'role': 'system',
        'content': 'You are a helpful assistant that can check the stock and price of a product.'
    },
    {
        'role': 'user',
        'content': 'What is the stock of iPhone 15? And what is the price of iPhone 15?'
    }
]

# Give the tools to an Ollama model
tools = [check_stock, check_price]

# Note  - ollama.generate dont have feature of tools, so we use ollama.chat

result = ollama.chat(model="llama3.1:8b", messages=messages, tools=tools)

print(result.message.tool_calls)
'''
[ToolCall(function=Function(name='check_stock', arguments={'product_name': 'iPhone 15'})), 
ToolCall(function=Function(name='check_price', arguments={'product_name': 'iPhone 15'}))]
'''

for tool_call in result.message.tool_calls:
    tool_name = tool_call.function.name
    args = tool_call.function.arguments
    if tool_name == "check_stock":
        result = check_stock(**args)
        print(f"Stock: {result}")
    elif tool_name == "check_price":
        result = check_price(**args)
        print(f"Price: {result}")
    messages.append({
        'role': 'tool',
        'content': f"Result: {result}"
    })

# Below is refactored code for better readability and maintainability.
'''
available_functions = {
    'check_stock': check_stock,
    'check_price': check_price,
}

for tool_call in result.message.tool_calls:
    tool_name = tool_call.function.name
    result = available_functions[tool_name](**tool_call.function.arguments)
    messages.append({
        'role': 'tool',
        'content': f"Result: {result}"
    })
'''
# Now finally called Model with the updated messages
final_result = ollama.chat(model="llama3.1:8b", messages=messages)
print(final_result.message.content)

'''
Stock: 100
Price: 1000.0

I've checked the stock and price of the iPhone 15 for you.

The current stock of iPhone 15 is: **100**
The current price of iPhone 15 is: **$1000.0**
'''