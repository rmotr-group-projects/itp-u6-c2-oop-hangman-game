from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, attempt, hit=False, miss=False):
        self.attempt = attempt
        self.hit = hit
        self.miss = miss
        if (self.hit==True and self.miss==True) or (self.hit==False and self.miss==False):
            raise InvalidGuessAttempt
        
    def is_hit(self):
        if self.hit:
            return True
        return False
    
    def is_miss(self):
        if self.miss:
            return True
        return False

class GuessWord(object):
    def __init__(self, answer):
        self.answer = answer.lower()
        self.masked = len(self.answer)*"*"
        if self.answer=='':
            raise InvalidWordException

    def perform_attempt(self, attempt):
        attempt = attempt.lower()
        if len(attempt)>1:
            raise InvalidGuessedLetterException
        
        if attempt in self.answer:
            answer_word_chars=[]
            masked_word_chars=[]
            for char in self.answer:
                answer_word_chars.append(char)
            for char in self.masked:
                masked_word_chars.append(char)

            for index, char in enumerate(answer_word_chars):
                if char==attempt:
                    masked_word_chars[index]=attempt

            self.masked=''.join(masked_word_chars)    
            return GuessAttempt(attempt, hit=True)

        else:
            return GuessAttempt(attempt, miss=True)

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=None, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        if list_of_words is None:
            self.word = GuessWord(HangmanGame.select_random_word(HangmanGame.WORD_LIST))
        else:
            self.word = GuessWord(HangmanGame.select_random_word(list_of_words))
        self.previous_guesses=[]
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if list_of_words == []:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)
    
    def guess(self, guess):
        guess = guess.lower()
        if self.is_finished():
            raise GameFinishedException
        if guess in self.word.answer:
            self.previous_guesses.append(guess)
            res = self.word.perform_attempt(guess)
            if self.is_won():
                raise GameWonException
            return res
        else:
            self.previous_guesses.append(guess)
            self.remaining_misses-=1
            if self.remaining_misses==0:
                if self.is_lost():
                    raise GameLostException
            return self.word.perform_attempt(guess)
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
        
    def is_lost(self):
        if self.remaining_misses==0:
            return True
        return False
        
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False


### def test_game_with_two_correct_guesses_same_move() thought process
# game = HangmanGame(['rmotr'])
# # game is a HangmanGame class - this is created based on what you have
# attempt = game.guess('r')
# # game.guess() means guess is an instance method you need to define for the class of game, HangmanGame. That method should return a GuessAttempt instance object which is returned in the GuessWord instance method, perform_attempt. so guess should be passed through the perform_attempt instance method 