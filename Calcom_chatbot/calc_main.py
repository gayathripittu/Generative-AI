import os
import requests
import json
import streamlit as st


from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY= os.environ.get("GOOGLE_API_KEY")
CALCOM_API_KEY=os.environ.get("CALCOM_API_KEY")

import vertexai
from vertexai.generative_models import (
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool,
)

PROJECT_ID = "dinesmart-430016" # @param {type:"string"}
LOCATION = "us-east4"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize Gemini model gemini-1.0-pro
model = GenerativeModel(model_name="gemini-1.0-pro-001")


def get_all_bookings(attendee_email):
    """
    Retrieves all bookings for a given attendee email address using the Cal.com API.

    Args:
        attendee_email (str): The email address of the attendee for whom to retrieve bookings.

    Returns:
        dict: A dictionary containing the parsed JSON response from the API,
              or None if the request failed.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the request.
    """

    url = "https://api.cal.com/v1/bookings"
    query_params = {"apiKey": CALCOM_API_KEY}  # Replace with your actual key
    data = {"attendeeEmail": attendee_email}

    try:
        response = requests.get(url, params=query_params, json=data)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "An unexpected error occurred", "details": str(e)})

from datetime import datetime, timezone, timedelta

def slot_availbility(date):
    
    url = "https://api.cal.com/v1/slots"

    query_params = {
        "apiKey": CALCOM_API_KEY,
        "eventTypeId": 1237037,
        "startTime": f'{date}T00:00:00.000Z',                 
        "endTime": f'{date}T23:45:00.000Z' 

    }
    
    
    try:
        response = requests.get(url, params=query_params)
        response.raise_for_status()  # Raise exception for non-200 status codes
        data= response.json()
        times = []
        for date, slots in data['slots'].items():
            for slot in slots:
            # Parse the time and extract only the time portion (HH:MM:SS)
                time_str = slot['time']
                utc_offset = timezone(timedelta(hours=-5))
                time_obj = datetime.fromisoformat(time_str.replace('Z', '+00:00')).astimezone(utc_offset)
                times.append(time_obj.strftime('%H:%M:%S'))
        return times
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error :{e}")
    

def create_booking(start,email,date):
    """Creates a new booking on a calendar API.

    Args:
      start (str): The start time of the booking
      email (str): The email address of the attendee.
      date(str): Booking date in YYYY-MM-DD FORMAT 
      title (str, optional): The title of the booking. Defaults to "Team Meeting".
      description (str, optional): The description of the booking. Defaults to "Meeting Description".
      status (str, optional): The status of the booking (e.g., "confirmed", "pending"). Defaults to "confirmed".

    Returns:
      dict: The JSON response from the API call, containing information about the created booking.
          Raises an exception if the API call fails.

    Raises:
      Exception: If the API call returns an error code or unexpected response.
    """
    # Check slot availability on Cal.com's API
    available_slots=slot_availbility(date)
    
    url = "https://api.cal.com/v1/bookings"

    query_params = {
      "apiKey": CALCOM_API_KEY
    }

    start_time=f'{date}T{start}-05:00' # Combine date, time, and time zone offset

    if start in available_slots:
    
        data = {
            "eventTypeId": int(1237037), # Replace with appropriate event type ID for your Cal.com calendar
            "start": start_time,
            "responses": {
              "name": "gayathri",
              "email": email,
              "guests": [],
              "location": {
                  "value": "integrations:calcom",
                  "optionValue": ""
              }
            },
            "metadata": {},
            "timeZone": "America/New_York",  # Adjust if needed
            "language": "en",
            "title": "",
            "description": "",
            "status": "confirmed",
            "seatsPerTimeSlot": 10,
            "seatsShowAttendees": True,
            "seatsShowAvailabilityCount": True
        }
    
        try:
            response = requests.post(url, params=query_params,json=data)
            response.raise_for_status()  # Raise exception for non-200 status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error creating booking: {e}")
    else:
        return f'slot time is not avaible. Available slot times {available_slots}'
    

def edit_booking(id, title,description,status="CANCELLED"):
    """Edits a booking on a calendar API.
    Args:
      id (int): The ID of the booking to edit.
      title (str, optional): The new title for the booking. Defaults to "".
      start (str, optional): The new start time for the booking (format depends on API). Defaults to "".
      end (str, optional): The new end time for the booking (format depends on API). Defaults to "".
      status (str, optional): The new status for the booking. Defaults to "CANCELLED".
      
    Returns:
      dict: The JSON response from the API call.
      
      """
    url = f"https://api.cal.com/v1/bookings/{id}"

    query_params = {
      "apiKey": CALCOM_API_KEY  # Replace with your actual API key
    }

    # Include only non-empty fields in the data payload
    data = {
        "title": title,
        "status": status,
        "description":description
    }

    response = requests.patch(url, params=query_params, json=data)  # Use PUT for editing

    # Use status code 200 for successful edits (might differ based on API)
    if response.status_code == 200:
      return response.json()
    else:
      raise Exception(f"Error editing booking: {response.text}")

def cancel_booking(booking_id):
    """
    Cancels a booking on a Cal.com calendar using the provided API key and booking ID.

    Args:
        booking_id (int): The unique identifier of the booking to cancel.
        api_key (str): Your Cal.com API key. Replace with your actual key.

    Returns:
        dict: A dictionary containing the response data from the API call,
             or None if the request failed.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """

    url = f"https://api.cal.com/v1/bookings/{booking_id}/cancel"
    query_params = {
      "apiKey": CALCOM_API_KEY  # Replace with your actual API key
    }

    try:
        response = requests.delete(url, params=query_params)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        if response.content:
            return response.json()  # Return JSON data if present
        else:
            return {}  # Return empty dict if response has no content

    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "An unexpected error occurred", "details": str(e)})
    

def run(user_query):

    """
    Handles user queries related to booking management, leveraging a generative model and custom tools.

    Args:
        user_query (str): The user's query.

    Returns:
        tuple: A tuple containing the model's response and the function response object.
    """

    # Function declarations for booking-related operations

    # Define a function for getting all bookings by attendee email
    get_all_bookings_func = FunctionDeclaration(
        name="get_all_bookings",
        description="Retrieves all bookings for a given attendee email address.",
        parameters={
            "type": "object",
            "properties": {"attendee_email": {"type": "string", "description": "email of the attendee"}},
        },
    )
    
    # Define a function for creating a booking with event details (start time, date, and email)
    create_booking_func = FunctionDeclaration(
        name="create_booking",
        description="Creates a new booking with specified event type, start, end, and attendee email.",
        parameters={
            "type": "object",
            "properties": {
                "start": {"type": "string", "description": "start time for the booking(in HH:MM:SS 24hrs format)"},
                "date":{"type":"string", "description": "date in YYYY-MM-DD format, consider year as 2024 if not provided"},
                "email": {"type": "string", "description": "Attendee email"},
            },
            "required": ["start","email","date"]
        },
    )
    
    # Define a function for editing an existing booking, identified by its booking ID
    edit_booking_func = FunctionDeclaration(
        name="edit_booking",
        description="Edits an existing booking with specified ID, start, end, and attendee email.",
        parameters={
            "type": "object",
            "properties": {
                "booking_id": {"type": "integer", "description": "ID of the booking to edit"},
                "title":{"type": "string", "description": "new title of the booking"},
                "start": {"type": "string", "description": "new start time for the booking ISO 8601 format with a -5 timezone offset"},
                "end": {"type": "string", "description": "new End time for the booking ISO 8601 format with a -5 timezone offset"},
                "description": {"type": "string", "description": "#new status for the booking. Allowed values('CANCELLED' | 'ACCEPTED' | 'REJECTED' | 'PENDING' | 'AWAITING_HOST')"},
            },
            "required": ["booking_id"]
        },
    )
    
    # Define a function for canceling an existing booking by its ID
    cancel_booking_func = FunctionDeclaration(
        name="cancel_booking",
        description="Cancels an existing booking with specified ID.",
        parameters={
            "type": "object",
            "properties": {"booking_id": {"type": "integer", "description": "ID of the booking to cancel"}},
            "required": ["booking_id"]
        },
    )
    
    # Create a tool that includes the booking-related functions (get, create, edit, and cancel)
    booking_tool = Tool(
        function_declarations=[
            get_all_bookings_func,
            create_booking_func, 
            edit_booking_func, 
            cancel_booking_func,
        ],
    )
    
    # Initialize the generative model (e.g., Gemini model) with booking tool support
    model = GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=GenerationConfig(temperature=0),
        tools=[booking_tool],
    )

    # Start a chat session
    chat = model.start_chat()
    
    # Send the user's query (user_query) to the model and get a response
    function_response = chat.send_message(user_query)

    
    try:
        # Attempt to extract the function call from the model's response
        function_call=function_response.candidates[0].function_calls[0].name
        function_args=function_response.candidates[0].function_calls[0].args

        # Handle the function call depending on which function was called
        if function_call=='get_all_bookings':
            attendee_email=function_args['attendee_email']
            api_response=get_all_bookings(attendee_email) # Fetch all bookings for the attendee email

            
        elif function_call=="create_booking":
            start=function_args['start']
            email=function_args['email']
            date=function_args['date']
            
            api_response=create_booking(start,email,date) # Create a new booking
    
        elif function_call=="edit_booking":
            booking_id=function_args['booking_id']
            title = function_args['title'] if 'title' in function_args else " "  # Default to an empty string if title is not provided
            description = function_args['description'] if 'description' in function_args else " "
            
            api_response=edit_booking(booking_id,title,description) # Edit the existing booking
    
        elif function_call=="cancel_booking":
            booking_id=function_args['booking_id']
            api_response=cancel_booking(booking_id) # Cancel the booking by ID

        # Send the function's response back as a chat message
        response = chat.send_message(
            Part.from_function_response(
                name=function_call,
                response={
                    "content": api_response,
                },
            ),
        )   
        return response.text,function_response # Return the response text and function response
        
    except:
        # If no function call was made, return the regular model-generated response
        model_response = function_response.candidates[0].text
        return model_response,function_response





def main():
    """Main function to run the Streamlit application."""
    st.title("Calcom Chatbot")
    st.write("Your personal booking fairy, at your service! 🧚‍♀️")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a Prompt Here 🎈"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        assistant_response,function_response = run(prompt)
        with st.chat_message("assistant"):
            
            st.markdown(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        

    

if __name__ == "__main__":
    main()


# Hello! 👋

# What would you like to do today?

# I can help you with:

# Creating bookings 🗓️
# Editing bookings ✏️
# Cancelling bookings ❌
# Viewing all your bookings 📃