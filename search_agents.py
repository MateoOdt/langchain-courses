from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from langchain_tavily import TavilySearch
from typing import List
from pydantic import BaseModel, Field

class Source(BaseModel):
    """Schema for a source used by the agent"""
    
    url: str = Field(description="the url of the source")
    
class AgentResponse(BaseModel):
    """Schema for the agent response with answer and sources"""
    
    response: str = Field(description="the agent response to the query")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to generate the response")


load_dotenv()

tavily = TavilyClient()

#custom search tool
#convert regular python func into langchain tool thanks to the decorator @tool : from langchain.tools import tool
@tool
def search(query: str) -> str:
    """"
        Tool that search over internet
        Args: 
            query: The query to search for
        Returns:
            The search result
    """
    print(f"Search for {query}")
    return tavily.search(query=query)

llm = ChatOpenAI(model="gpt-5")

#previously tools = [search] our own tool / using now the tavily search tool
##tools = [TavilySearch()]
tools = [search]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

def main():
    print("test")
    res = agent.invoke({"messages": HumanMessage(content="Je suis en recherche d'emplois. Donne moi 3 vrai annonces d'entreprise qui recrute linkedin des developpeurs fullstack JS react & Node JS avec leurs liens pour postuler")})
    print(res)

if __name__ == "__main__":
    main()
