import streamlit as st
import logging
import sys
import requests
from rag import YoutubeStudyAssistant  # Import custom YouTube RAG assistant module

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# --- Assistant Initialization ---
logging.info("Initializing YouTubeStudyAssistant")

# --- Sidebar Input Widgets ---
with st.sidebar:
    # Input box for YouTube URL
    youtube_url = st.text_input("Paste a YouTube URL", "https://www.youtube.com/watch?v=KTzGBJPuJwM")
    # Button to trigger knowledge base creation
    build_button = st.button("⚙️ Build Knowledge Base")

# --- Constants ---
FLASK_API_URL = "http://localhost:5050"  # Local backend API URL
HEADERS = {'Content-Type': 'application/json'}  # Set headers for JSON communication

# --- Session State Initialization ---
if 'messages' not in st.session_state:
    st.session_state.messages = []  # Initialize chat history if not already present

# --- Build Knowledge Base Logic ---
if build_button:
    st.session_state.messages = []  # Clear chat history
    logging.info(f"Build button clicked with URL: {youtube_url}")
    try:
        # Send POST request to backend to build knowledge base
        response = requests.post(
            f"{FLASK_API_URL}/build",
            json={"url": youtube_url},
            headers=HEADERS
        )
        logging.info(f"Response object: {response}")
        logging.info(f"Response from /build: {response.status_code} - {response.text}")

        # Handle success response
        if response.status_code == 200:
            st.success("Knowledge base built successfully!")
            logging.info("Knowledge base built successfully")
        else:
            # Attempt to extract error message
            try:
                error_msg = response.json().get('error', 'Unknown error')
            except Exception:
                error_msg = response.text or 'Unknown error'
            st.error(f"Error: {error_msg}")
            logging.error(f"Error building knowledge base: {error_msg}")
    except Exception as e:
        # Handle any request exceptions
        st.error(f"Error: {e}")
        logging.error(f"Error during POST request to /build: {e}")

# --- Query Input Section ---
user_query = st.text_input("Ask a question:")  # User input for a query

# --- Handle Query Submission ---
if user_query:
    logging.info(f"User query received: {user_query}")
    with st.spinner("Generating response..."):
        try:
            # Send POST request to backend with the query
            response = requests.post(
                f"{FLASK_API_URL}/query",
                json={"query": user_query},
                headers=HEADERS
            )
            logging.info(f"Response from /query: {response.status_code} - {response.text}")

            if response.status_code == 200:
                # Extract and display assistant response
                assistant_response = response.json().get('response', '')
                st.session_state.messages.append({"role": "user", "content": user_query})
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                logging.info(f"Assistant response: {assistant_response}")
            else:
                # Attempt to extract error message
                try:
                    error_msg = response.json().get('error', 'Unknown error')
                except Exception:
                    error_msg = response.text or 'Unknown error'
                st.error(f"Error: {error_msg}")
                logging.error(f"Error during POST request to /query: {error_msg}")
        except Exception as e:
            # Handle exceptions during the request
            st.error(f"Error: {e}")
            logging.error(f"Error during POST request to /query: {e}")

# --- Display Chat Messages ---
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.chat_message("user").markdown(message['content'])  # Display user message
    else:
        st.chat_message("assistant").markdown(message['content'])  # Display assistant response