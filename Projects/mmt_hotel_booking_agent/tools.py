# Contains all required tools for the project.


from langchain_community.tools import tool # Tool decorator.
import db # Database connection.
from datetime import datetime
import uuid
import Projects.common as common # custom function to print text with color
color_text = common.color_text


@tool
def search_hotel(city: str) -> list[dict]:
    """Search for hotels in a given city.
    Args:
        city: The name of the city.
    Returns:
        A list of dictionaries with hotel_id, hotel_name, hotel_phone_number, hotel_city, hotel_rating.
    Validations:
        - City must be provided.
    """
    print(color_text(f"Tool Calling - Searching for hotels in {city}...", "yellow"))
    hotels = db.get_hotel_by_city(city)
    # return dictionary of hotels with hotel_id, hotel_name, hotel_phone_number, hotel_city, hotel_rating
    if hotels:
        hotels_list = [{
            "hotel_id": hotel[0],
            "hotel_name": hotel[1],
            "hotel_phone_number": hotel[2],
            "hotel_city": hotel[3],
            "hotel_rating": hotel[4]
        } for hotel in hotels]
        print(color_text(f'hotel list is {hotels_list}', "cyan"))
        return hotels_list
    else:
        return []

@tool
def search_room_category(hotel_id: int) -> list[dict]:
    """Search for room categories in a given hotel.
    Args:
        hotel_id: The id of the hotel.
    Returns:
        A list of dictionaries with room_id, room_category, room_price, max_occupancy, room_availability.
    Validations:
        - Hotel id must be provided. Please use the search_hotel tool to get the hotel id.
    """
    print(color_text(f"Tool Calling - Searching for room categories in hotel {hotel_id}...", "yellow"))
    room_categories = db.get_room_category_by_hotel_id(hotel_id)
    print(color_text(f'room categories from database are {room_categories}', "cyan"))
    if room_categories:
        room_categories_list = [{
            "room_id": room[0],
            "hotel_id": room[1],
            "room_category": room[2],
            "room_price": room[3],
            "max_occupancy": room[4],
            "room_availability": room[5]
        } for room in room_categories]
        print(color_text(f'room categories list is {room_categories_list}', "green"))
        return room_categories_list
    else:
        return []



@tool
def calculate_booking_price(selected_hotel: str, selected_room_category: str, room_price: float, check_in_date: str, check_out_date: str, number_of_guests: int) -> float:
    """Calculate the booking price for a given hotel, room category, check-in date and check-out date.
    Args:
        selected_hotel: The name of the hotel.
        selected_room_category: The name of the room category.
        room_price: The price of the room.
        check_in_date: The check-in date.
        check_out_date: The check-out date.
        number_of_guests: The number of guests.
    Validations:
        - Selected hotel and room category must be provided. Please use the search_hotel and search_room_category tools to get the hotel and room category.
        - Check-in date and check-out date must be provided.
        - Check-in date must be before check-out date.
        - Number of guests must be greater than 0.
        - Room price must be greater than 0.
    Returns:
        The booking price.
    """
    print(color_text(f"Tool Calling - Calculating booking price for {selected_hotel} with room category {selected_room_category} for {number_of_guests} guests...", "yellow"))
    check_in_date = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out_date, "%Y-%m-%d")
    
    if selected_hotel is None or selected_room_category is None:
        return 'Selected hotel and room category must be provided.'
    if check_in_date is None or check_out_date is None:
        return "Check-in date and check-out date must be provided."
    if check_in_date > check_out_date:  
        return "Check-in date must be before check-out date."
    if number_of_guests <= 0:
        return "Number of guests must be greater than 0."
    if room_price <= 0:
        return "Room price must be greater than 0."

    days = (check_out_date - check_in_date).days
    required_rooms = (number_of_guests + 1) // 2 # Each room can accommodate 2 guests. 3 Guest means 2 rooms.
    booking_price = room_price * days * required_rooms
    print(color_text(f"Tool Returning - Calculated booking price is {booking_price}", "green"))
    return booking_price

@tool
def book_hotel(selected_hotel: str, selected_room_category: str, check_in_date: str, check_out_date: str, number_of_guests: int, booking_price: float) -> str:
    """Book a hotel for a given hotel, room category, check-in date and check-out date.
    Args:
        selected_hotel: The name of the hotel.
        selected_room_category: The name of the room category.
        check_in_date: The check-in date.
        check_out_date: The check-out date.
        number_of_guests: The number of guests.
        booking_price: The booking price.
    Returns:
        A message indicating that the hotel has been booked successfully.
    Validations:
        - Selected hotel and room category must be provided. Please use the search_hotel and search_room_category tools to get the hotel and room category.
        - Check-in date and check-out date must be provided.
    """
    print(color_text(f"Tool Calling - Booking hotel {selected_hotel} with room category {selected_room_category} for {number_of_guests} guests...", "yellow"))
    # Generate a random booking transaction id.
    booking_transaction_id = str(uuid.uuid4())
    db.insert_booking_details(booking_transaction_id, selected_hotel, selected_room_category, check_in_date, check_out_date, number_of_guests, booking_price)
    return f"Hotel booked successfully. Booking transaction id: {booking_transaction_id}"

@tool
def booking_confirmation(booking_transaction_id: str) -> str:
    """Get the booking confirmation for a given booking transaction id.
    Args:
        booking_transaction_id: The booking transaction id.
    Returns:
        The booking confirmation.
    Validations:
        - Booking transaction id must be provided.
    """
    print(color_text(f"Tool Calling - Getting booking confirmation for booking transaction id {booking_transaction_id}...", "yellow"))
    booking_details = db.get_booking_details(booking_transaction_id)
    return booking_details if booking_details else "No booking details found for the given booking transaction id."