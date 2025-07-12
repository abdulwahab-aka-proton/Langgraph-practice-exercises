from langgraph.graph import StateGraph
from langgraph.graph import END
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List, Union
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="your-model")

class AgentState(TypedDict):
    messages : List[Union[HumanMessage, AIMessage]]

def process_node (state: AgentState) -> AgentState:
    """This node processes user query"""
    response = llm.invoke(
        state["messages"]
    )
    state["messages"].append(AIMessage(content=response.content))
    print(f"\n\033[92;1mBot: \033[0m{response.content}")
    return state

workflow = StateGraph(AgentState)
workflow.add_node("process" , process_node)
workflow.set_entry_point("process")
workflow.add_edge("process", END)
app = workflow.compile()

conversation_history = []

print("----C H A T B O T----\n(Type 'quit' to exit)")
while True:
    user_input = input("\033[93;1mYou: \033[0m")
    conversation_history.append(HumanMessage(content=user_input))
    if user_input.lower() == "quit":
        break
    result = app.invoke(
        {
            "messages" : conversation_history
        }
    )
    conversation_history = result["messages"]

with open("convo_log.txt" , "w") as file:
    file.write("Your Conversation log: \n\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"Bot: {message.content}\n\n")
    file.write("END OF CONVERSATION")

print("Converation saved to convo_log.txt")

        
