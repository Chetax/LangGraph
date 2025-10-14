import streamlit as st 
from basic_chatbot import chatbot 
from langchain_core.messages import HumanMessage 

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

for message in  st.session_state['message_history']:
    with st.chat_message(message['user']):
        st.text(message['content'])

user_input=st.chat_input('Type here')

if user_input:
    with st.chat_message('user'):
        st.text(user_input)
        st.session_state['message_history'].append({
            'user':'user',
            'content':user_input
        })

    response=chatbot.invoke({
        'messages':[HumanMessage(content=user_input)]
    }, config={
        'configurable':{'thread_id':'1'}
    })
    res=response['messages'][-1].content
    with st.chat_message('assistant'):
        st.text(res)
        st.session_state['message_history'].append({
            'user':'assistant',
            'content':res
        })
