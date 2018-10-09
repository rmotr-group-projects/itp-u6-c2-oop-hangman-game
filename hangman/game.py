from .exceptions import *
from random import choice

class GuessAttempt(object):
    
    
    def __init__(self, attempt, hit = None, miss = None):
        
        self.attempt = attempt
        self.hit = hit
        self.miss = miss
        
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt()
        
        
    def is_hit(self):
        
        if self.hit:
            return True
        
        if self.miss:
            return False
        
        
    def is_miss(self):
        
        if self.miss:
            return True
        
        if self.hit:
            return False


class GuessWord(object):
    
    
    def __init__(self, word):
        word = word.lower()
        
        if not word:
            raise InvalidWordException()
        
        self.answer = word
        self.masked = '*' * len(word)
    
    
    def perform_attempt(self, letter):
        
        letter = letter.lower()
        
        if len(letter) > 1 :
            raise InvalidGuessedLetterException
        
        if letter in self.answer:
            attempt = GuessAttempt(letter, hit = True, miss = False)
            
        if letter not in self.answer:
            attempt = GuessAttempt(letter, hit = False, miss = True)
            
        index = 0
        new_masked_word = ''
        for char in self.answer:
            
            if char == letter:
                new_masked_word += letter
            else:
                new_masked_word += self.masked[index]
            index += 1
        
        self.masked = new_masked_word
        return attempt
    


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    
    def __init__(self, list_of_words = WORD_LIST, number_of_guesses = 5):
        
        self.list_of_words = list_of_words
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(list_of_words))
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return choice(list_of_words)  
        
            
    def guess(self, letter):
    
        if self.is_won() or self.is_lost():
            raise GameFinishedException()
            
        letter = letter.lower()
        self.word.perform_attempt(letter)
        self.previous_guesses.append(letter)
        
        if self.word.perform_attempt(letter).is_miss():
            self.remaining_misses -= 1
        
        if self.word.answer == self.word.masked:
            raise GameWonException()
            
        if self.remaining_misses == 0:
            raise GameLostException()
    
        return self.word.perform_attempt(letter)
        
        
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
        
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
    
    
    def is_finished(self):
        if self.word.answer == self.word.masked or self.remaining_misses == 0:
            return True
        return False


      

