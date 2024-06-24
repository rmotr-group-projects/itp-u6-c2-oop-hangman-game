from .exceptions import *


class GuessAttempt(object):
    
    def __init__(self, char, hit=False, miss=False):
        self.miss = miss
        self.hit= hit
        self.char = char
        if self.miss == True and self.hit == True:
            raise InvalidGuessAttempt
        
    def is_hit(self):
        return self.hit

    def is_miss(self):
        return self.miss
        
    def is_char(self):
        return self.char
    

class GuessWord(object):
    pass

    def __init__(self, answer):
        self.answer = answer
        self.masked = "*"*len(self.answer)
        if len(self.answer) == 0:
            raise InvalidWordException
        

    

    def unmask_word(self, char):
        guess_pos = []
        for pos, character in enumerate(self.answer):
            if character.lower() == char.lower():
                guess_pos.append(pos)
                self.masked = self.masked[:pos] + character.lower() + self.masked[pos + 1:]
        return self.masked
        

    def perform_attempt(self, char):
        if len(char) !=1:
            raise InvalidGuessedLetterException
        if char.lower() in self.answer.lower():
            self.unmask_word(char)
            return GuessAttempt(char, hit= True) 
        else:
            return GuessAttempt(char, miss= True)
            

import random

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    list_of_words=None
    

    def __init__(self, answer= WORD_LIST, number_of_guesses=5):
        self.miss_remaining=0
        self.previous_guesses=[]
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(HangmanGame.select_random_word(answer))

 

    @classmethod
    def select_random_word(cls, list_of_words):
        if list_of_words == []:
            raise InvalidListOfWordsException
        return random.choice(list_of_words) 

    
    def number_of_guesses(self):
        if GuessAttempt.is_miss() is True:
            self.guess_number -= self.guess_number
        return self.guess_number
        
    
       

        
    def guess(self, char):
       if self.is_finished():
            raise GameFinishedException
       attempt = self.word.perform_attempt(char)
       self.previous_guesses.append(char.lower())
       if attempt.is_miss():
           self.remaining_misses -= 1
       if self.is_lost():
           raise GameLostException
       if self.is_won():
            raise GameWonException
       return attempt
       
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        else:
            return False

    def is_lost(self):
        if self.remaining_misses <1:
            return True
        else:
            return False
            
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
            
           
        
 