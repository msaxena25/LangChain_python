from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda
from langchain.agents import create_agent

import tools

model = ChatOllama(model="qwen3.5:latest", temperature=0.2)
tools = [
    tools.search_hotel,
    tools.search_room_category,
    tools.calculate_booking_price,
    tools.book_hotel,
    tools.booking_confirmation,
]

messages = [
    ("system", "You are a helpful assistant that helps users book hotels."),
]

agent = create_agent(
    model=model,
    tools=tools,
    #debug=True,
    system_prompt='''You are a helpful assistant that helps users book hotels.
    You help users book hotels in two steps.
    Step 1: call only search_hotel with the city name.
    Step 2: Return the list of hotels in the city to user.
    Step 3: After the user selects a hotel, call search_room_category with that exact hotel_id.
    Step 4: Return the list of room categories in the hotel to the user.
    Step 5: After the user selects a room category, call calculate_booking_price with that exact hotel_id and room_category.
    Step 6: Return the booking price to the user.
    Step 7: After the user confirms the booking, call book_hotel with that exact hotel_id and room_category.
    Step 8: Return the booking confirmation to the user.

    Keep the conversation friendly and engaging.
    '''
)

print('AI: Hello, I am your hotel booking assistant. How may I help you today?')

while True:
    print('----------------------------------------------------------------')
    user_input = input("You: ")
    if user_input == "exit":
        break
    messages.append(("user", user_input))
    response = agent.invoke({
        "messages": messages
    })
    messages = response["messages"] # agent.invoke() returns the complete updated message history so assigned that into messages.
    print("AI:", response["messages"][-1].content)


'''
You: Suggest me 3 hotels in mumbai for my family trip?

AI: Here are three great hotel options in Mumbai for your family trip:

1. **Hotel Hyatt**
   - Rating: 4.0/5
   - Phone: 99989888999

2. **Hotel Marriott**
   - Rating: 3.9/5
   - Phone: 02211111111

3. **Hotel Sheraton**
   - Rating: 3.8/5
   - Phone: 02443444333

Which one would you like to explore further? Let me know, and I can help you check out the room categories available!

You: I want to book a room in Hotel Marriott.

AI: Great choice! Hotel Marriott has several room categories available for your family trip. Here are the options:

1. **Deluxe Room**
   - Price: ₹4,500 per night
   - Max Occupancy: 2 guests
   - Availability: 8 rooms

2. **Premium Room**
   - Price: ₹6,500 per night
   - Max Occupancy: 2 guests
   - Availability: 4 rooms

3. **Suite Room**
   - Price: ₹9,000 per night
   - Max Occupancy: 2 guests
   - Availability: 2 rooms

Which room category would you like to book? Also, please let me know:
- Your check-in date
- Your check-out date
- Number of guests in your party

Once you provide these details, I can calculate the total booking price for you!

You: Okie Fine. I need to book Premium room for 4 guests.

AI: Great! I'd be happy to help you book a Premium room at Hotel Marriott for 4 guests. However, I need a couple more details to calculate the booking price:

- **Check-in date**: When would you like to check in?
- **Check-out date**: When would you like to check out?

Also, I noticed that the Premium rooms have a maximum occupancy of 2 guests per room according to our system. Since you're traveling with 4 guests, we might need to book multiple rooms or consider a different room category. But let's first get your dates sorted out!

Please provide your preferred check-in and check-out dates, and I'll calculate the total booking price for you.

You: Ok ok, my check In date is 2 nov 2026 and checkout date is 6 nov 2026.

AI: Great! Here's your booking summary:

- **Hotel**: Hotel Marriott
- **Room Category**: Premium Room
- **Check-in Date**: November 2, 2026
- **Check-out Date**: November 6, 2026
- **Number of Guests**: 4
- **Total Booking Price**: ₹52,000

Please note that the Premium room category has a maximum occupancy of 2 guests per room. Since you're booking for 4 guests, you might need to book two rooms or considera different room category with higher occupancy. Would you like to proceed with this booking as is, or would you prefer to adjust your selection?

You: I am fine with this. Proceed for booking.

AI: Your booking has been successfully confirmed! Here are the details:

- **Hotel**: Hotel Marriott
- **Room Category**: Premium Room
- **Check-in Date**: November 2, 2026
- **Check-out Date**: November 6, 2026
- **Number of Guests**: 4
- **Total Booking Price**: ₹52,000
- **Booking Transaction ID**: 5364bd81-4889-44f2-bafa-c755aca11fa4

Please keep your booking transaction ID safe for future reference. If you need any further assistance, feel free to ask. Enjoy your stay at Hotel Marriott!

--------------------------------------------------------------------------------
'''

# Till now agentic flow is perfectly working. 

# Below I am just trying to cancel the booking and want to see how it will respond.

'''
You: Can you cancel this booking?

AI: I'm sorry, but I don't have access to a cancellation function with the current tools available to me. The system only allows me to search for hotels, view room categories, calculate prices, make bookings, and retrieve booking confirmations.

To cancel your booking, you'll need to:

1. Contact Hotel Marriott directly using their phone number (02211111111)
2. Or visit their website/customer service with your booking transaction ID (5364bd81-4889-44f2-bafa-c755aca11fa4)        

I recommend reaching out to them as soon as possible to discuss cancellation options and any applicable fees or policies.Is there anything else I can help you with regarding your hotel search or booking?
'''

# AI did not try any cancel action itself, it just gave the information to cancel the booking. And that is completely correct.


# Now Lets check to search hotels in different city with is not listed in the database.

'''
You: Can you suggest me some hotels in Kolkata?

AI: I'm sorry, but there are currently no hotels listed in our system for Kolkata.

Would you like me to search for hotels in a different city instead? Or perhaps you'd like to explore other options for your trip? Let me know how I can assist you further!

'''


# Now Lets ask AI to search deluxe room price of Hotel Ginger Delhi. And try to book rooms more then available.

'''
You: Can you tell me deluxe room price of Hotel Ginger Delhi?

AI: The Deluxe room at Hotel Ginger in Delhi is priced at ₹3000 per night. This room can accommodate up to 2 guests and currently has 8 rooms available.

Would you like to proceed with booking this room, or would you prefer to explore other options?

You: We are 20 peoples and we need 10 deluxe rooms. we have to go on 2 nov 2026 to 3 nov 2026. 

AI: Here's your booking summary for Hotel Ginger in Delhi:

- **Hotel**: Hotel Ginger
- **Room Category**: Deluxe Room
- **Number of Rooms**: 10 rooms (for 20 guests)
- **Check-in Date**: November 2, 2026
- **Check-out Date**: November 3, 2026
- **Total Booking Price**: ₹30,000

Please note that each Deluxe room can accommodate up to 2 guests, so 10 rooms are required for your group of 20 people.   

Would you like to proceed with this booking? If yes, I'll confirm it for you.

'''

# In above you can see there were only 8 rooms but AI also give me calculation for 10 rooms instead of giving a message that there are only 8 rooms available.  This is Because we did not check this condition in the tools. So tool must be fully validated and full of informative and it must return complete information.


# Check room price without giving any hotel name and city name

'''
You:  What is the price and room availability of Suite room?   

AI: Based on the room categories available at Hotel Ginger Delhi, here are the details for the Suite room:

- **Room Category**: Suite
- **Price**: ₹6500 per night
- **Max Occupancy**: 2 guests
- **Room Availability**: 2 rooms currently available

'''

# In Above AI gave response based on last conversation context and last I was asked about ginger hotel in delhi. 