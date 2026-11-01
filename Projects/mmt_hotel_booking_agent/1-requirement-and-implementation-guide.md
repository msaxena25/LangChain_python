# MakeMyTrip – Agentic Hotel Booking System

## 1. Project Objective

Build a console-based, AI-powered hotel booking assistant using Python, LangChain, LangGraph, Ollama, and SQLite.

The system should understand natural-language conversations and help users:

1. Find hotels in a supported city.
2. Explore hotel details and room categories.
3. Check room availability and prices.
4. Provide booking details in natural language.
5. Calculate the total booking amount.
6. Confirm or cancel the booking.
7. Generate a booking ID and display booking confirmation.

This is a learning project. We will simulate the booking process rather than integrate with a real hotel booking service.

---

## 2. Technology Stack

| Component                   | Technology                                    |
| --------------------------- | --------------------------------------------- |
| Programming language        | Python                                        |
| AI model                    | Qwen3.5 (`qwen3.5:latest`)                    |
| Local model runtime         | Ollama                                        |
| LangChain model integration | ChatOllama                                    |
| Agent creation              | LangChain `create_agent()`                    |
| Agent orchestration         | LangGraph (used internally by `create_agent`) |
| Database                    | SQLite                                        |
| User interface              | Python console                                |
| Database access             | Python `sqlite3`                              |

---

# 3. Functional Requirements

## Requirement 1: Console-based conversation

- Take user input through the Python console.
- Support continuous conversation until the user exits.
- Maintain conversation history.
- Remember the previously selected city, hotel, and booking details.
- Respond naturally to greetings and general queries.

Example:

User:\
Hi

Agent:\
Hello! Welcome to MakeMyTrip. How may I help you?

User:\
I am looking for a hotel in Jaipur.

## Requirement 2: Hotel recommendations

- Understand the city provided by the user.
- Search the hotel database using the `search_hotels` tool.
- Display up to 3 matching hotels.
- Show the following information:
  - Hotel name
  - Star rating
  - Location
  - Starting price per night
  - Facilities

### Supported cities

Initially, we will maintain:

- Jaipur – 3 hotels
- Delhi – 3 hotels

No separate City table is required. The city name will be stored as a field in the Hotels table.

If the user requests an unsupported city, display:

"Currently, we are operating in Jaipur and Delhi. Please let me know if you would like to explore hotels in either of these locations."

### Next-action guidance

After displaying the hotels, the agent must ask:

"Which hotel would you like to explore? You can select a hotel to check its room availability and prices."

## Requirement 3: Hotel details and room availability

- Allow users to select a hotel from the recommendations.
- Retrieve hotel details and room categories from SQLite.
- Check available rooms and their prices.
- Display:
  - Hotel name
  - Room categories
  - Price per room per night
  - Available quantity

Example:

User:\
Is Hotel A available?

Agent:

Hotel A has the following room categories:

1. Deluxe Room – ₹5,000/night
2. Premium Room – ₹7,000/night
3. Suite – ₹10,000/night

Would you like to book a room?

If yes, please provide:

- Check-in date
- Check-out date or duration
- Number of guests
- Room category

The selected hotel will be remembered from the conversation.

## Requirement 4: Collect booking information

The user should be able to provide booking information in a single natural-language message.

Example:

User:

"I want to book a Deluxe Room for 4 people for 3 days, starting 10 November."

The agent should extract:

- Hotel name – from previous conversation
- Check-in date
- Check-out date or duration
- Number of guests
- Room category
- Number of rooms – calculated automatically

If any required information is missing, the agent should ask the user for it.

### Room calculation rule

We will use a simple fixed rule:

- 1 room = 2 guests
- 3–4 guests = 2 rooms
- 5–6 guests = 3 rooms
- 7–8 guests = 4 rooms

Formula:

`required_rooms = (number_of_guests + 1) // 2`

No extra beds, extra guest charges, or room-capacity adjustments.

For pricing, a duration of 3 days will mean 3 nights. When dates are provided, the number of nights will be calculated from the check-in and check-out dates.

## Requirement 5: Calculate price and show booking summary

Once all required information is collected:

1. Calculate the required number of rooms.
2. Calculate the total number of nights.
3. Check the selected room category's availability.
4. Calculate the total booking amount.
5. Display the complete booking summary.
6. Ask the user for confirmation.

### Pricing formula

`total_amount = required_rooms * price_per_room * number_of_nights`

Example:

User:

I want to book a Deluxe Room for 4 people for 3 days.

Agent:

Please review your booking details:

- Hotel: Hotel A
- Room Category: Deluxe
- Check-in: 10 November
- Check-out: 13 November
- Guests: 4
- Rooms: 2
- Price per room/night: ₹5,000
- Duration: 3 nights

**Total Amount: ₹30,000**

Would you like to confirm this booking?

Please reply Yes or No.

## Requirement 6: User confirmation

The agent must wait for explicit user confirmation before booking.

Accept natural-language confirmation such as:

- Yes
- Yes, confirm
- Go ahead
- Please book it
- Confirm my booking

If the user declines:

- Do not invoke the booking tool.
- Inform the user that the booking process was cancelled.
- Allow the user to start another booking.

If the user confirms:

- Invoke the `book_hotel` tool.
- Pass the confirmed booking details.

Important: The agent must not book a hotel simply because the user previously expressed an interest in booking it.

## Requirement 7: Hotel booking

Create a tool named `book_hotel`.

Responsibilities:

1. Accept the confirmed booking details.
2. Generate a unique booking ID (for example, `MMT10001`).
3. Pass the booking ID and booking details to the booking confirmation functionality.
4. Return the result.

### Simplification

We will not implement:

- Actual hotel reservation APIs.
- Room inventory updates.
- Payment processing.
- Complex database transactions.
- Booking cancellation APIs.

The booking ID will be generated for simulation purposes.

## Requirement 8: Booking confirmation

Create a separate tool named `booking_confirmation`.

Responsibilities:

1. Accept the booking ID.
2. Accept the booking details.
3. Prepare the final confirmation message.
4. Return the confirmation to the agent.

The `book_hotel` workflow will invoke the booking confirmation functionality after generating the booking ID.

Example:

Congratulations! Your hotel booking is confirmed.

- Booking ID: MMT10001
- Hotel: Hotel A
- Room Category: Deluxe
- Guests: 4
- Rooms: 2
- Check-in: 10 November
- Check-out: 13 November
- Duration: 3 nights

**Total Amount: ₹30,000**

Thank you for choosing MakeMyTrip!

---

# 4. Database Requirements

We will use SQLite to maintain hotel and room information.

Initially, we will create two tables.

### Table 1: Hotels

| Column     | Description          |
| ---------- | -------------------- |
| hotel_id   | Unique hotel ID      |
| hotel_name | Hotel name           |
| city       | City name            |
| rating     | Hotel star rating    |
| location   | Hotel location       |
| facilities | Available facilities |

### Table 2: Rooms

| Column          | Description              |
| --------------- | ------------------------ |
| room_id         | Unique room ID           |
| hotel_id        | Associated hotel ID      |
| room_category   | Deluxe, Premium, Suite   |
| price_per_night | Price per room per night |
| available_rooms | Available room quantity  |

### Initial data

- 3 hotels in Jaipur.
- 3 hotels in Delhi.
- Each hotel will have multiple room categories.
- Each room category will have its own price and available quantity.

We do not need a separate City table.

We also do not need a Bookings table initially because we are not persisting simulated bookings or updating inventory.

---

# 5. Agent Tools

We will create six tools.

| Tool                      | Responsibility                                           |
| ------------------------- | -------------------------------------------------------- |
| `search_hotels`           | Search hotels by city                                    |
| `get_hotel_details`       | Retrieve hotel details and room categories               |
| `check_room_availability` | Check room availability for requested dates and quantity |
| `calculate_booking_price` | Calculate the total booking amount                       |
| `book_hotel`              | Generate a booking ID and initiate confirmation          |
| `booking_confirmation`    | Generate the final booking confirmation                  |

### Tool execution flow

The agent will decide which tools to invoke based on the user's request.

For dependent operations, we will ensure that the required information from one step is passed to the next.

For the final booking sequence:

1. User confirms the booking.
2. `book_hotel` generates a booking ID.
3. The booking confirmation functionality receives the booking ID and booking details.
4. The agent displays the final confirmation.

---

# 6. Implementation Guidelines

We will implement the project incrementally rather than writing the entire application at once.

### Phase 1: Project setup

- Create a Python project.
- Set up a virtual environment.
- Install required packages.
- Configure Ollama.
- Download the Qwen3.5 model.
- Verify that ChatOllama can communicate with the local model.

### Phase 2: SQLite database

- Create the SQLite database.
- Create Hotels and Rooms tables.
- Insert 3 Jaipur hotels and 3 Delhi hotels.
- Add room categories, prices, and availability.
- Test database queries independently.

### Phase 3: Create individual tools

Implement and test each tool independently:

1. `search_hotels`
2. `get_hotel_details`
3. `check_room_availability`
4. `calculate_booking_price`
5. `book_hotel`
6. `booking_confirmation`

Use Python's `sqlite3` module to interact with the database.

### Phase 4: Create the agent

- Initialize `ChatOllama`.
- Configure the Qwen3.5 model.
- Import `create_agent` from `langchain.agents`.
- Register all six tools.
- Define the system prompt.
- Create the agent.

### Phase 5: Conversation memory

- Maintain conversation history across console interactions.
- Use a consistent conversation/thread ID.
- Preserve selected hotel and pending booking details.
- Use a LangGraph checkpointer for conversation state persistence during the session.

### Phase 6: Console application

- Implement the continuous input loop.
- Pass each user message to the agent.
- Extract and print only the final response.
- Handle exit commands.

### Phase 7: End-to-end testing

Test the complete conversation:

Greeting → Hotel Search → Hotel Selection → Availability → Booking Details → Price Calculation → Confirmation → Booking ID → Final Confirmation.

---

# 7. Edge Cases to Handle

We should consider the following scenarios during implementation.

### A. User input and conversation

1. User enters an unsupported city.
2. User enters an invalid or unknown hotel name.
3. User asks for hotel recommendations without specifying a city.
4. User changes the city during the conversation.
5. User changes the selected hotel.
6. User provides incomplete booking information.
7. User provides multiple booking details in an unexpected order.
8. User sends an unrelated message during the booking process.
9. User starts a new booking after completing or cancelling the previous one.

### B. Date validation

1. Check-in date is in the past.
2. Check-out date is before check-in.
3. Check-in and check-out dates are identical.
4. User provides an invalid date format.
5. User provides only a duration without a starting date.
6. User provides an ambiguous date such as "next Friday".

### C. Guest and room calculation

1. Guest count is zero or negative.
2. User provides a non-numeric guest count.
3. User provides a very large guest count.
4. Correctly calculate rooms for odd and even guest counts.
5. User changes the number of guests after receiving the booking summary.

### D. Room availability

1. Selected room category does not exist.
2. No rooms are available.
3. Available room quantity is less than the required quantity.
4. User selects an invalid room category.
5. Requested hotel is available, but the selected room category is unavailable.

### E. Pricing

1. Room price is missing or invalid.
2. Number of nights is calculated incorrectly.
3. Required rooms are calculated incorrectly.
4. Total amount is calculated incorrectly.
5. User changes the room category or booking duration after price calculation.

### F. Confirmation and booking

1. User confirms the booking.
2. User declines the booking.
3. User provides an ambiguous confirmation.
4. User changes booking details after the confirmation summary.
5. Agent must not call `book_hotel` before explicit confirmation.
6. Booking ID generation fails.
7. Booking confirmation receives incomplete booking details.
8. Booking confirmation must use the same booking ID generated by `book_hotel`.
9. Prevent duplicate booking tool calls for the same confirmation.

### G. Database and application errors

1. SQLite database file does not exist.
2. Required tables are missing.
3. Database connection fails.
4. No matching hotel records are found.
5. SQL query returns empty results.
6. Ollama service is not running.
7. Requested model is not available locally.
8. LLM returns an invalid tool argument.
9. Tool execution fails or returns an unexpected result.

---

# 8. Important Business Rules

These rules must be consistently followed throughout the application:

1. Only Jaipur and Delhi are supported initially.
2. Each city has three hotels.
3. One room accommodates two guests for our simplified calculation.
4. Required rooms = `(guests + 1) // 2`.
5. Pricing is per room per night.
6. Total price = rooms × price per room × nights.
7. Check room availability before presenting the final booking summary.
8. Explicit user confirmation is mandatory before invoking `book_hotel`.
9. `book_hotel` generates a simulated booking ID.
10. Booking confirmation displays the final booking details.
11. No real inventory updates or payment processing will be implemented.

---

# 9. Expected Final Architecture

The overall application will have these components:

**Console Application**

- Receives user messages.
- Maintains the conversation session.
- Displays agent responses.

**LangChain Agent**

- Uses ChatOllama with Qwen3.5.
- Understands user intent.
- Selects the appropriate tools.
- Maintains the tool-calling conversation loop.

**Tools Layer**

- Hotel search.
- Hotel details.
- Room availability.
- Price calculation.
- Hotel booking.
- Booking confirmation.

**SQLite Database**

- Hotels.
- Rooms.

### Overall flow

User → Console → `create_agent()` → LLM decides the next action → Tool execution → SQLite (when required) → Agent response → Console.

---

## 10. Project Completion Criteria

The project will be considered complete when:

- A user can interact with the system through the console.
- The agent can recommend hotels in Jaipur and Delhi.
- The agent can retrieve hotel and room information from SQLite.
- The agent can understand booking details from natural-language input.
- Room quantity and total price are calculated correctly.
- The agent asks for confirmation before booking.
- A confirmed booking generates a booking ID.
- The booking confirmation tool returns the final booking summary.
- The complete conversation works without losing important context.

Implementation reference points: `create_agent()` manages the model/tool execution loop and supports checkpointers for conversation state.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://reference.langchain.com\&sz=32)

LangChain Reference

+1

`ChatOllama` is provided by the `langchain-ollama` integration.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://reference.langchain.com\&sz=32)

LangChain Reference

&#x20;Ollama's Qwen3.5 listing identifies tool support and provides the `qwen3.5` model tag.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ollama.com\&sz=32)

Ollama



One design detail we'll preserve while coding: SQLite will store hotel and room data; simulated bookings will generate an ID without modifying hotel inventory. Also, the confirmation tool can be invoked by the `book_hotel` workflow, so the two steps remain explicit and testable.