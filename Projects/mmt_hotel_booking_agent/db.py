import sqlite3
import mmt_hotels_data # Data storage seperate file.

# Create a database
connection =  sqlite3.connect('hotel_booking.db')
# Open Cursor Object
cursor = connection.cursor()

# Create Table hotels   
create_table_hotels_query = '''CREATE TABLE IF NOT EXISTS hotels (
    hotel_id INTEGER PRIMARY KEY NOT NULL,
    hotel_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    rating REAL NOT NULL
)'''

cursor.execute(create_table_hotels_query)

# Create Rooms Table
create_table_rooms_query = '''CREATE TABLE IF NOT EXISTS rooms (
    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL,
    room_category TEXT NOT NULL,
    room_price REAL NOT NULL,
    max_occupancy INTEGER NOT NULL DEFAULT 2,
    room_availability INTEGER NOT NULL
)'''

cursor.execute(create_table_rooms_query)


# First delete all data from the tables
cursor.execute('DELETE FROM hotels')
cursor.execute('DELETE FROM rooms')

# Insert Data into Hotels Table
insert_data_hotels_query = '''INSERT OR IGNORE INTO hotels (hotel_id, hotel_name, phone, city, rating) VALUES (?, ?, ?, ?, ?)'''

# Insert multiple data into hotels table using executemany
cursor.executemany(insert_data_hotels_query, mmt_hotels_data.hotels_data)

# Insert Data into Rooms Table

'''
To prevent duplicate records, you can use: INSERT OR IGNORE INTO [table_name]
'''

insert_data_rooms_query = '''INSERT OR IGNORE INTO rooms (hotel_id, room_category, room_price, max_occupancy, room_availability) VALUES (?, ?, ?, ?, ?)'''

cursor.executemany(insert_data_rooms_query, mmt_hotels_data.rooms_data)

# Create Booking detail table

create_table_booking_details_query = '''CREATE TABLE IF NOT EXISTS booking_details (
    booking_transaction_id TEXT PRIMARY KEY NOT NULL,
    selected_hotel TEXT NOT NULL,
    selected_room_category TEXT NOT NULL,
    check_in_date TEXT NOT NULL,
    check_out_date TEXT NOT NULL,
    number_of_guests INTEGER NOT NULL,
    booking_price REAL NOT NULL
)'''

cursor.execute(create_table_booking_details_query)

connection.commit() # save all changes to db
connection.close() # close the connection to the 

'''
Recommended approach for our project.

Whenever an agent calls a database tool, open a new SQLite connection inside that tool, execute the query, and close the connection.
'''

def get_hotel_by_city(city):
    with sqlite3.connect('hotel_booking.db') as connection:
        cursor = connection.cursor()
        query = '''SELECT * FROM hotels WHERE city = ?'''
        cursor.execute(query, (city,))
        return cursor.fetchall()

def get_room_category_by_hotel_id(hotel_id):
    with sqlite3.connect('hotel_booking.db') as connection:
        cursor = connection.cursor()
        query = '''SELECT * FROM rooms WHERE hotel_id = ?'''
        cursor.execute(query, (hotel_id,))
        return cursor.fetchall()

def insert_booking_details(booking_transaction_id, selected_hotel, selected_room_category, check_in_date, check_out_date, number_of_guests, booking_price):
    with sqlite3.connect('hotel_booking.db') as connection:
        cursor = connection.cursor()
        query = '''INSERT OR IGNORE INTO booking_details (booking_transaction_id, selected_hotel, selected_room_category, check_in_date, check_out_date, number_of_guests, booking_price) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        cursor.execute(query, (booking_transaction_id, selected_hotel, selected_room_category, check_in_date, check_out_date, number_of_guests, booking_price))
        connection.commit()

def get_booking_details(booking_transaction_id):
    with sqlite3.connect('hotel_booking.db') as connection:
        cursor = connection.cursor()
        query = '''SELECT * FROM booking_details WHERE booking_transaction_id = ?'''
        cursor.execute(query, (booking_transaction_id,))
        return cursor.fetchall()

#----------------------------------------------------------------

"""
# Run above commands

#----------------------------------------------------------------

print('----------------------------------------------------------------')
data = get_hotel_by_city('Mumbai')
if data:
        data_list = [{
            "hotel_id": hotel[0],
            "hotel_name": hotel[1],
            "hotel_phone_number": hotel[2],
            "hotel_city": hotel[3],
            "hotel_rating": hotel[4]
        } for hotel in data]
        print(data_list)
print(data)


print('----------------------------------------------------------------')
data = get_room_category_by_hotel_id(1)
print(data)

print('----------------------------------------------------------------')
data = get_booking_details('1234567890')
print(data)

print('----------------------------------------------------------------')

"""



