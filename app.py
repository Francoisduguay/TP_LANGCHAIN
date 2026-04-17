import streamlit as st
from agent import creer_agent

st.set_page_config(page_title="Agent LangChain", layout="wide")

st.title("Agent LangChain")

# Init agent once
if "agent" not in st.session_state:
    st.session_state.agent = creer_agent()

agent = st.session_state.agent

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask a question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    result = agent.invoke({"input": user_input})
    answer = result["output"]

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)

with st.sidebar:
    st.header("Outils disponibles")

    for tool in agent.tools:
        st.subheader(tool.name)
        st.write(tool.description)

    if st.button("Réinitialiser conversation"):
        st.session_state.messages = []