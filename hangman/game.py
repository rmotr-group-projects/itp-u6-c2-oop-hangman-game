from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess, hit=None, miss=None):
        self.guess = guess
        self.hit = hit
        self.miss = miss
           
        if self.hit != None and self.miss != None:
            raise InvalidGuessAttempt()
            
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
        self.answer = answer
        self.masked = len(answer) * '*'
        
        if self.answer == '':
            raise InvalidWordException()
    
    def perform_attempt(self, attempt):
        if len(attempt) > 1:
            raise InvalidGuessedLetterException()
            
       
        #Loop through self.answer to determine if guess attempt is
        #present, if so, convert self.mask to a list and replace
        #the proper index(s) with the guess attempt character. 
        #Convert self.mask back to a string and return the value
        
        if attempt.lower() in self.answer.lower():
            newAttempt = GuessAttempt(attempt, hit=True)
            for idx, char in enumerate(self.answer):
                if char.lower() == attempt.lower():
                    self.masked = list(self.masked) #[*,*,*,*,...]
                    self.masked[idx] = attempt.lower()
                    self.masked = ''.join(self.masked) # *y****
        else:
            newAttempt = GuessAttempt(attempt, miss=True)
        return newAttempt
            
            
        
class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
        
    def __init__(self, wordlist=WORD_LIST, number_of_guesses=5):  
        self.word = GuessWord(HangmanGame.select_random_word(wordlist))
        self.wordlist = wordlist
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
          
    @classmethod
    def select_random_word(cls, words):
        if words == []:
            raise InvalidListOfWordsException
        return random.choice(words).lower()
    
    def guess(self, userguess):
        
        if self.word.answer == self.word.masked or self.remaining_misses == 0:
            raise GameFinishedException
            
        userguess = userguess.lower()
        self.previous_guesses.append(userguess)
        self.word.perform_attempt(userguess)
        
            
        if userguess:
            if userguess not in HangmanGame.select_random_word(self.wordlist):
                self.remaining_misses -= 1
        
            if self.word.answer == self.word.masked:
                raise GameWonException
            if self.remaining_misses == 0:
                raise GameLostException
          
        return self.word.perform_attempt(userguess)
    
    def is_finished(self):
        if self.word.answer == self.word.masked or self.remaining_misses == 0:
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