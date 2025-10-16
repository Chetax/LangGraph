from langgraph.graph import StateGraph,START,END
from typing import TypedDict ,Literal,Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage,HumanMessage ,SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

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
    
checkpointer=MemorySaver()
graph=StateGraph(ChatState)


#add node 
graph.add_node('chat_node',chat_node)


graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)




