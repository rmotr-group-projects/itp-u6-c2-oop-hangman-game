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
        return bool(self.hit)

    def is_miss(self):
        return bool(self.miss)





# tracks the word to guess, and current state of masked word
class GuessWord(object):

    def __init__(self, answer):
        if len(answer) == 0:
            raise InvalidWordException()
        self.answer = answer.lower()
        self.masked = self.mask_word(self.answer)

    def perform_attempt(self, letter):
        if len(letter) is 1:
            if letter.lower() in self.answer:

                new_masked_word = ''
                for answer_char, masked_char in zip(self.answer, self.masked):  # this part is hard as hell. Had to cheat - ASK FOR CLARITY!!!
                    if answer_char.lower() == letter.lower():
                        new_masked_word += answer_char
                    else:
                        new_masked_word += masked_char

                self.masked = new_masked_word
                return GuessAttempt(letter, hit=True)

            else:
                return GuessAttempt(letter, miss=True)

        raise InvalidGuessedLetterException()

    def mask_word(self, a_word):
        return len(a_word) * '*'







# shows game status
class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))

    # NEED HELP HERE - WTF IS THIS DECORATOR AND FIRST ARGUMENT!?!?
    @classmethod
    def select_random_word(cls, list_of_words):
        if len(list_of_words) is 0:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)

    def guess(self, letter):
        if len(letter) is 1:
            if letter.lower() in self.previous_guesses:
                raise InvalidGuessedLetterException()

            if self.is_finished():
                raise GameFinishedException()

            self.previous_guesses.append(letter.lower())

            attempt = self.word.perform_attempt(letter)

            if attempt.is_miss():
                self.remaining_misses -= 1

            if self.is_won():
                raise GameWonException()

            if self.is_lost():
                raise GameLostException()

            return attempt

    def is_finished(self):
        return self.is_won() or self.is_lost()

    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0


# game = HangmanGame()
# print(game.word_list)
# print(HangmanGame.word_list)
# print(HangmanGame.WORD_LIST)
# print(game.number_of_guesses)
# print(HangmanGame.select_random_word(['hi', 'there', 'how', 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
