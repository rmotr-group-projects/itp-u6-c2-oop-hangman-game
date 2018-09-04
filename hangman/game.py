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
            raise InvalidWordException()
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

    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    def guess(self, letter):
        letter = letter.lower()

        if self.is_finished():
            raise GameFinishedException() 
  
        if letter in self.previous_guesses:
            raise InvalidGuessedLetterException()

        self.previous_guesses.append(letter)

        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException()

        if self.is_lost():
            raise GameLostException
        
        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False

    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
