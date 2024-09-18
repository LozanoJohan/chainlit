import streamlit as st
from openai import OpenAI
import time


client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

@st.cache_data
def create_thread():
    return client.beta.threads.create()

thread = create_thread()

def run_assistant(assistant_id, thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistant_id)
    
    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages)
    new_message = messages.data[0].content[0].text.value
    print(f"Generated message: {new_message}")
    return new_message






assistant_id = st.query_params.get("assistant_id")
title = st.query_params.get("title")

if not assistant_id or not title:
    st.subheader("¡Crea tu primer vendedor para empezar a usarlo!")
else: st.subheader(title)



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt,
    )
        st.markdown(prompt)
    
    if not assistant_id or not thread:
        response = "Personaliza tu chat primero!"
    else:
        response = run_assistant(assistant_id, thread)
    # Add user message to chat history
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})



# import streamlit as st
# from openai import OpenAI
# import time
# import shelve


# client = OpenAI(
#     api_key="sk-KaBn9NWnh0sJXIIX1KPx8WP8b7fsyKZGdq6IWl18DGT3BlbkFJendov-4GMG-jtynOI7cGTfbUdpZUD4LFw-HLrCiFYA"
# )


# prompt = st.chat_input("Say something")
# if prompt:
#     st.write(f"User has sent the following prompt: {prompt}")

# if st.query_params.get("assistant_id"):
#     response = generate_response()
#     st.write(st.query_params["assistant_id"])


# # --------------------------------------------------------------
# # Thread management
# # --------------------------------------------------------------
# def check_if_thread_exists(wa_id):
#     with shelve.open("threads_db") as threads_shelf:
#         return threads_shelf.get(wa_id, None)


# def store_thread(wa_id, thread_id):
#     with shelve.open("threads_db", writeback=True) as threads_shelf:
#         threads_shelf[wa_id] = thread_id


# # --------------------------------------------------------------
# # Generate response
# # --------------------------------------------------------------
# def generate_response(message_body, wa_id, name):
#     # Check if there is already a thread_id for the wa_id
#     thread_id = check_if_thread_exists(wa_id)

#     # If a thread doesn't exist, create one and store it
#     if thread_id is None:
#         print(f"Creating new thread for {name} with wa_id {wa_id}")
#         thread = client.beta.threads.create()
#         store_thread(wa_id, thread.id)
#         thread_id = thread.id

#     # Otherwise, retrieve the existing thread
#     else:
#         print(f"Retrieving existing thread for {name} with wa_id {wa_id}")
#         thread = client.beta.threads.retrieve(thread_id)

#     # Add message to thread
#     message = client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=message_body,
#     )

#     # Run the assistant and get the new message
#     new_message = run_assistant(thread)
#     print(f"To {name}:", new_message)
#     return new_message


# def run_assistant(thread, assistant_id):
#     # Retrieve the Assistant
#     assistant = client.beta.assistants.retrieve(assistant_id)

#     # Run the assistant
#     run = client.beta.threads.runs.create(
#         thread_id=thread.id,
#         assistant_id=assistant.id,
#     )

#     # Wait for completion
#     while run.status != "completed":
#         # Be nice to the API
#         time.sleep(0.5)
#         run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

#     # Retrieve the Messages
#     messages = client.beta.threads.messages.list(thread_id=thread.id)
#     new_message = messages.data[0].content[0].text.value
#     print(f"Generated message: {new_message}")
#     return new_message
