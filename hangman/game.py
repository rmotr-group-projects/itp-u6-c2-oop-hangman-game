from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit = None, miss = None):
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
        if len(word) == 0:
            raise InvalidWordException
        self.answer = word.lower()
        self.masked = '*' * len(word)

    def perform_attempt(self, letter):
        if len(letter) == 0 or len(letter) > 1:
            raise InvalidGuessedLetterException
        
        if letter.lower() in self.answer:
            current_word = ''
            for answer, mask in zip(self.answer, self.masked):
                if letter.lower() == answer:
                    current_word += answer
                else:
                    current_word += mask
            self.masked = current_word
            
        if letter.lower() in self.answer:
            attempt = GuessAttempt(letter, hit = True)
        else:
            attempt = GuessAttempt(letter, miss = True)
        
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = WORD_LIST, number_of_guesses = 5):
        self.word_list = word_list
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        #selected_word = self.select_random_word(word_list)
        self.word = GuessWord(self.select_random_word(word_list))
        
    @classmethod
    def select_random_word(self, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
    
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append(letter.lower())
        
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException
        
        if self.is_won():
            raise GameWonException
            
        return attempt