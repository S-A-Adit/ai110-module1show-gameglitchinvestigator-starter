# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- It says go higher when it is supposed to go lower for the guessed number.
- negative score
- New game does not erase old game.
- Range of 1 to 100 is not being maintained
- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) as my AI pair-programmer throughout this project.

**Correct AI suggestion — new game state reset:**
Claude Code read `app.py` and correctly identified that the `new_game` button handler only reset `attempts` and `secret`, leaving `status`, `history`, and `score` untouched. It pointed directly to the guard at line 146 (`if st.session_state.status != "playing"`) as the place where stale `"won"` or `"lost"` status would block the new game immediately on rerun. I verified this by winning a round, clicking New Game, and confirming the "You already won" message still appeared — exactly matching Claude's diagnosis. After applying the fix, the new game loaded cleanly.

**Incorrect/misleading AI suggestion — FIXME comment left in place:**
Claude Code added the `FIXME` comment in the `new_game` block but initially did NOT apply the actual state resets (`status`, `history`, `score`) in that same edit — it described the bug without fixing it yet. This was misleading because the comment made the code look annotated-but-broken, and I had to explicitly ask for the real fix to be written. I verified the issue was unresolved by checking that `st.session_state.status` was still not being reset after the first edit.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only after both a manual UI test and a passing pytest confirmed the same behavior.

For the new-game bug, I ran two pytest cases in `tests/test_game_logic.py`: `test_new_game_resets_status_after_win` and `test_new_game_resets_all_fields`. These simulate session state as a plain dict and call a `simulate_new_game` helper that mirrors the corrected reset logic. Both tests passed once the fix was applied, confirming all five session state keys (`attempts`, `secret`, `status`, `history`, `score`) returned to their initial values. I also tested manually by winning a game, clicking New Game, and verifying the guess input and attempt counter were both fresh.

For the swapped hint messages, I ran `test_too_high_message_says_go_lower` and `test_too_low_message_says_go_higher` — those tests caught the incorrect strings before I even touched the game in the browser.

Claude Code helped design the new-game regression tests by explaining that Streamlit session state can't be imported in a plain pytest context, so it suggested wrapping the reset logic in a helper that accepts a plain dict — making the test portable with no Streamlit dependency.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
