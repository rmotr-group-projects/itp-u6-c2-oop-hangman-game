from .exceptions import *
from random import *


class GuessAttempt(object):
    def __init__(self, alphabet, hit=None, miss=None):
        self.alphabet = alphabet
        self.hit = hit
        self.miss = miss

        if hit:
            if miss:
                raise InvalidGuessAttempt()

# Adding @property to test. This was suggested on online help.
# TODO - read about @property on python docs.


    def is_hit(self):
        if self.hit is None:
            self.hit = False
        return self.hit


    def is_miss(self):
        if self.miss is None:
            self.miss = False
        return self.miss


class GuessWord(object):
    def __init__(self, word):

        if len(word) == 0:
            raise InvalidWordException()

        self.answer = word.lower()
        self.masked = '*' * len(word)

    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()

        masked_work = ''
        for i in range(0, len(self.answer)):
            if letter.lower() == self.answer[i].lower():
                masked_work += letter.lower()
            else:
                masked_work += self.masked[i]
        self.masked = masked_work

        attempt = GuessAttempt(letter)
        if letter.lower() in self.answer.lower():
            attempt.hit = True
        else:
            attempt.miss = True

        return attempt

