from langgraph.graph import StateGraph
from langgraph.graph import END
from typing import TypedDict
import random

class AgentState (TypedDict):
    name : str
    target : int
    guess : int
    guesses : list [int]
    attempts : int
    lower_bound : int
    upper_bound : int
    hint : str

def setup_node (state : AgentState) -> AgentState:
    """This node sets up the game by choosing a random number"""
    state['target'] = random.randint(1,20)
    print(f"\nWelcome {state['name']}! Game has started. Guess a number between 1 and 20.\n")
    state['attempts'] = 0
    state['upper_bound'] = 20
    state['lower_bound'] = 1
    state['guesses'] = []
    state['hint'] = ""
    return state


def guess_node(state: AgentState) -> AgentState:
    """This node guesses the number"""
    state['attempts'] += 1
    print(f"This is your {state['attempts']}/7 attempt\n...Guessing...")
    print(f"Range: {state['lower_bound']} - {state['upper_bound']}")
    state['guess'] = random.randint(state['lower_bound'], state['upper_bound'])
    state['guesses'].append(state['guess'])
    print(f"Your current guesses so far are: {state['guesses']}\n")
    return state

def hint_node(state: AgentState) -> AgentState:
    """This node gives a hint based on the guess"""
    if state['guess'] > state['target']:
        state['hint'] = "Lower"
        print(f"Hint: {state['hint']}")
        state['upper_bound'] = state['guess'] - 1
    elif state['guess'] < state['target']:
        state['hint'] = "Higher"
        print(f"Hint: {state['hint']}")
        state['lower_bound'] = state['guess'] + 1
    else:
        state['hint'] = "Congratulations! You guessed the right number"
        print(f"{state['hint']}")
    return state

def should_continue(state: AgentState) -> AgentState:
    """This node decides whether the you should guess again or not"""
    if state['guess'] == state['target']:
        return "exit"
    elif state['attempts'] == 7:
        print("Sorry, you couldn't guess right in 7 attempts")
        return "exit"
    else:
        return "loop"
    
workflow = StateGraph(AgentState)
workflow.add_node("setup", setup_node)
workflow.add_node("guess", guess_node)
workflow.add_node("hint", hint_node)
workflow.set_entry_point("setup")
workflow.add_edge("setup", "guess")
workflow.add_edge("guess", "hint")
workflow.add_conditional_edges(
    "hint",
    should_continue,
    {
        "loop" : "guess",
        "exit" : END
    }
)
app = workflow.compile()

result = app.invoke(
    {
        "name" : "Player"
    }
)



