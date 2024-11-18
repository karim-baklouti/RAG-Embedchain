import os
import json
import streamlit as st
import requests
from datetime import datetime

# File to store session history
SESSION_FILE = "session_history.json"

# Load existing session history or create a new one
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
        st.session_state.session_history = json.load(f)
else:
    st.session_state.session_history = {}

# Automatically create a new session name based on the current timestamp
def create_new_session_name():
    return f"Session {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

# Initialize the current session and messages
if "current_session" not in st.session_state:
    st.session_state.current_session = create_new_session_name()
    st.session_state.messages = []

# Sidebar for managing sessions
with st.sidebar:
    st.title("💬 Chatbot")
    st.caption("MLOps Chatbot")
    
    # Display existing sessions
    st.subheader("Sessions")
    
    # Button to create a new session
    if st.button("Create a new session"):
        new_session_name = create_new_session_name()
        st.session_state.session_history[new_session_name] = []
        st.session_state.current_session = new_session_name  # Switch to the new session
        st.session_state.messages = []  # Reset messages for the new session

        # Automatic request to the API with a default message
        default_query = "How can I help you?"  # You can customize this message
        payload = {"query": default_query}
        response = requests.post("http://localhost:8000/query", json=payload)
        data = response.json()
        answer = data.get("answer", "No answer found.")
        
        # Save the default message and assistant's response in the new session history
        st.session_state.messages.append({"role": "user", "content": default_query})
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Update the session history
        st.session_state.session_history[st.session_state.current_session] = st.session_state.messages

        # Save session history to the file
        with open(SESSION_FILE, "w") as f:
            json.dump(st.session_state.session_history, f)

    # Display existing sessions with a delete icon, sorted in descending order
    for session in sorted(st.session_state.session_history.keys(), reverse=True):
        col1, col2 = st.columns([3, 1])  # Two columns for selecting and deleting
        with col1:
            if st.button(session):
                st.session_state.current_session = session
                st.session_state.messages = st.session_state.session_history[session]
        with col2:
            if st.button("❌", key=session):  # Using an icon to delete the session
                # Delete the session and update session state immediately
                del st.session_state.session_history[session]
                st.session_state.current_session = create_new_session_name()  # Create a new session
                st.session_state.messages = []  # Clear messages
                # Update session history file
                with open(SESSION_FILE, "w") as f:
                    json.dump(st.session_state.session_history, f)

# API URL for FastAPI
API_URL = "http://localhost:8000/query"

# Streamlit application layout
st.title("MLOPS BOT")

# Display historical messages with emojis
if st.session_state.messages:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        if role == "assistant":
            st.markdown(f"🤖 **{role.capitalize()}** : {content}")  # Emoji for the assistant
        else:
            st.markdown(f"👤 **{role.capitalize()}** : {content}")  # Emoji for the user

# Text input field to enter the query
query = st.text_input("Enter your query:")

# Button to send the query to FastAPI
if st.button("Submit the query"):
    if query:
        # Prepare the payload to send to FastAPI
        payload = {"query": query}
        
        try:
            # Send the POST request to FastAPI and get the response
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()  # Check if the request was successful
            
            # Extract the response from the response
            data = response.json()
            answer = data.get("answer", "No answer found.")
            
            # Save the user's message and the assistant's response in the current session history
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # Update the session history
            st.session_state.session_history[st.session_state.current_session] = st.session_state.messages

            # Save session history to the file
            with open(SESSION_FILE, "w") as f:
                json.dump(st.session_state.session_history, f)
            
            # Display the result
            st.success(f"Response: {answer}")
        
        except requests.exceptions.RequestException as e:
            # Display an error if the request fails
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a query before submitting.")

# Automatically create a new session if the user hasn't switched from an existing session
if st.session_state.current_session not in st.session_state.session_history:
    st.session_state.session_history[st.session_state.current_session] = []


