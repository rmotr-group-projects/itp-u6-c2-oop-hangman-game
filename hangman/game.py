from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if (hit == True) and (miss ==  True):
            raise InvalidGuessAttempt

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
        self.masked = len(word) * "*"

        if word == '':
            raise InvalidWordException ()

    def perform_attempt (self, letter):
        if len (letter) != 1:
            raise InvalidGuessedLetterException ()
        letter = letter.lower()
        if letter in self.answer.lower():
            attempt = GuessAttempt (letter, hit=True)
            self.masked = self.unveil_word(letter)
        else:
            attempt = GuessAttempt (letter, miss=True)
        return attempt

    def unveil_word (self,  letter):
        s = ""
        for i in range (len(self.answer)):
            word_letter = self.answer[i]
            mask_letter = self.masked[i]
            if mask_letter != "*":
                s += mask_letter
            elif letter.lower() == word_letter.lower():
                s +=word_letter.lower()
            else:
                s += '*'
        return s


    pass


class HangmanGame(object):
    WORD_LIST =['rmotr', 'python', 'awesome']

    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)

    def guess (self, letter):
        if self.is_finished() is True:
            raise GameFinishedException
        attempt = self.word.perform_attempt(letter)
        self.previous_guesses.append (letter.lower ())
        if attempt.is_miss() is True:
            self.remaining_misses += -1
            if self.remaining_misses == 0:
                raise GameLostException
        if self.word.answer == self.word.masked:
            raise GameWonException


        return attempt


    def is_lost (self):
        if self.remaining_misses == 0:
            return True
        return False

    def is_finished (self):
        if (self.is_won() == True) or (self.is_lost()==True):
            return True


    def is_won (self):
        if self.word.answer == self.word.masked:
            return True
        return False



    @classmethod
    def select_random_word (cls, word_list):
        if len(word_list)== 0:
            raise InvalidListOfWordsException
        return random.choice(word_list)







