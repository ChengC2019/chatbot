import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Show title and description.
uah_logo_url = "https://www.uah.edu/images/administrative/communications/logo/uah-logo.svg"

# Create two columns: one for the logo, one for the title
col1, col2 = st.columns([1, 5])  # Adjust ratio to size preference

with col1:
    st.image(uah_logo_url, width=90)
with col2:
    st.title("Teaching Assistant")
st.write(
    "Please feel free to ask any questions about the course syllabus or homework assignments."
    "Please ask course-related or factual questions - such as key concepts for each chapter. "
)

load_dotenv()
USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

openai_api_key = st.secrets["openai"]["api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What questions do you have about the course so far?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
