from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, character, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()
            
        self.character = character
        self.hit = hit
        self.miss = miss

    
    def is_hit(self):
        if self.hit is True:
            return True
        return False
    
    def is_miss(self):
        if self.miss is True:
            return True
        return False

'''
#guessattemps is called when an attempt is performed one a guessword object
#has two methods "is_hit()" and "is_miss()"
#if the attempt is in the answer, is_hit() is true
'''

class GuessWord(object):

    def __init__(self, word):
        if word == '':
            raise InvalidWordException()
        
        self.answer = word
        self.masked = "*"* len(word)
    

    def perform_attempt(self, character):
        if len(character) > 1:
            raise InvalidGuessedLetterException()
        
        if character.lower() in self.answer.lower():
            attempt = GuessAttempt(character, hit= True)
        else:
            attempt = GuessAttempt(character, miss= True)

        updated_masked_word = ""
        for indx, char in enumerate(zip(self.answer, self.masked)):
            if character.lower() == char[0].lower(): #from self.answer
                updated_masked_word += char[0].lower()

            else:
                updated_masked_word += char[1].lower() #from self.masked

            self.masked = updated_masked_word
        self.masked
        return attempt


'''
#passing a word/string to guess
#has a method "guessAttempts" that takes one char
#able to check the answer and the masked word
#if the attempt is in the answer, than it is a hit, then update the masked word, else, remain the masked word
#if the length is more than one char, raise an exception
'''

class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self,  list_of_words=None, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        if list_of_words is None:
            list_of_words = self.WORD_LIST
        #self.list_of_words = list_of_words
        
        selected_word = self.select_random_word(list_of_words)
        self.word = GuessWord(selected_word)
    
    def guess(self, character):
        if self.is_finished():
            raise GameFinishedException()
        attempt = self.word.perform_attempt(character)
        self.previous_guesses += character.lower()

 
        if not attempt.is_hit():
            self.remaining_misses -= 1
            if self.remaining_misses <1:
                raise GameLostException()
          
        
        if self.is_won():
            raise GameWonException()
    
        return attempt

    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    
    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False
            
    @classmethod
    def select_random_word(cls,list_of_words):
        if len(list_of_words) ==0:
            raise InvalidListOfWordsException()
        
        return random.choice(list_of_words)


'''
#class method "select_random_word" --> select one randomly from a list
#hangmanGam can optionally passing a list of workd and the number of attemps 
#by default the num of attemps is 5
#word_list should be taken from class variable "hangmanGame.WORD_LIST"

'''