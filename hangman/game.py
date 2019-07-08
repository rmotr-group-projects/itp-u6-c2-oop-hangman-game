from .exceptions import *


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit == None and miss == None:
            raise InvalidGuessAttempt("Must be a hit OR a miss")
        if hit != None and type(hit) != bool:
            raise InvalidGuessAttempt("hit must be a bool")
        if miss != None and type(miss) != bool:
            raise InvalidGuessAttempt("miss must be a bool")
        if hit and miss:
            raise InvalidGuessAttempt("Can't be a hit AND a miss")
        self.letter = letter
        if hit == None:
            self.miss = miss
            self.hit = not miss
        if miss == None:
            self.hit = hit
            self.miss = not hit

    def is_hit(self):
        return bool(self.hit)

    def is_miss(self):
        return bool(self.miss)
        

class GuessWord(object):
    def __init__(self, answer):
        if type(answer) != str:
            raise InvalidWordException("Word is type {}, must be type str".format(type(answer)))
        if answer == '':
            raise InvalidWordException("Word can't be''")
        self.answer = answer.lower()
        self.masked = "*" * len(answer)

    def perform_attempt(self, letter):
        if type(letter) != str or len(letter) > 1:
            raise InvalidGuessedLetterException("{} is not a valid letter".format(letter))
        lower_letter = letter.lower()
        is_hit = lower_letter in self.answer
        print("is_hit: {}".format(is_hit))
        if is_hit:
            new_masked_word = ""
            ctr = 0
            for char in self.answer:
                if char == lower_letter:
                    new_masked_word += char
                else:
                    new_masked_word += self.masked[ctr]
                ctr += 1
            self.masked = new_masked_word
        attempt = GuessAttempt(letter, hit=is_hit)
        return(attempt)

import random
class HangmanGame(object):
    WORD_LIST = ['rmotr','python','awesome']
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        

    @classmethod
    def select_random_word(cls, word_list):
        if type(word_list) != list:
            raise InvalidListOfWordsException('word_list is of type {} and must be a list'.format(type(word_list)))
        if len(word_list) == 0:
            raise InvalidListOfWordsException("word_list can't be empty")
        return random.choice(word_list)

    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        attempt = self.word.perform_attempt(letter)
        if letter not in self.previous_guesses:
            self.previous_guesses.append(letter.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException
        return attempt

    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def is_lost(self):
        return self.remaining_misses == 0

    def is_won(self):
        return self.word.answer == self.word.masked