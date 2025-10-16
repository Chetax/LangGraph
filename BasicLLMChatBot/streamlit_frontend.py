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
    # without streaming
    # response=chatbot.invoke({
    #     'messages':[HumanMessage(content=user_input)]
    # }, config={
    #     'configurable':{'thread_id':'1'}
    # })
    # res=response['messages'][-1].content
    with st.chat_message('assistant'):
    #     st.text(res)
    #     st.session_state['message_history'].append({
    #         'user':'assistant',
    #         'content':res
    #     })

    #with streaming 
        ai_message=st.write_stream(
        message_chunk.content for message_chunk,metadata in chatbot.stream(  
                {'messages':[HumanMessage(content=user_input)]},
                config= {'configurable':{'thread_id':'1'} },
                stream_mode='messages')
           )
        st.session_state['message_history'].append({
            'user':'assistant',
            'content':ai_message
        })
