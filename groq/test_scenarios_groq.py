import os
import json
import time
import random
from groq import Groq
from dotenv import load_dotenv
from prompts import SYSTEM_INSTRUCTION

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# --- REDDIT-STYLE INPUT GENERATOR ---
def generate_reddit_user_input(intent=None):
    """
    Simulates chaotic, Reddit-style human inputs for stress testing.
    intent can be: rock | paper | scissors | bomb | ambiguous | multiple
    """
    templates = {
        "rock": [
            "ok hear me out… rock 🪨",
            "ROCK. Final answer.",
            "i guess rock? unless that's dumb",
            "throwing rock like a caveman",
            "rock because vibes",
            "not paper, not scissors — rock"
        ],
        "paper": [
            "paper (don't ask why)",
            "i pick paper, obviously",
            "paper beats rock right? whatever paper",
            "choosing paper like a coward",
            "paper 📄"
        ],
        "scissors": [
            "scissors. snip snip ✂️",
            "i go scissors bc risky",
            "SCISSORS!!!",
            "cutting things. scissors.",
            "scissors gang rise up"
        ],
        "bomb": [
            "fine. bomb.",
            "BOMB TIME 💣",
            "i use the bomb don't hate me",
            "dropping the bomb now",
            "bomb because chaos"
        ],
        "ambiguous": [
            "idk man surprise me",
            "this game is rigged",
            "rock paper scissor bomb gun dragon",
            "💀💀💀",
            "bruh",
            "only real ones know what im choosing",
            "i plead the fifth",
            "my lawyer advised me not to answer"
        ],
        "popculture": [
            "I choose OMNI MAN. Think Mark, THINK!",
            "ONE PUUUUNCH - Saitama mode activated",
            "Salman bhai aayenge toh truck se aayenge",
            "DBoss style. Enri media",
            "I am inevitable - Thanos snap",
            "This is Sparta! *kicks*",
            "Ek tha tiger. Rock.",
            "Pushpa. Flower nahi, fire."
        ],
        "multiple": [
            "rock but maybe paper actually",
            "scissors… no rock… wait paper",
            "rock paper scissors shoot",
            "i choose all of them"
        ]
    }

    if intent in templates:
        return random.choice(templates[intent])
    
    return random.choice(templates["ambiguous"])

def run_test_scenario(scenario_name, user_input, bot_move, bomb_already_used, client):
    print(f"\n--- Testing Scenario: {scenario_name} ---")
    print(f"Input: '{user_input}' | Bot: {bot_move} | Bomb Used: {bomb_already_used}")
    
    prompt_payload = f"""
    Current Game State:
    - Round: 1
    - User Bomb Used Previously: {bomb_already_used}
    - Bot's Hidden Move: {bot_move}
    
    User Input: "{user_input}"
    """
    
    max_retries = 3
    base_delay = 5

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
            
            text = response.choices[0].message.content.strip()
            data = json.loads(text)
            
            analysis = data.get("outcome_analysis", {})
            print(f"Round: {data.get('round_number')} | User: {data.get('user_move')} | Bot: {data.get('bot_move')}")
            print(f"Result: Status={analysis.get('status')} | Winner={analysis.get('winner')} | Reason={analysis.get('reason')}")
            print(f"Message: {data.get('display_message')}")
            return data

        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                print(f"Rate limit hit. Retrying in {base_delay}s... (Attempt {attempt+1}/{max_retries})")
                time.sleep(base_delay)
                base_delay *= 2
            else:
                print(f"Error: {e}")
                return None
    print("Failed after max retries.")
    return None

def main():
    if not API_KEY:
        print("Skipping tests: No GROQ_API_KEY in .env or environment.")
        return

    client = Groq(api_key=API_KEY)

    print("\n" + "="*60)
    print("SECTION 1: STANDARD DETERMINISTIC TESTS")
    print("="*60)

    # 1. Standard Win
    run_test_scenario("Standard Rock vs Scissors", "rock", "scissors", False, client)
    time.sleep(1)
    
    # 2. Ambiguous Input - Nonsense
    run_test_scenario("Ambiguous/Unclear", "I choose the sword of destiny", "paper", False, client)
    time.sleep(1)

    # 3. Bomb Usage (Valid)
    run_test_scenario("Valid Bomb usage", "BOMB!", "rock", False, client)
    time.sleep(1)

    # 4. Bomb Usage (Invalid - Already used)
    run_test_scenario("Invalid Bomb (Second time)", "bomb", "paper", True, client)
    time.sleep(1)

    # 5. Natural Language with Valid Move
    run_test_scenario("Natural Language - Paper", "I pick paper please", "rock", False, client)
    time.sleep(1)

    # 6. Multiple Moves (Ambiguous)
    run_test_scenario("Multiple Moves", "rock and paper", "scissors", False, client)
    time.sleep(1)

    print("\n" + "="*60)
    print("SECTION 2: REDDIT-STYLE CHAOS TESTING")
    print("(Stress testing with realistic human inputs)")
    print("="*60)

    # 7. Reddit - Overexplainer with Rock Intent
    run_test_scenario("Reddit - Overexplainer", generate_reddit_user_input("rock"), "scissors", False, client)
    time.sleep(1)

    # 8. Reddit - Meme Brain (Ambiguous)
    run_test_scenario("Reddit - Meme Brain", generate_reddit_user_input("ambiguous"), "paper", False, client)
    time.sleep(1)

    # 9. Reddit - Bomb Drama
    run_test_scenario("Reddit - Bomb Drama", generate_reddit_user_input("bomb"), "rock", False, client)
    time.sleep(1)

    # 10. Reddit - Cheating Attempt (Bomb already used)
    run_test_scenario("Reddit - Cheating Attempt", generate_reddit_user_input("bomb"), "scissors", True, client)
    time.sleep(1)

    # 11. Reddit - Indecisive (Multiple moves)
    run_test_scenario("Reddit - Indecisive", generate_reddit_user_input("multiple"), "paper", False, client)
    time.sleep(1)

    # 12. Reddit - Scissors with Emoji
    run_test_scenario("Reddit - Emoji Chaos", generate_reddit_user_input("scissors"), "rock", False, client)
    time.sleep(1)

    print("\n" + "="*60)
    print("SECTION 3: POP CULTURE REFERENCE TESTING")
    print("(Testing with movie/anime references users might type)")
    print("="*60)

    # 13. Pop Culture - Omni Man
    run_test_scenario("Pop Culture - Omni Man", generate_reddit_user_input("popculture"), "scissors", False, client)
    time.sleep(1)

    # 14. Pop Culture - Random
    run_test_scenario("Pop Culture - Random", generate_reddit_user_input("popculture"), "rock", False, client)
    time.sleep(1)

    # 15. Pop Culture - Another
    run_test_scenario("Pop Culture - Desi Cinema", generate_reddit_user_input("popculture"), "paper", False, client)

    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
