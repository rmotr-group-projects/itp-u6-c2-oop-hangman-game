from .exceptions import *


class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        self.guess = guess
        self.hit = hit
        self.miss = miss
        if miss == True and hit == True:
            raise InvalidGuessAttempt
    
    def is_hit(self):
        if self.hit == True:
            return True
        else: 
            return False
    
    def is_miss(self):
        if self.miss == True:
            return True
        else:
            return False



class GuessWord(object):
    def __init__(self, answer):
        if answer == '':
            raise InvalidWordException
        self.attemptedletters = []
        self.answer = answer.lower()
        self.masked = ''
        for i in answer:
            self.masked = self.masked + '*'

    
    def perform_attempt(self, guess):
        guess = guess.lower()
        if len(guess) != 1:
            raise InvalidGuessedLetterException
        if guess in self.attemptedletters:
            raise InvalidGuessedLetterException
        self.attemptedletters.append(guess)
        if guess not in self.answer:
            return GuessAttempt(guess, miss=True)
        if guess in self.answer:
            self.masked = ''
            for i in self.answer:
                if i in self.attemptedletters:
                    self.masked = self.masked + i
                else:
                    self.masked = self.masked + '*'
            return GuessAttempt(guess, hit=True)
        
            
            
    


class HangmanGame(object):
    pass
