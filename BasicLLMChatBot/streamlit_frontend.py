import streamlit as st 
from basic_chatbot import chatbot 
from langchain_core.messages import HumanMessage 
import uuid
from datetime import datetime

def generate_random_thread_id():
      thread_id=uuid.uuid4()
      return str(thread_id)

def clear_message_history():
    st.session_state['thread_id']=generate_random_thread_id()
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    existing_threads = [t['thread'] for t in st.session_state['chat_thread']]
    if thread_id not in existing_threads:
        st.session_state['chat_thread'].append({'thread':thread_id,'content':f'New chat at {datetime.now().strftime("%H:%M:%S")}'})


def load_chat_history(threadId):
    return chatbot.get_state(config={'configurable':{'thread_id':threadId} }).values['messages']


if 'message_history' not in st.session_state:
     st.session_state['message_history']=[]
if  'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_random_thread_id()


add_thread(st.session_state['thread_id'])
# -------------------- Side bar ui----------
st.sidebar.title('LangGraph Chatbot')
new_chat=st.sidebar.button('New Chat')
st.sidebar.markdown('--------')
st.header('My Conversations')
for threads in st.session_state['chat_thread']:
    thread=threads['thread']
    content=threads['content']
    if st.sidebar.button(content):
        st.session_state['thread_id']=thread
        messages=load_chat_history(thread)
        temp_messages=[]
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content': message.content})

        st.session_state['message_history']=temp_messages
        


if new_chat:
    clear_message_history()




for message in  st.session_state['message_history']:
    with st.chat_message(message['role']):
         st.text(message['content'])

user_input=st.chat_input('Type here')

if user_input:
    with st.chat_message('user'):
        st.text(user_input)
        st.session_state['message_history'].append({
            'role':'user',
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
                config= {'configurable':{'thread_id':st.session_state['thread_id']} },
                stream_mode='messages')
           )
        st.session_state['message_history'].append({
            'role':'assistant',
            'content':ai_message
        })
