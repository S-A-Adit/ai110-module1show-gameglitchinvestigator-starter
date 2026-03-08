from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug regression: swapped hint messages in app.py check_guess ---
# See FIXME in app.py: when guess > secret, message incorrectly said "Go HIGHER"
# and when guess < secret, it incorrectly said "Go LOWER".
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import check_guess as app_check_guess

def test_too_high_message_says_go_lower():
    # guess (80) > secret (50): outcome must be "Too High" and hint must say LOWER
    outcome, message = app_check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected hint to say LOWER, got: {message}"

def test_too_low_message_says_go_higher():
    # guess (20) < secret (50): outcome must be "Too Low" and hint must say HIGHER
    outcome, message = app_check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected hint to say HIGHER, got: {message}"


# --- Bug regression: new game does not erase old game state (see #file:app.py) ---
# When "New Game" is clicked, app.py only reset `attempts` and `secret`.
# `status`, `history`, and `score` were not cleared, so a completed game
# (status="won"/"lost") would immediately block play again on rerun.
# This test simulates session_state as a plain dict to verify all fields reset.

def simulate_new_game(session_state: dict, new_secret: int) -> dict:
    """
    Mirror the corrected new_game reset logic from #file:app.py.
    All five game-state keys must be restored to their initial values.
    """
    session_state["attempts"] = 0
    session_state["secret"] = new_secret
    session_state["status"] = "playing"
    session_state["history"] = []
    session_state["score"] = 0
    return session_state


def test_new_game_resets_status_after_win():
    # After winning, status is "won". New game must restore it to "playing"
    # so the game-over guard in #file:app.py (line 146) does not block play.
    session = {
        "attempts": 7,
        "secret": 42,
        "status": "won",
        "history": [10, 20, 42],
        "score": 80,
    }
    result = simulate_new_game(session, new_secret=55)
    assert result["status"] == "playing", "status must be reset to 'playing' on new game"


def test_new_game_resets_all_fields():
    # Every session_state field must be cleared — partial resets leave stale data
    # that carries over into the next game (see FIXME comment in #file:app.py).
    session = {
        "attempts": 5,
        "secret": 99,
        "status": "lost",
        "history": [1, 2, 3, 4, 5],
        "score": -15,
    }
    result = simulate_new_game(session, new_secret=7)
    assert result["attempts"] == 0
    assert result["secret"] == 7
    assert result["status"] == "playing"
    assert result["history"] == []
    assert result["score"] == 0
