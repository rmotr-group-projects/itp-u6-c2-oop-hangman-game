from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):

        if hit is None and miss is None:
            raise InvalidGuessAttempt

        if hit == miss:
            raise InvalidGuessAttempt
        
        self.letter = letter
        self.is_hit_value = False
        self.is_miss_value = False
        
        if hit == True:
            self.is_hit_value = True
            
        if miss == True:
            self.is_miss_value = True
            
    def is_hit(self):
        return self.is_hit_value
    def is_miss(self):
        return self.is_miss_value

class GuessWord(object):
    def __init__(self, word_to_guess):
        if not word_to_guess:
            raise InvalidWordException
        
        self.answer = word_to_guess.lower()
        self.masked = "*" * len(word_to_guess)

    def perform_attempt(self, char):
        if len(char) > 1:
            raise InvalidGuessedLetterException
        
        if char.lower() in self.answer:
            char = char.lower()
            locations_of_character = []
            for index, letter in enumerate(self.answer):
                if letter == char:
                    locations_of_character.append(index)
            for location in locations_of_character:
                self.masked = self.masked[:location] + char + self.masked[location + 1:]
            return(GuessAttempt(char, hit=True))
        else:
            return(GuessAttempt(char, miss=True))
    
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=[], number_of_guesses=5):
        self.words = list_of_words
        if not list_of_words:
            list_of_words = HangmanGame.WORD_LIST
        self.chosen_word = HangmanGame.select_random_word(list_of_words)
        self.word = GuessWord(self.chosen_word)
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.is_finished_flag = None
    
    def guess(self, guess):
        self.previous_guesses.append(guess.lower())
        guess_try = self.word.perform_attempt(guess)
        
        if self.is_finished_flag == True:
            raise GameFinishedException
        
        if guess_try.is_miss() == True:
            self.remaining_misses -= 1
            if self.remaining_misses == 0:
                self.is_finished_flag = True
                raise GameLostException

        if guess_try.is_hit() == True:
            if self.word.answer == self.word.masked:
                self.is_finished_flag = True
                raise GameWonException
        return self.word.perform_attempt(guess)
    
    @staticmethod
    def select_random_word(list_of_words=[]):
        if list_of_words == []:
            raise InvalidListOfWordsException
        choice = random.choice(list_of_words)
        choice = choice.lower()
        return str(choice)
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.remaining_misses == 0 and self.word.answer != self.word.masked:
            return True
        else:
            return False
    
    def is_finished(self):
        if self.is_finished_flag == True:
            return True
        else:
            return False
        