import streamlit as st
from langchain_ollama import ChatOllama

from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder 
)
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory

st.title('Ask about Superheroes')
st.write('Get information about Marvel and DC superheroes')



base_url = "http://localhost:11434"
model = 'llama3.2:3b'
user_id = st.text_input("Enter User ID: ", 'mahbubhossain')



def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button('Start New Conversation'):
    st.session_state.chat_history = []
    history = get_session_history(user_id)
    history.clear()

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

    

### LLM Setup
llm = ChatOllama(base_url=base_url,model=model)

# Define the prompt templates.
system_message = SystemMessagePromptTemplate.from_template('Act as an AI Assistant')
human_message = HumanMessagePromptTemplate.from_template('{input}')

messages = [system_message, MessagesPlaceholder(variable_name='history'), human_message]
template = ChatPromptTemplate(messages=messages)

chain = template | llm | StrOutputParser()

runnables_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

def chat_with_llm(session_id,input):
    for output in runnables_with_history.invoke({'input':input},config={'configurable':{'session_id': session_id}}):
        yield output


prompt = st.chat_input("What\'s up? ")
#st.write(prompt)

if prompt:
    st.session_state.chat_history.append({'role':'user','content':prompt})

    with st.chat_message('user'):
        st.markdown(prompt)

   
    with st.chat_message('assistant'):
        response = st.write_stream(chat_with_llm(user_id,prompt))
    
    st.session_state.chat_history.append({'role':'assistant','content': response})