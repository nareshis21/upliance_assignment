# Rock-Paper-Scissors-Bomb AI Judge

A prompt-driven AI Judge implementation that evaluates moves, enforces rules, and determines winners in a Rock-Paper-Scissors-Bomb game.

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Keys**:
   
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Run the Game**:
   ```bash
   # CLI version with Groq (recommended - better rate limits)
   python groq/ai_judge_groq.py
   
   # ADK CLI (natural conversation)
   adk run adk_agent
   
   # ADK Web interface (browser-based)
   adk web --port 8000
   # Then open http://localhost:8000
   ```

4. **Run Tests**:
   ```bash
   python groq/test_scenarios_groq.py
   ```

## 🎮 Example Gameplay

```
Round 1 - Enter your move: rock
>> JUDGE'S DECISION: Round 1: You played rock vs bot's scissors. Rock beats scissors, so you win!

Round 2 - Enter your move: wrap you up like a shawarma
>> JUDGE'S DECISION: Round 2: You played paper vs bot's rock. Paper beats rock, so you win!

Round 3 - Enter your move: BOMB!
>> JUDGE'S DECISION: Round 3: You played bomb vs bot's paper. Bomb beats everything! You win!

Round 4 - Enter your move: bomb
>> JUDGE'S DECISION: Invalid! You already used your bomb. Turn wasted.
```

## 🧠 Design Philosophy

### Prompt-Driven Architecture
The entire game logic resides in the `SYSTEM_INSTRUCTION` prompt (not Python code). The Python code is minimal "glue" that:
- Manages state (score, bomb usage)
- Generates random bot moves
- Calls the LLM with context
- Displays results

### Why Two Implementations?

| Implementation | Purpose | Key Feature |
|----------------|---------|-------------|
| **Groq** (`groq/`) | Testing & Development | **30 RPM** free tier - enables comprehensive test suite |
| **ADK** (`adk_agent/`) | Production & ADK Demo | Demonstrates ADK primitives, conversational interface |

**Why Groq for Testing?**

Groq's significantly higher rate limits (30 RPM vs Gemini's 10 RPM) make it ideal for:
- Running the full 15-scenario test suite without rate-limit errors
- Rapid iteration during development
- Demonstrating the AI Judge's robustness across edge cases

The ADK implementation uses Gemini (as required by ADK) and focuses on demonstrating Google's agent framework primitives.

### Separation of Concerns
- **Intent Understanding**: LLM parses user input to identify intended move
- **Validation**: LLM checks move validity and rule compliance
- **Judgment**: LLM applies game rules to determine winner
- **Response**: LLM generates user-facing explanation

### Why This Approach?
- **Flexibility**: Rule changes only require prompt updates, not code changes
- **Explainability**: LLM provides natural language reasoning for decisions
- **Edge Case Handling**: LLM handles ambiguous inputs better than regex/if-else
- **No Hardcoded Logic**: All game rules live in the prompt

## 📁 Project Structure

```
upliance_assignment/
├── groq/
│   ├── ai_judge_groq.py     # Main game (Groq/Llama)
│   ├── test_scenarios_groq.py # 15 test cases
│   └── prompts.py            # System instruction (JSON output)
├── adk_agent/
│   ├── agent.py              # ADK-based AI Judge
│   ├── prompts.py            # System instruction (natural language)
│   ├── .env.example          # API key template
│   └── __init__.py
├── requirements.txt          # Dependencies
├── .env                      # API keys (create this)
├── .gitignore
└── README.md                 # This file
```

## 🔑 Why Separate Prompts?

- **Groq** (`groq/prompts.py`): Returns structured JSON for programmatic parsing
- **ADK** (`adk_agent/prompts.py`): Returns natural language for conversational UI

Both share the same core logic, just different output formats.

## 🧪 Test Scenarios

The test suite includes 15 scenarios divided into 3 sections:

### Section 1: Deterministic Tests
1. Standard win (rock vs scissors)
2. Ambiguous input (nonsense text)
3. Valid bomb usage
4. Invalid bomb (second attempt)
5. Natural language extraction
6. Multiple moves (ambiguous)

### Section 2: Reddit-Style Chaos Testing
The system was stress-tested using Reddit-style natural language inputs:

7. Reddit - Overexplainer ("ok hear me out… rock 🪨")
8. Reddit - Meme Brain ("bruh", "💀💀💀")
9. Reddit - Bomb Drama ("BOMB TIME 💣")
10. Reddit - Cheating Attempt (bomb after already used)
11. Reddit - Indecisive ("rock but maybe paper actually")
12. Reddit - Emoji Chaos ("scissors. snip snip ✂️")

### Section 3: Pop Culture Reference Testing
Testing with movie/anime references users might type:

13. Pop Culture - Omni Man ("Think Mark, THINK!")
14. Pop Culture - Saitama ("ONE PUUUUNCH")
15. Pop Culture - Desi Cinema ("Pushpa. Flower nahi, fire.")

This demonstrates:
- Edge-case awareness
- Natural language robustness
- Real-world product thinking
- Confidence in the judge prompt

## 🔮 Implementation Notes

### Bot Move Generation
Bot moves are randomly selected before LLM evaluation. This ensures:
- Fair, unpredictable gameplay
- Clear separation: move generation ≠ judgment
- Consistent state for LLM evaluation

### JSON Output Structure (Groq)
```json
{
  "round_number": 1,
  "user_move": "rock",
  "bot_move": "scissors",
  "outcome_analysis": {
    "intent": "rock",
    "status": "VALID",
    "reason": "Valid move identified",
    "bomb_used_this_turn": false,
    "winner": "user"
  },
  "display_message": "Round 1: Rock vs Scissors. You win!"
}
```

### State Management
- Minimal state: round number, scores, bomb usage
- State injected into each LLM call as context
- Prevents LLM "forgetting" across rounds

## 📝 Assignment Alignment

✅ **Prompt Quality**: Clear instructions, explicit roles, structured output  
✅ **Instruction Design**: Rules in prompt, not hardcoded logic  
✅ **Edge-Case Handling**: 15 test scenarios covering ambiguity, pop culture, and violations  
✅ **Explainability**: JSON separates internal logic from user messages  
✅ **Minimal Code**: ~140 lines of glue code, all logic in prompt  
✅ **ADK Primitives**: `adk_agent/` uses Agent, tools, and structured definitions  

## 🔧 API Comparison

| Feature | Groq (Llama 3.3 70B) | Gemini 2.5 Flash Lite (ADK) |
|---------|---------------------|----------------------------|
| Free Tier RPM | 30 | 10 |
| Free Tier RPD | 14,400 | 20 |
| Speed | Very Fast | Fast |
| Quality | Excellent | Excellent |
| Output Format | JSON | Natural Language |
| Use Case | CLI game | Conversational UI |

## 🚀 Future Enhancements

- Web UI for better accessibility
- Persistent leaderboards (database)
- Adaptive bot strategy (pattern detection)
- Voice interface (TTS/STT)
- Multi-player support
