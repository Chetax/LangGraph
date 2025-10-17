from langgraph.graph import StateGraph,START,END
from typing import TypedDict ,Literal,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage,HumanMessage ,SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
load_dotenv()
llm=ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-lite'
)


class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):

    #take user message 
    message=state['messages']
    # send to llm
    res=llm.invoke(message)

    return {
        'messages':[res]
    }
    
# checkpointer=MemorySaver() # it is for inmemory stoare(RAM)
conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)
graph=StateGraph(ChatState)


#add node 
graph.add_node('chat_node',chat_node)


graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)

# In chatbot_backend.py

def get_all_threads():
    all_thread_ids = set()
    # 1. Collect all unique thread IDs (strings)
    for chekpoint in checkpointer.list(None):
        all_thread_ids.add(chekpoint.config['configurable']['thread_id'])
    
    # 2. Convert the set of IDs into the required list of dictionaries
    #    Use a generic content, as the timestamp info is not available here
    thread_list = []
    for thread_id in sorted(list(all_thread_ids)): # Sorting is nice for consistent display
        thread_list.append({'thread': thread_id, 'content': f'Existing Chat: {thread_id[:4]}...'})
        
    return thread_list # This now returns a list of dictionaries, e.g., [{'thread': '...', 'content': '...'}]

