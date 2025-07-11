from langgraph.graph import StateGraph
from langgraph.graph import END
from typing import TypedDict

class AgentState (TypedDict):
    name : str
    age : int
    skills : list [str]
    final : str


def first_node (state : AgentState) -> AgentState:
    """This node greets user by saying their name"""
    state['final'] = f"Hi {state['name']}, Welcome to the system!"
    return state

def seconde_node (state: AgentState) -> AgentState:
    """This nodes adds user age to the final output"""
    state['final'] = state['final'] + f"You are {state['age']} years old"
    return state

def third_node (state: AgentState) -> AgentState:
    """This node adds user skills to the final output"""
    state['final'] = state['final'] + f"You have skills in: {", ".join(state['skills'])}"
    return state

workflow = StateGraph(AgentState)
workflow.add_node("firstnode", first_node)
workflow.add_node("secondnode", seconde_node)
workflow.add_node("thirdnode", third_node)
workflow.set_entry_point("firstnode")
workflow.add_edge("firstnode", "secondnode")
workflow.add_edge("secondnode", "thirdnode")
workflow.add_edge("thirdnode", END)
app = workflow.compile()

result = app.invoke(
    {
        "name" : "Your-name",
        "age" : 21,
        "skills" : ["Web development" , "Database Development" , "Bot Development"],
        "final" : ""
    }
)

print(f"{result['final']}")
