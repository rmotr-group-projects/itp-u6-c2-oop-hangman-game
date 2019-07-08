from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess_letter, hit=False, miss=False):
        self.guess_letter = guess_letter
        self.hit = hit
        self.miss = miss
        if hit is True and miss is True:
            raise InvalidGuessAttempt


    def is_hit(self):
        if self.hit:
            return True
        else:
            return False

    def is_miss(self):
        if self.miss:
            return True
        else:
            return False
    
class GuessWord(object):
    def __init__(self, guess_word):
        if not guess_word:
            raise InvalidWordException
        self.answer = guess_word.lower()
        self.answer_as_list = list(guess_word)
        self.masked = self.mask_word(guess_word)

    def perform_attempt(self, attempt):
        if len(attempt) > 1:
            raise InvalidGuessedLetterException
        if attempt.lower() in self.answer:
            x = GuessAttempt(attempt, hit=True)
            self.unmask_word(attempt)
        else:
            x = GuessAttempt(attempt, miss=True)
        return x

    def mask_word(self, guess_word):
        len_of_word = len(guess_word)
        word = '*' * len_of_word
        return word

      
    def unmask_word(self, character):
        word_guess_list = list(self.masked)
        for idx, char in enumerate(self.answer):
            if char == character.lower():
                word_guess_list[idx] = char
        self.masked = ''.join(word_guess_list)
 

    
class HangmanGame(object):
    '''
    attrs to track:
    remaining_misses
    previous guesses
    '''
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word_list = word_list
        self.word = GuessWord(random.choice(self.word_list))
    
    @classmethod
    def select_random_word(self, list_of_words):
        if len(list_of_words) == 0:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)
   
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException
        self.previous_guesses.append(letter.lower())
        attempt = self.word.perform_attempt(letter.lower())
        if attempt.is_miss():
            self.remaining_misses -= 1
        self.check_game_status()
        return attempt
    
    def check_game_status(self):
        status = ''
        if not status:
            if self.is_won():
                status = 'won'
                raise GameWonException
            if self.is_lost():
                status = 'lost'
                raise GameLostException
            if self.is_finished():
                status = 'finished'
                raise GameFinishedException
        elif status == 'finished':
            raise GameFinishedException

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
        