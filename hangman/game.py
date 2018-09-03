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

    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()

        if letter in self.answer:
            attemp = GuessAttempt(letter, hit=True)
        else:
            attemp = GuessAttempt(letter, miss=True)
        return attemp


class HangmanGame(object):
    pass
