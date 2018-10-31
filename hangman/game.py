from .exceptions import *
import random

class GuessAttempt(object):

    def __init__(self, letter, hit=False, miss=False):

        # Truth values for 'hit' and 'miss' must be different
        if hit == miss:
            raise InvalidGuessAttempt

        self.hit = hit
        self.miss = miss

    def is_hit(self):
        return self.hit

    def is_miss(self):
        return self.miss



class GuessWord(object):

    def __init__(self, answer):

        if not answer:
            raise InvalidWordException

        self.answer = answer
        self.masked = '*'*len(answer)

    def perform_attempt(self, guessed_letter):

        if len(guessed_letter) > 1:
            raise InvalidGuessedLetterException

        if guessed_letter.lower() in self.answer.lower():

            new_masked = ''

            for idx, letter in enumerate(self.answer):

                # If there is a new match, or the current letter has already been uncovered
                if guessed_letter.lower() == letter.lower() or self.masked[idx] != '*':
                    new_masked += letter.lower()
                else:
                    new_masked += '*'

            self.masked = new_masked
            return GuessAttempt(guessed_letter, hit=True)

        else:

            return GuessAttempt(guessed_letter, miss=True)


class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    @classmethod
    def select_random_word(cls, word_list):

        if word_list:
            return random.choice(word_list)
        else:
            raise InvalidListOfWordsException


    def __init__(self, word_list=None, number_of_guesses=5):

        if not word_list:
            word_list = HangmanGame.WORD_LIST

        self.word = GuessWord(self.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.finished = False
        self.won = False
        self.lost = False

    def guess(self, guessed_letter):

        if self.finished:
            raise GameFinishedException

        self.previous_guesses.append(guessed_letter.lower())

        attempt = self.word.perform_attempt(guessed_letter)

        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.remaining_misses == 0:
                self.lost = True
                self.finished = True
                raise GameLostException

        elif self.word.answer == self.word.masked:
            self.won = True
            self.finished = True
            raise GameWonException

        return attempt


    def is_won(self):
        return self.won


    def is_lost(self):
        return self.lost


    def is_finished(self):
        return self.finished




