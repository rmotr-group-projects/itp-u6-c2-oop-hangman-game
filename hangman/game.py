from .exceptions import *
from random import choice


class GuessAttempt:
    def __init__(self, character, miss=None, hit=None):
        self.character = character
        self.miss = miss
        self.hit = hit
    
        if self.hit and self.miss:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        return self.hit is True
    
    def is_miss(self):
        return self.miss is True


        
class GuessWord:
    
    def __init__(self, word):
        if not word:
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = '*' * len(self.answer)
        
    def perform_attempt(self, char):
        
        if len(char) > 1:
            raise InvalidGuessedLetterException()
        attempt = GuessAttempt(char)
        
        char = char.lower()
        
        if char not in self.answer:
            return GuessAttempt(char, miss=True)
        
        else:
            attempt.hit = True
            masked_list = list(self.masked)
            index = 0
            for letter in self.answer:
                if letter == char:
                    masked_list[index] = char
                index += 1
            self.masked = ''.join(masked_list)
            
        return attempt


    

        

    
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=None, number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return choice(word_list)

    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def guess(self, g):
        g = g.lower()
        if g in self.previous_guesses:
            raise InvalidGuessedLetterException()

        if self.is_finished():
            raise GameFinishedException()

        self.previous_guesses.append(g)
        attempt = self.word.perform_attempt(g)
        if attempt.is_miss():
            self.remaining_misses -= 1

        if self.is_lost():
                raise GameLostException()
            
        if self.is_won():
            raise GameWonException()

        

        return attempt