from langgraph.graph import StateGraph
from langgraph.graph import END
from typing import TypedDict

class AgentState (TypedDict):
    name : str
    values : list [int]
    operation : str
    result : str


def processing_node (state : AgentState) -> AgentState:
    """This node takes user input and generates an output"""
    if state['operation'] == '+':
        ans = sum(state['values'])
    elif state['operation'] == '*':
        r = 1
        for val in state['values']:
            r = r * val
        ans = r
    
    result = f"Hi {state['name']}! Your answer is: {ans}" 

    return {"result" : result}

workflow = StateGraph(AgentState)
workflow.add_node("processor" , processing_node)
workflow.set_entry_point("processor")
workflow.add_edge("processor" , END)
app = workflow.compile()

output = app.invoke(
    {
        "name" : "User",
        "values" : [1,2,3,4],
        "operation" : "+",
        "result" : ""
    }
)

print (f"{output['result']}")

