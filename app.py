import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="Conversational AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Conversational AI Assistant")
st.caption(
    "A Python-based conversational AI app with customizable prompt engineering."
)

# Load API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

# System prompt
system_prompt = st.sidebar.text_area(
    "System Prompt",
    value="""You are a helpful, concise and reliable AI assistant.
Explain technical concepts clearly and use examples when useful."""
)

# Clear chat
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.previous_interaction_id = None
    st.rerun()

st.sidebar.markdown("### Prompt Engineering")
st.sidebar.caption(
    "Modify the system prompt to change the assistant's "
    "behavior, tone and response style."
)

# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_interaction_id" not in st.session_state:
    st.session_state.previous_interaction_id = None

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask something..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                # First interaction
                if st.session_state.previous_interaction_id is None:

                    interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=prompt,
                        system_instruction=system_prompt
                    )

                # Continue existing conversation
                else:

                    interaction = client.interactions.create(
                        model="gemini-3.6-flash",
                        input=prompt,
                        previous_interaction_id=(
                            st.session_state.previous_interaction_id
                        ),
                        system_instruction=system_prompt
                    )

                answer = interaction.output_text

                st.session_state.previous_interaction_id = interaction.id

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")