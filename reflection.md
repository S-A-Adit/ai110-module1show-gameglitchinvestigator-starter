# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, the hints were completely backwards — if my guess was too high, the game told me to go higher, which sent me in the wrong direction every time. Starting a new game after winning or losing didn't work either; the old game state was still there, so the game immediately showed "You already won" or "Game over" without letting me play again. The score could also go negative, and on certain attempts the game seemed impossible to win because the secret number was being compared as a string instead of an integer.

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

The secret number kept changing because Streamlit reruns the entire Python script from top to bottom every time a user interacts with anything — clicking a button, typing in a field, anything. Without session state, `random.randint()` was called fresh on each rerun, picking a new number every time. It was like the game forgot what it had just decided.

I would explain Streamlit reruns to a friend like this: imagine every button click causes the whole program to restart from line one. Normal Python variables get reset each restart. `st.session_state` is a special dictionary that survives across those restarts — it's the game's memory.

The fix was wrapping the initial `random.randint()` call in a guard: `if "secret" not in st.session_state`. That way, a new secret is only generated the very first time the app loads, and every subsequent rerun just reads the already-stored value.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is writing regression tests the moment I fix a bug — not after. In this project, the tests for the swapped hints and the incomplete new-game reset forced me to clearly define what "fixed" meant before I could move on, which kept me from leaving half-done fixes in place.

Next time I work with AI on a coding task I would ask it to show me the actual changed lines immediately, not just describe the fix in a comment. In this project, Claude added a `FIXME` comment explaining the bug without writing the corrected code in the same step, which made the code look annotated-and-done when it wasn't.

This project changed how I read AI-generated code: I now treat it as a first draft that needs review, not a finished solution. The AI was right about diagnosing the bugs, but it still shipped code with wrong hint messages and incomplete state resets — things that only became obvious when the tests ran.
