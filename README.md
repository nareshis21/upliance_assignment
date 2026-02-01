# Rock-Paper-Scissors-Bomb AI Judge

A prompt-driven AI Judge implementation using Google Gemini and Groq that evaluates moves, enforces rules, and determines winners in a Rock-Paper-Scissors-Bomb game.

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Key** (choose one or both):
   
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Run the Game**:
   ```bash
   # Using Gemini (interactive gameplay)
   python google/ai_judge.py
   
   # Using Groq (recommended - faster, better free tier)
   python groq/ai_judge_groq.py
   ```

4. **Run Tests**:
   ```bash
   # RECOMMENDED: Use Groq for testing (30 RPM vs 10 RPM)
   python groq/test_scenarios_groq.py
   
   # Gemini (may hit rate limits on free tier)
   python google/test_scenarios.py
   ```

> ⚠️ **Note on Rate Limits**: Due to Gemini's restrictive free tier limits (10 RPM, 20 RPD), a Groq-based version has been created with significantly better quotas (30 RPM, 14,400 RPD). **Use the Groq version for running tests**. The Google version works great for interactive gameplay.

## 🎮 Example Gameplay

```
Round 1 - Enter your move: rock
>> JUDGE'S DECISION: Rock vs Scissors. Rock crushes scissors! You win!

Round 2 - Enter your move: BOMB!
>> JUDGE'S DECISION: BOMB vs Paper. BOMB obliterates everything! You win!

Round 3 - Enter your move: bomb
>> JUDGE'S DECISION: INVALID. You already used your bomb! Turn wasted.

Round 4 - Enter your move: dragon
>> JUDGE'S DECISION: UNCLEAR. "dragon" is not a valid move. Turn wasted.
```

## 🧠 Design Philosophy

### Prompt-Driven Architecture
The entire game logic resides in `prompts.py` as a system instruction. The Python code is minimal "glue" that:
- Manages state (score, bomb usage)
- Generates random bot moves
- Calls the LLM with context
- Displays results

### Separation of Concerns
- **Intent Understanding**: LLM parses user input to identify intended move
- **Validation**: LLM checks move validity and rule compliance
- **Judgment**: LLM applies game rules to determine winner
- **Response**: LLM generates user-facing explanation

### Why This Approach?
- **Flexibility**: Rule changes only require prompt updates, not code changes
- **Explainability**: LLM provides natural language reasoning for decisions
- **Edge Case Handling**: LLM handles ambiguous inputs better than regex/if-else
- **Maintainability**: Clear separation between logic (prompt) and infrastructure (code)

## 🛡️ Edge Cases Handled

1. **Ambiguous Inputs**: "sword of destiny", emojis, typos → Marked UNCLEAR
2. **Rule Violations**: Using bomb twice → Marked INVALID
3. **Natural Language**: "I pick paper please" → Extracts "paper"
4. **Multiple Moves**: "rock and paper" → Marked UNCLEAR (ambiguous)
5. **State Tracking**: Bomb usage persists across rounds via explicit state injection

## 📁 Project Structure

```
upliance_assignment/
├── google/
│   ├── ai_judge.py          # Main game (Gemini direct API)
│   └── test_scenarios.py    # 15 test cases (Gemini)
├── groq/
│   ├── ai_judge_groq.py     # Main game (Groq/Llama)
│   └── test_scenarios_groq.py # 15 test cases (Groq)
├── adk_agent/
│   ├── agent.py             # ADK-based AI Judge (uses ADK primitives)
│   ├── .env.example         # API key template
│   └── __init__.py
├── prompts.py               # System instruction (the "brain")
├── requirements.txt         # Dependencies
├── .env                     # API keys (create this)
└── README.md               # This file
```

## 🤖 ADK Implementation

An additional implementation using **Google Agent Development Kit (ADK)** primitives is provided in `adk_agent/`. This demonstrates:

- **Agent-oriented architecture** using `google.adk.agents.llm_agent.Agent`
- **Tool-based design** with separate functions for:
  - `get_bot_move()` - Generates random bot move
  - `get_game_state()` - Returns current round, scores, bomb status
  - `update_game_state()` - Updates state after judgment
- **Structured agent definition** with model, name, description, instruction, and tools

**Run with ADK CLI:**
```bash
pip install google-adk
adk run adk_agent
# Or use web interface:
adk web --port 8000
```

## 🧪 Test Scenarios

The test suite is divided into two sections:

### Section 1: Deterministic Tests
1. Standard win (rock vs scissors)
2. Ambiguous input (nonsense text)
3. Valid bomb usage
4. Invalid bomb (second attempt)
5. Natural language extraction
6. Multiple moves (ambiguous)

### Section 2: Reddit-Style Chaos Testing
The system was stress-tested using Reddit-style natural language inputs, including sarcasm, emojis, indecision, and pop-culture references to evaluate robustness of intent understanding.

7. Reddit - Overexplainer ("ok hear me out… rock 🪨")
8. Reddit - Meme Brain ("bruh", "💀💀💀")
9. Reddit - Bomb Drama ("BOMB TIME 💣")
10. Reddit - Cheating Attempt (bomb after already used)
11. Reddit - Indecisive ("rock but maybe paper actually")
12. Reddit - Emoji Chaos ("scissors. snip snip ✂️")

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

### JSON Output Structure
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
✅ **Minimal Code**: ~140 lines of glue code per implementation, all logic in prompt  
✅ **ADK Primitives**: `adk_agent/` uses Agent, tools, and structured definitions  

## 🔧 API Comparison

| Feature | Gemini 2.5 Flash Lite | Groq (Llama 3.3 70B) |
|---------|----------------------|---------------------|
| Free Tier RPM | 10 | 30 |
| Free Tier RPD | 20 | 14,400 |
| Speed | Fast | Very Fast |
| Quality | Excellent | Excellent |
| System Instructions | ✅ Native | ✅ Via messages |

## 🚀 Future Enhancements

- Web UI for better accessibility
- Persistent leaderboards (database)
- Adaptive bot strategy (pattern detection)
- Voice interface (TTS/STT)
