from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
from langchain.tools import tool, BaseTool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

load_dotenv()

MAX_ITERATIONS: int = 10
MODEL: str = "qwen3:1.7b"

@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog"""
    print(f">>> Execute the get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)

@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price.
    Available tiers are: bronze / silver and gold.
    """
    print(f">>> Execute the apply_discount(price='{price}', discount_tier='{discount_tier}')")
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount: int = discount_percentages.get(discount_tier, 0)
    return round(price * (1 - discount / 100), 2)

@traceable(name="Agent loop")
def run_agent(question: str):
    tools: list[BaseTool] = [get_product_price, apply_discount]
    tools_dict = {t.name: t for t in tools}
    
    llm = init_chat_model(MODEL, model_provider="ollama", temperature=0)
    llm_with_tools = llm.bind_tools(tools=tools)
    print(f"Question: {question}")
    print("=" * 120)
    
    messages = [
        SystemMessage(
            ##General system prompts
            "You are helpfull shopping assistant."
            "You have access to a product catalog tool."
            "and a discount tool"
            "Give the price to the user using the provided tools"
            ##Instructions - Defensive prompts to avoid hallucinations
            "STRICT RULES - you must follow these exactly:"
            "1. NEVER guess or assume any product price."
            "2. You MUST call get_product_price first to get the real price."
            "3. Only call apply_discount AFTER you have received the price from get_product_price. Pass the exact price."
            "4. Always use apply_discount tool."
            "5. If a user doesn't specify a discount tier, ask them which tier to use - do NOT assume one."
        ),
        HumanMessage(content=question),
    ]
    
    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"Iteration {iteration}")
        
        ai_message = llm_with_tools.invoke(messages)
        
        tools_calls = ai_message.tool_calls
        #if no tools_calls -> final anwser
        if not tools_calls:
            print(f"Final Answer: {ai_message.content}")
            return ai_message.content
        
        tool_call = tools_calls[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id")
        
        print(f"Selected tool : name={tool_name} / args={tool_args} / ID={tool_id}")
        
        tool_to_use = tools_dict.get(tool_name)
        if tool_to_use is None: 
            raise ValueError(f"Tool not found")
        
        observation = tool_to_use.invoke(tool_args)
        print(f"Observation: {observation}")
        
        messages.append(ai_message)
        messages.append(ToolMessage(content=str(observation), tool_call_id=tool_id))

    print(f"ERROR Max iterations reached")
    return None

if __name__ == "__main__":
    print("Started")
    res = run_agent("What is the price of a laptop after applying a gold discount ?")