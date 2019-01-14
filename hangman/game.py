from .exceptions import *

import random

class GuessAttempt(object):
    def __init__(self, some_char=None, hit=None, miss=None):
        self.some_char = some_char

        # don't give these default states
        self.hit = hit
        self.miss = miss
        
    #### NEED THIS EXPLAINED
#         if hit:
#             self.hit = True
#         if miss:
#             self.miss = True
        
        # make them both false
        if self.hit and self.miss:
            raise InvalidGuessAttempt()
            
    def is_hit(self):
        return bool(self.hit)

    def is_miss(self):
        return bool(self.miss)
        
    # some methods .... that aren't needed
#     def is_hit(self):
#         return (self.hit == True)
#     def is_miss(self):
#         return (self.miss == True)

class GuessWord(object):
    def __init__(self, word):
        # this check isn't clear to me
        
        if not word:
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = len(self.answer) * '*'
        
        # no situation with guess = None
        # guess char
        
    def perform_attempt(self, guess):
        if len(guess) > 1:
            raise InvalidGuessedLetterException()
        
        #object method
        if guess.lower() not in self.answer:
            return GuessAttempt(guess, miss=True)
            
        # perform attempt needs an attribute is_hit and is_miss?
        
        self.attempt_hit = False
        self.attempt_miss = False
        
        new_masked_word = ''

        # iterate through the masked and unmasked word
        
        # check if guess is in answer...if so replace letter in mask
        
        for answer_char, masked_char in zip(self.answer, self.masked):
            if guess.lower() == answer_char:
                new_masked_word += answer_char
            else:
                new_masked_word += masked_char

        self.masked = new_masked_word

        return GuessAttempt(guess, hit=True)
        
        
        
class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    # init with none, not empty list?
    def __init__(self,word_list=None,number_of_guesses=5):
        if not word_list:
            word_list = self.WORD_LIST # list from the class
    
        # NOT A METHOD...
        self.remaining_misses = number_of_guesses
    
        # PICK A RANDOM WORD
        self.word = GuessWord(self.select_random_word(word_list))
        
        # print(self.word)
        
        #PREVIOUS GUESS starts with nothing
        self.previous_guesses = []
   
        ###game = HangmanGame(['Python'])
        ###attempt = game.guess('y')
        ###assert attempt.is_hit() is True

        ### game.guess('y').is_hit()

    def guess(self,guess_char):
        #lower case the characters before the guess
        guess_char = guess_char.lower()
        
        #make sure you're not reusing stuff
        if guess_char in self.previous_guesses:
            raise InvalidGuessedLetterException()
            
        #if the game is complete, confusing test
        # this is raised because you have to call the is_won 
        # or is_lost functions to see if the game is finished
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(guess_char) #list of prev guesses
        #test = GuessWord(self.word)
        #return test.perform_attempt(guess_char)
    
        # attempt uses a GuessAttempt method perform_attempt
        attempt = self.word.perform_attempt(guess_char)
    
        # A MISS???
        if attempt.is_miss():
            self.remaining_misses -= 1
        
        # CHECK THESE IF YOU WIN OR LOSE THE GAME
        if self.is_won():
            raise GameWonException()

        if self.is_lost():
            raise GameLostException()
    
        #kept getting error because I hadn't returned the result from the other object
        return attempt
    
    def is_won(self):
        return self.word.masked == self.word.answer

    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    
    # the test shows this is a class method, does this make sense to do it that way?
    @classmethod
    def select_random_word(cls, word_list):
        if word_list == []:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
            
            