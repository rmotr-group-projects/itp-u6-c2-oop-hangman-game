from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self, letter, miss=None, hit=None):
        if (hit and miss) or (miss==None and hit==None):
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
        self.answer = word
        self.masked = self.mask_word()
    
    def mask_word(self):
        if len(self.answer) == 0:
            raise InvalidWordException()
        mask = '*' * len(self.answer)
        return mask
        
    def perform_attempt(self, letter):
        if letter.lower() in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
        else:
            attempt = GuessAttempt(letter, miss=True)
        
#         if len(self.answer) == 0 or len(self.masked) == 0:
#             raise InvalidWordException()
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
#         if len(self.answer) != len(self.masked):
#             raise InvalidWordException()
        new_masked_word = ''
        for idx, char in enumerate(self.answer.lower()):
            if self.masked[idx] != '*':
                new_masked_word += self.masked[idx]
            elif letter.lower() == char:
                new_masked_word += char
            else:
                new_masked_word += '*'
        self.masked = new_masked_word
        return attempt

    
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        picked_word = self.select_random_word(word_list) 
        self.word = GuessWord(picked_word)
        
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss() == True:
            self.remaining_misses -= 1
            
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()
        return attempt
    
    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses == 0:
            return True
        return False
        
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False
        
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
