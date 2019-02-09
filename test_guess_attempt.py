import pytest
from hangman.game import GuessAttempt
from hangman.exceptions import InvalidGuessAttempt


def test_guess_attempt_interface_hit(): #pass
    attempt = GuessAttempt('x', hit=True)
    assert attempt.is_hit() is True
    assert attempt.is_miss() is False


def test_guess_attempt_interface_miss(): #pass
    attempt = GuessAttempt('x', miss=True)
    assert attempt.is_miss() is True
    assert attempt.is_hit() is False


def test_guess_attempt_cant_be_both_hit_and_miss(): #pass
    with pytest.raises(InvalidGuessAttempt):
        attempt = GuessAttempt('x', miss=True, hit=True)
