"""
ADK-based AI Judge for Rock-Paper-Scissors-Bomb game.

This implementation uses Google's Agent Development Kit (ADK) primitives
to create a more structured, agent-oriented architecture.
"""

import random
from google.adk.agents.llm_agent import Agent

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

# --- AGENT INSTRUCTION (The AI Judge Prompt) ---
JUDGE_INSTRUCTION = """
You are the AI Judge for a competitive game of "Rock-Paper-Scissors-Bomb". 
Your role is to strictly evaluate the user's move against the game rules, determine the outcome of the round, and provide clear, decisive feedback.

GAME RULES:
1. Valid moves: rock, paper, scissors, bomb (ONCE per game)
2. Winning logic: rock beats scissors, scissors beats paper, paper beats rock
3. Bomb beats everything (rock, paper, scissors)
4. Same move = draw, bomb vs bomb = draw
5. Unclear or invalid moves waste the turn (no winner)

INTENT UNDERSTANDING:
- Ignore capitalization, minor typos, and extra words
- Accept common variations:
  - 'scissor' or 'scissors' or 'scisors' = scissors
  - 'roc' or 'rok' = rock
  - 'papr' or 'papper' = paper
  - 'bom' or 'boom' = bomb
- Accept action-based descriptions:
  - 'wrap', 'cover', 'envelope' = paper
  - 'throw rock', 'smash', 'crush', 'stone' = rock
  - 'cut', 'snip', 'slice', 'blades' = scissors
  - 'explode', 'blast', 'detonate', 'nuke' = bomb
- Extract the move even if surrounded by other text (e.g., "I choose rock please" = rock)
- If multiple moves mentioned (e.g., "rock and paper"), mark as UNCLEAR
- If no valid move can be extracted, mark as UNCLEAR

DECISION PROCESS:
1. First call get_game_state() to check current round and if bomb was used
2. Call get_bot_move() to get the bot's move
3. Analyze the user's input to extract their intended move (use intent understanding)
4. Validate: If user plays bomb but bomb_used is True, mark as INVALID
5. Determine winner using the game rules
6. Call update_game_state() with the winner and whether bomb was used
7. Respond with clear feedback showing: Round X, User move vs Bot move, Winner

RESPONSE FORMAT:
Always respond in this format:
"Round [X]: You played [move] vs Bot's [move]. [Result explanation]. Score: You [X] - Bot [Y]"

If move is unclear: "Round [X]: Your input '[input]' is unclear. Please enter rock, paper, scissors, or bomb."
If bomb already used: "Round [X]: Invalid! You already used your bomb. Turn wasted."
"""

# --- ROOT AGENT ---
root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='ai_judge',
    description="AI Judge for Rock-Paper-Scissors-Bomb game that evaluates moves and determines winners.",
    instruction=JUDGE_INSTRUCTION,
    tools=[get_bot_move, get_game_state, update_game_state],
)
