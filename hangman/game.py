from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
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
        if not word:
            raise InvalidWordException
        self.answer = word
        self.masked = '*' * len(word)

    def unveil_word(self, letter):
        s = ''
        for idx in range(len(self.answer)):
            word_letter = self.answer[idx]
            mask_letter = self.masked[idx]

            if mask_letter != '*':
                s += mask_letter
            elif letter == word_letter.lower():
                s += word_letter.lower()
            else:
                s += '*'
        return s

    def perform_attempt(self, letter):
        if len(letter) > 1:
            raise InvalidGuessedLetterException
        
        letter = letter.lower()
        if letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unveil_word(letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt





class HangmanGame(object):
    
    def __init__(self, word_list, number_of_guesses):
        self.remaining_misses = number_of_guesses
        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        self.previous_guesses = []

    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException
        return random.choice(word_list)
