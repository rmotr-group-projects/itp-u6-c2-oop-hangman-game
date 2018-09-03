from .exceptions import *


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt() 

        self.letter = letter
        self.hit = hit 
        self.miss = miss

    def is_hit(self):
        if self.hit:
            return True
        return False 

    def is_miss(self):
        if self.miss:
            return True
        return False 


class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException()
        self.answer = word
        self.masked = len(word) * '*'

    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()


class HangmanGame(object):
    pass
