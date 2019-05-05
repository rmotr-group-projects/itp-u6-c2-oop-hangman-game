import random
from .exceptions import *

class GuessAttempt(object):
    
    def __init__(self, character, hit=None, miss=None):
        if hit == True and miss == True:
            raise InvalidGuessAttempt()
        self.character = character
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        return self.hit == True
        
    def is_miss(self):
        return self.miss == True
        
class GuessWord(object):
    
    def __init__(self, answer):
        if not answer:
            raise InvalidWordException
        self.answer = answer
        self.masked = len(answer) * '*'
        
    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        
        if character.lower() in self.answer.lower():
            self.masked = list(self.masked)
            for index, letter in enumerate(self.answer):
                if character.lower() == letter.lower():
                    self.masked[index] = character.lower()
            self.masked = ''.join(self.masked)
            return GuessAttempt(character, hit=True)
        return GuessAttempt(character, miss=True)
        
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    def is_won(self):
        return self.word.answer == self.word.masked
            
    def is_lost(self):
        return self.remaining_misses == 0
        
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    def guess(self, character):
        character = character.lower()
        
        if self.is_finished():
            raise GameFinishedException()
        
        attempt = self.word.perform_attempt(character)
        self.previous_guesses.append(character)
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException()
        
        if self.is_lost():
            raise GameLostException()
        return attempt
    
    @classmethod    
    def select_random_word(cls, word_list):
        try:
            return random.choice(word_list)
        except:
            raise InvalidListOfWordsException
        