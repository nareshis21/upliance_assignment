import os
import random
from google.adk.agents.llm_agent import Agent
from prompts import SYSTEM_INSTRUCTION

# --- GAME STATE (stored externally, passed to tools) ---
game_state = {
    "round_num": 1,
    "user_score": 0,
    "bot_score": 0,
    "bomb_used": False
}

# --- TOOLS ---
def get_bot_move() -> dict:
    """
    Generates the bot's move for the current round.
    
    Returns:
        dict: Contains the bot's randomly selected move (rock, paper, or scissors).
    """
    moves = ['rock', 'paper', 'scissors']
    bot_move = random.choice(moves)
    return {
        "status": "success",
        "bot_move": bot_move
    }

def get_game_state() -> dict:
    """
    Retrieves the current game state including round number and bomb usage.
    
    Returns:
        dict: Current game state with round number, scores, and bomb availability.
    """
    return {
        "status": "success",
        "round_number": game_state["round_num"],
        "user_score": game_state["user_score"],
        "bot_score": game_state["bot_score"],
        "bomb_used": game_state["bomb_used"]
    }

def update_game_state(winner: str, bomb_used_this_turn: bool) -> dict:
    """
    Updates the game state after a round is judged.
    
    Args:
        winner: The winner of the round ('user', 'bot', 'draw', or 'none').
        bomb_used_this_turn: Whether the user played bomb this turn.
    
    Returns:
        dict: Confirmation of state update.
    """
    global game_state
    
    if winner == 'user':
        game_state["user_score"] += 1
    elif winner == 'bot':
        game_state["bot_score"] += 1
    
    if bomb_used_this_turn:
        game_state["bomb_used"] = True
    
    game_state["round_num"] += 1
    
    return {
        "status": "success",
        "message": "Game state updated",
        "new_state": game_state
    }

# --- ROOT AGENT ---
root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='ai_judge',
    description="AI Judge for Rock-Paper-Scissors-Bomb game that evaluates moves and determines winners.",
    instruction=SYSTEM_INSTRUCTION,
    tools=[get_bot_move, get_game_state, update_game_state],
)

