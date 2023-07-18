from dataclasses import dataclass
import streamlit as st

st.set_page_config(layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


@dataclass
class InputParams:
    topic: str
    model_name: str
    model_temperature: float
    autopilot: bool


def get_parameters():
    topic = st.sidebar.text_input(
        label="Write a topic you're interested to write about",
        placeholder="python decorators",
    )
    model_name = st.sidebar.selectbox(
        "Select a model",
        options=["gpt3.5", "gpt4"],
        index=0,
    )
    model_temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
    )
    autopilot = st.sidebar.checkbox(
        "Autopilot",
        value=False,
    )

    params = InputParams(
        topic=topic,
        model_name=model_name,
        model_temperature=model_temperature,
        autopilot=autopilot,
    )
    return params


parameters = get_parameters()

start_writing = st.sidebar.button("Start writing")


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    happy = st.checkbox(
        "Are you happy with the answer?",
        value=True,
    )

    if not happy:
        st.write("not happy")
    else:
        st.write("happy")
