from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

load_dotenv()

def main():
    info = """
        Emmanuel Macron, né le 21 décembre 1977 à Amiens, est un homme d'État français. Il est le président de la République française depuis le 14 mai 2017. Sorti de l'École nationale d'administration en 2004, il devient inspecteur des finances.
    """
    
    sum_template = """
        based on the informations {info} about a person I want you to create : 
        1. A short story
        2. Two interesting facts about that person.
    """
    
    summary_prompt_template = PromptTemplate(input_variables=["info"], template=sum_template)
    
    llm = ChatOpenAI(temperature=0.5, model="gpt-5")
    
    #use local llm installed 
    #llm = ChatOllama(temperature=0.5, model="gemma3:270m")
    
    ## runnable chain -> will connect the output of summary_prompt_template to give it to the LLM
    chain = summary_prompt_template | llm 
    response = chain.invoke(input={"info": info})
    print(response)

if __name__ == "__main__":
    main() 