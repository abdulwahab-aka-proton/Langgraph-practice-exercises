from langgraph.graph import StateGraph
from langgraph.graph import END
from langchain_core.messages import HumanMessage
from typing import TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="your-model")

class AgentState(TypedDict):
    messages : list[HumanMessage]

def process_node (state: AgentState) -> AgentState:
    response = llm.invoke(
        state["messages"]
    )
    print(f"\n\033[92;1mBot: \033[0m{response.content}")
    return state

workflow = StateGraph(AgentState)
workflow.add_node("process" , process_node)
workflow.set_entry_point("process")
workflow.add_edge("process", END)
app = workflow.compile()

print("----C H A T B O T----\n(Type 'quit' to exit)")
while True:
    user_input = input("\033[93;1mYou: \033[0m")
    if user_input.lower() == "quit":
        break
    result = app.invoke(
        {
            "messages" : [HumanMessage(content=user_input)]
        }
    )




