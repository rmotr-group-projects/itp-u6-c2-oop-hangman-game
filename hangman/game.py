from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, miss = None, hit = None):
        self.letter = letter
        self.miss = miss
        self.hit = hit
        
        if self.miss == True and self.hit == True:
            raise InvalidGuessAttempt()
    
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
    
    def __init__(self, word):
        if not word:
            raise InvalidWordException()
        
        self.answer = word.lower()
        self.masked_list = []
        for char in word:
            self.masked_list.append("*")
        self.masked = "".join(self.masked_list)
    
    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        
        self.letter = letter.lower()
        hit = None
        count = 0
        for char in self.answer:
            if self.letter == char:
                self.masked_list[count] = self.letter
                hit = True
            count += 1
        self.masked = "".join(self.masked_list)
        
        if hit == None:
            return GuessAttempt(self.letter, miss = True, hit = False)
        else:
            return GuessAttempt(self.letter, miss = False, hit = True)
        
        
        
class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = None, number_of_guesses = 5):
        if word_list == None:
            word_list = self.WORD_LIST
        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
    
    def is_won(self):
        if "*" not in self.word.masked and self.remaining_misses > 0:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        else:
            return False
        
    def is_finished(self):
        if ("*" not in self.word.masked and self.remaining_misses > 0) or (self.remaining_misses == 0):
            return True
        else:
            return False
    
    def guess(self, letter):        
        if ("*" not in self.word.masked) or (self.remaining_misses == 0):
            raise GameFinishedException()
        
        attempt = self.word.perform_attempt(letter.lower())
        
        if attempt.is_hit() == False:
            self.remaining_misses -= 1
        self.previous_guesses.append(letter.lower())
        
        if "*" not in self.word.masked:
            raise GameWonException()
            
        if self.remaining_misses == 0:
            raise GameLostException()
        
            
        return attempt
    
    
    #     Receive list of words and selects one randomly
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)

    
    
    
