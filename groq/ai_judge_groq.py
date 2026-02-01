import os
import sys
import random
import json
import time
from groq import Groq
from dotenv import load_dotenv

# Add parent directory to path to import prompts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts import SYSTEM_INSTRUCTION

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY") 
if not API_KEY:
    print("WARNING: GROQ_API_KEY environment variable not set.")
    print("Please set it in your .env file.")

# --- STATE MANAGEMENT ---
class GameState:
    def __init__(self):
        self.round_num = 1
        self.user_score = 0
        self.bot_score = 0
        self.bomb_used = False
        self.history = []

    def update(self, winner, bomb_played):
        if winner == 'user':
            self.user_score += 1
        elif winner == 'bot':
            self.bot_score += 1
        
        if bomb_played:
            self.bomb_used = True
        
        self.round_num += 1

# --- GLUE CODE ---
def get_bot_move():
    """Generate bot's move using random selection.
    
    Rationale: Random selection ensures fairness and unpredictability.
    The AI Judge evaluates user input against this pre-determined bot move,
    maintaining separation between move generation and judgment logic.
    """
    moves = ['rock', 'paper', 'scissors']
    return random.choice(moves)

def play_round(state, user_input, client):
    bot_move = get_bot_move()
    
    # Construct the prompt payload
    prompt_payload = f"""
    Current Game State:
    - Round: {state.round_num}
    - User Bomb Used Previously: {state.bomb_used}
    - Bot's Hidden Move: {bot_move}
    
    User Input: "{user_input}"
    """

    max_retries = 3
    base_delay = 2

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_INSTRUCTION},
                    {"role": "user", "content": prompt_payload}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            # Parse JSON response
            text_response = response.choices[0].message.content.strip()
            decision = json.loads(text_response)
            
            # Extract Logic
            analysis = decision.get("outcome_analysis", {})
            winner = analysis.get("winner")
            bomb_action = analysis.get("bomb_used_this_turn", False)
            
            # Display Result
            print("\n" + "="*40)
            print(f">> JUDGE'S DECISION (Round {state.round_num})")
            print(decision.get("display_message"))
            print("="*40 + "\n")
            
            # Update State
            state.update(winner, bomb_action)
            return

        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print(f"Rate limit hit. Retrying in {base_delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(base_delay)
                base_delay *= 2
            else:
                print(f"Error calling AI Judge: {e}")
                return
    print("Unable to get decision after retries.")

def main():
    print("Initializing AI Judge (Groq)...")
    
    if not API_KEY:
        print("Cannot start: API Key missing.")
        return

    # Initialize Client
    client = Groq(api_key=API_KEY)
    
    state = GameState()
    
    print("\n--- WELCOME TO ROCK-PAPER-SCISSORS-BOMB ---")
    print("Rules: Standard RPS. Bomb beats all (Use only ONCE).")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input(f"Round {state.round_num} - Enter your move: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'end', 'stop', 'done']:
                print("Exiting game.")
                print(f"Final Score -> You: {state.user_score} | Bot: {state.bot_score}")
                break
            
            if not user_input:
                continue

            play_round(state, user_input, client)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
