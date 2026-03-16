# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose
This is a number guessing game built with Streamlit. The player picks a difficulty, then tries to guess a randomly chosen secret number within a limited number of attempts. Each guess returns a hint (higher/lower) and updates a running score. The goal is to guess the secret number before running out of attempts.

### Bugs Found

1. **Swapped hint messages** — `check_guess()` returned "Go HIGHER!" when the guess was *above* the secret and "Go LOWER!" when it was *below*. This made the hints actively misleading — following them moved you further from the answer.

2. **New game didn't fully reset state** — Clicking "New Game" only reset `attempts` and `secret`. The fields `status`, `history`, and `score` carried over from the previous game. Because the game loop checks `status` at the top and exits if it's `"won"` or `"lost"`, a completed game would immediately block the new one from starting.

3. **Secret number type toggling** — On even-numbered attempts, the secret was cast to a string before being passed to `check_guess()`. An integer guess could never equal a string secret, so winning on even attempts was impossible regardless of the correct number.

### Fixes Applied

1. Corrected the hint messages in `check_guess()`: guess > secret now returns `"📉 Go LOWER!"` and guess < secret returns `"📈 Go HIGHER!"`.

2. Updated the `new_game` handler to reset all five session state keys — `attempts`, `secret`, `status`, `history`, and `score` — so every new game starts from a clean slate.

3. Diagnosed the type-toggle bug at the point where `secret` is passed to `check_guess()`; the cast to `str` on even attempts was the root cause of unwinnable even-turn rounds.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
