from langgraph.graph import StateGraph
from langgraph.graph import END
from typing import TypedDict

class AgentState (TypedDict):
    num1 : int
    num2 : int
    num3 : int
    num4 : int
    operation1 : str
    operation2 : str
    answer1 : int
    answer2 : int

def add_node(state : AgentState) -> AgentState:
    """This node adds num1 and num2"""
    state['answer1'] = state['num1'] + state['num2']
    return state

def add_node2(state : AgentState) -> AgentState:
    """This node adds num3 and num4"""
    state['answer2'] = state['num3'] + state['num4']
    return state

def sub_node(state : AgentState) -> AgentState:
    """This node subtracts num2 from num1"""
    state['answer1'] = state['num1'] - state['num2']
    return state

def sub_node2(state: AgentState) -> AgentState:
    """This node subtracts num4 from num3"""
    state['answer2'] = state['num3'] - state['num4']
    return state

def router_node1(state: AgentState) -> AgentState:
    """This node decides next node in graph based on operation1"""
    if state['operation1'] == "+":
        return "addition1"
    if state['operation1'] == "-":
        return "subtraction1"
    
def router_node2(state: AgentState) -> AgentState:
    """This node decides next node in graph based on operation2"""
    if state['operation2'] == "+":
        return "addition2"
    if state['operation2'] == "-":
        return "subtraction2"
    

workflow = StateGraph(AgentState)
workflow.add_node("add1", add_node)
workflow.add_node("add2", add_node2)
workflow.add_node("sub1", sub_node)
workflow.add_node("sub2", sub_node2)
workflow.add_node("router1", lambda state:state)
workflow.add_node("router2", lambda state:state)
workflow.set_entry_point("router1")
workflow.add_conditional_edges(
    "router1",
    router_node1,
    {
        "addition1" : "add1",
        "subtraction1" : "sub1"
    }
)
workflow.add_edge("add1", "router2")
workflow.add_edge("sub1", "router2")
workflow.add_conditional_edges(
    "router2",
    router_node2,
    {
        "addition2" : "add2",
        "subtraction2" : "sub2"
    }
)
workflow.add_edge("add2", END)
workflow.add_edge("sub2", END)
app = workflow.compile()

result = app.invoke(
    {
        "num1" : 5,
        "num2" : 10,
        "operation1" : "+",
        "num3" : 10,
        "num4" : 6,
        "operation2" : "-"
    }
)

print(f"Your Answer#1 is: {result['answer1']}\nYour Answer#2 is: {result['answer2']}")
