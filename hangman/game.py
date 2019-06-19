from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        if self.miss == True:
            if self.hit == True:
                raise InvalidGuessAttempt    
        else:
            self.miss = not hit
            
#         self.miss = not hit
#         if self.hit == True:
#             if self.miss == True:
#                 raise InvalidGuessAttempt
    def is_hit(self):
        if self.hit:
            return True
        else:
            return False
    def is_miss(self):
        remaining_miss_counter = 0
        if self.miss:
            remaining_miss_counter += 1
            return True
        else:
            return False

class GuessWord(object):
    def __init__(self, answer, masked=""):
        self.answer = answer
        self.masked = masked

        if self.answer == "":
            raise InvalidWordException
        for i in self.answer:
            self.masked += "*"
        
    def __str__(self):
        return self.text

    def __add__(self, other):
        self.other = other
        self.answer_len = len(self.answer)
        for i in range(self.answer_len):
            self.masked + "*"
    def is_hit(self, char):
        if char in self.answer:
            return True
        else:
            return False
    def is_miss(self, char):
        if char not in self.anwer:
            return True
        else:
            return False
        
    def perform_attempt(self, char):
        self.char = char.lower()
        if len(self.char) > 1:
            raise InvalidGuessedLetterException
        if self.char.lower() in self.answer.lower():
            already_guessed_char_list = []
            counter = 0
            for letter in self.masked:
                if letter != "*":
                    dict_item = {counter:letter}
                    already_guessed_char_list.append(dict_item)
                counter += 1
            self.masked = ""
            guessed_letter = GuessAttempt(char, True)
            counter = 0
            for letter in self.answer.lower():
                if {counter:letter} in already_guessed_char_list:
                    self.masked += letter
                elif char.lower() == letter:
                    self.masked += letter 
                else:
                    self.masked += "*"
                counter += 1
#             if self.masked == self.answer:
#                 raise GameWonException
            return guessed_letter
        else:
            guessed_letter = GuessAttempt(char, False)
            return guessed_letter
class HangmanGame(object):
    WORD_LIST = ["rmotr", "python", "awesome"]
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = self.number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
        self.previous_guesses = []
        
        
    
    @classmethod
    def select_random_word(cls, words):
        if words == []:
            raise InvalidListOfWordsException
        else:
            word_var = random.choice(words)
            return word_var
#             return GuessWord(word_var)
    
    def guess(self, letter):
        if self.word.masked == self.word.answer:
            raise GameFinishedException
            raise GameWonException
        if self.remaining_misses == 0:
            raise GameFinishedException
        self.previous_guesses.append(letter.lower())
        before_guess = self.word.masked
        self.word.perform_attempt(letter)
        after_guess = self.word.masked
        if "*" not in self.word.masked:
            raise GameWonException
        if before_guess == after_guess:
            hit = False
            self.remaining_misses -= 1
            if self.remaining_misses == 0:
                raise GameLostException
        else:
            hit = True
        guess_var = GuessAttempt(letter, hit)
        
        return guess_var
    
    def is_finished(self):
        if self.word.masked == self.word.answer:
            return True
        if self.remaining_misses == 0:
            return True
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        if self.remaining_misses == 0:
            return False
    def is_lost(self):
        if self.word.masked == self.word.answer:
            return False
        elif self.remaining_misses == 0:
            return True