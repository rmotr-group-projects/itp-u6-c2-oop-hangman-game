from .exceptions import *
import random

class GuessAttempt(object):
    
    def __init__(self,letter, miss=None, hit=None):
        
        if miss==True and hit==True or miss ==False and hit==False:
            raise InvalidGuessAttempt()
        self.letter = letter
        self.miss = miss
        self.hit = hit 
    
    def is_hit(self):
        
        if self.miss == True or self.hit == False:
            return False
        elif self.miss == False or self.hit == True:
            return True 
    
    def is_miss(self):
        if self.miss == True or self.hit == False:
            return True
        elif self.miss == False or self.hit == True:
            return False

class GuessWord(object):
    def __init__(self, word):
        
        if len(word) < 2:
            raise InvalidWordException()
            
        self.answer = word.lower()
        self.masked = len(word) * '*'
        
    def perform_attempt(self,letter):
        letter = letter.lower()
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        
        if letter in self.answer:
            masked_word = list(self.masked)
            for i in range(len(self.answer)):
                if self.answer[i] == letter:
                    masked_word[i] = letter
        
            self.masked = "".join(masked_word)
            return GuessAttempt(letter, hit=True)
        return GuessAttempt(letter,miss=True)


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome'] 
    
    def __init__(self, word_list = None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    def is_won(self):
        return self.word.masked == self.word.answer
    
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()

    def guess(self,letter):
        
        letter = letter.lower()
        if letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
        
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(letter)
        attempt = self.word.perform_attempt(letter)
        
        if attempt.is_miss():
            self.remaining_misses -= 1 
        
        if self.is_won():
            raise GameWonException()
        
        if self.is_lost():
            raise GameLostException()
            
        return attempt 
            
  
    
    @classmethod
    def select_random_word(cls,word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)

