from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit = None, miss=None):
        if hit == True and miss == True:
            raise InvalidGuessAttempt
        elif hit == False and miss == False:
            raise InvalidGuessAttempt
        self.guess = guess
        self.hit = hit
        self.miss = miss
    def is_hit(self):
        if self.hit == True:
            return True
        else:
            return False
    def is_miss(self):
        if self.miss == True:
            return True
        else:
            return False
            
            
class GuessWord(object):
    def __init__(self, word):
        if word == '':
            raise InvalidWordException
        self.answer = word.lower()
        self.masked = ((len(word)*'*'))
    def perform_attempt(self,guess):
        if len(guess) > 1 or len(guess) <1:
            raise InvalidGuessedLetterException
        if guess.lower() in self.answer.lower():
            hit = True
            miss = False
            attempt = GuessAttempt(guess, hit, miss)
        else:
            hit = False
            miss = True
            attempt = GuessAttempt(guess, hit, miss)
        count = 0
        testword = list(self.masked)
        if attempt.is_hit() == True:
            for letter in self.answer:
                if letter == guess.lower():
                    testword[count]= guess.lower()
                    count+=1
                else:
                    count+=1
        new_masked_word = ''            
        for i in testword:
            new_masked_word+=i
        self.masked = new_masked_word
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, wordlist = WORD_LIST, number_of_guesses = 5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(HangmanGame.select_random_word(wordlist))
        self.guess = GuessAttempt
    @classmethod
    def select_random_word(cls, list_of_words):
        if list_of_words == []:
            raise InvalidListOfWordsException
        return random.choice(list_of_words)
    def is_finished(self):
        pass
    def is_won(self):
        pass
    def is_lost(self):
        pass 