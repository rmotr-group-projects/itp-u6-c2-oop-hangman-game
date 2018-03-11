from .exceptions import *
import random


class GuessAttempt(object):

    def __init__(self, ltr, hit=None, miss=None):
        if not isinstance(ltr, str) or len(ltr) != 1:
            raise InvalidGuessedLetterException

        if hit == miss:
            raise InvalidGuessAttempt

        self.ltr = ltr
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
        if not isinstance(word, str) or len(word) < 2:
            raise InvalidWordException

        self._word = word
        self.answer = self._word
        self.masked = '*' * len(self._word)

    def perform_attempt(self, ltr):
        if not isinstance(ltr, str) or len(ltr) != 1:
            raise InvalidGuessedLetterException

        if ltr.lower() in self.masked:
            raise InvalidGuessAttempt

        if ltr.lower() in self._word.lower():
            for inx, letter in enumerate(self._word):
                if letter.lower() != ltr.lower():
                    continue
                masked_to_list = list(self.masked)
                masked_to_list[inx] = ltr.lower()
                self.masked = ''.join(masked_to_list)
            return GuessAttempt(ltr, hit=True)

        return GuessAttempt(ltr, miss=True)


class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=None, number_of_guesses=5):
        if not isinstance(number_of_guesses, int) or not number_of_guesses:
            raise InvalidNumberOfGuesses

        self.number_of_guesses = number_of_guesses
        self.word_list = word_list

        if not word_list:
            self.word_list = HangmanGame.WORD_LIST

        if not all(isinstance(word, str) for word in self.word_list):
            raise InvalidListOfWordsException

        self.remaining_misses = self.number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(HangmanGame.select_random_word(self.word_list))

    def guess(self, ltr):
        if self.is_finished():
            raise GameFinishedException

        if not isinstance(ltr, str) or len(ltr) != 1:
            raise InvalidGuessedLetterException

        if ltr in self.previous_guesses:
            raise InvalidGuessedLetterException

        attempt = self.word.perform_attempt(ltr)

        if attempt.is_miss():
            self.previous_guesses.append(attempt.ltr.lower())
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException
        else:
            self.previous_guesses.append(ltr.lower())
            if self.is_won():
                raise GameWonException
        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False

    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False

    def is_lost(self):
        if self.word.masked != self.word.answer and self.remaining_misses < 1:
            return True
        return False

    @classmethod
    def select_random_word(cls, words):
        if not isinstance(words, list) or not words:
            raise InvalidListOfWordsException
        return random.choice(words)
