from .exceptions import *
from random import choice


class GuessAttempt(object):
    def __init__(self,guess ,hit=None, miss=None):
        self.hit = hit
        self.miss = miss
        
        if hit and miss:
            raise InvalidGuessAttempt()
            
    def is_hit(self):
        'Determine if guess is a match'
        if self.hit:
            return True
        else:
            return False
    
    def is_miss(self):
        'Determine if guess is not a match'
        if self.miss:
            return True
        else:
            return False
        
        


class GuessWord(object):
    'Guess word class'
    def __init__(self,answer):
        'Initialise and check answer value'
        self.answer = answer        
        answer_length = len(answer)
                       
        if not answer_length:
            raise InvalidWordException() 
        
        self.masked = '*' * answer_length
        
    def perform_attempt(self, guess):
        'try to guess a letter'
        
                
        if len(guess) > 1:
            raise InvalidGuessedLetterException()        
                    
        if guess.lower() in self.answer.lower():
            self.masked = [letter for letter in self.masked]              
            for index, letter in enumerate(self.answer):                
                if letter.lower() == guess.lower():
                    self.masked[index] = guess.lower()   
                    
            self.masked = ''.join(self.masked)      
                        
                
            return GuessAttempt(guess,hit=True)
        else:
            return GuessAttempt(guess, miss=True)
        

class HangmanGame(object):
    'Hangman Game Class'
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls, words):
        if not words:
            raise InvalidListOfWordsException()
        return choice(words)
    
    def __init__(self,word_list=WORD_LIST, number_of_guesses=5):        
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
    
    def guess(self,character): 
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(character.lower())
        result= self.word.perform_attempt(character)    
        
                
        if self.word.masked == self.word.answer:
            raise GameWonException()
        
        if result.miss:
            self.remaining_misses -= 1
            
        if self.remaining_misses == 0:
            raise GameLostException()       
        
        return result
        
    def is_finished(self):
        if self.remaining_misses == 0 or self.word.masked == self.word.answer:
            return True
        else:
            return False
    
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        else:
            return False
    