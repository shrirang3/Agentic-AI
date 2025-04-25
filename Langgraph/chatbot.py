#tools
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper

from dotenv import load_dotenv
import os
load_dotenv()


api_wrapper_arxiv=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
arxiv=ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Query Arxiv papers")
def arxiv_search(query: str) -> str:
    """Searches arXiv for the given query."""
    res=arxiv.invoke(query)
    return res

#print(arxiv_search("Attention is all you need")) # Example usage

api_wrapper_wikipedia=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
wikipedia=WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia, description="Query Wikipedia")

def wikipidea_search(query: str) -> str:
    """Searches Wikipedia for the given query."""
    res=wikipedia.invoke(query)
    return res

#print(wikipidea_search("Who is Pedri Gonzalez?")) # Example usage


#My tools
from langchain_community.tools.tavily_search import TavilySearchResults

os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY") #My tool 3 for news search

tavily=TavilySearchResults()
def news_search(query: str) -> str:
    """Searches news for the given query."""
    res=tavily.invoke(query)
    return res

#print(news_search("Latest Fc barcelona news")) # Example usage

#-------------------------------------- Tools Defined--------------------------------------

tools=[arxiv, wikipedia, tavily]

#Initializa LLM
from langchain_groq import ChatGroq

llm=ChatGroq(model="qwen-qwq-32b")
def llm_invoke(query: str) -> str:
    res=llm.invoke(query)
    return res

llm_with_tools=llm.bind_tools(tools=tools) #bind tools to LLM

#----------------------------------------- Models Loaded-------------------------------------

## State Schema
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage ##human message or AI message
from typing import Annotated
from langgraph.graph.message import add_messages ## appends messages in variable



from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition ##conditions on which path to take when using/not using a tool

class State(TypedDict):
    messages:Annotated[list[AnyMessage], add_messages]

##Node definition
def tool_calling_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]}

#Build Graph
builder=StateGraph(State)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode(tools))

#Edges
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges("tool_calling_llm",
                              #If the latest message(result) from assistant is a tool call=>tool_condition routes to tools
                              #If latest message(result) from assistant is not a tool=>tool_consition rotes to END
                              tools_condition,
                              )

builder.add_edge("tools", END)

graph=builder.compile()

def graph_invoke(message:str)->str:
    messages=graph.invoke({"messages":message})
    return messages

# messages=graph_invoke("Hi....Address me as Pedri!!")
# for m in messages['messages']:
#     m.pretty_print()
