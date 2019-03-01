import random
from .exceptions import *

class GuessAttempt(object):\

    def __init__(self,guess,hit=False,miss=False):
        self.guess = guess
        self.hit = hit
        self.miss = miss
        if hit == True and miss == True or hit == False and miss == False:
            raise InvalidGuessAttempt('Invalid Guess')
    
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
    
    pass


class GuessWord(object):

    def __init__(self,answer_word=''):
        self.answer = answer_word
        self.masked = ''.join('*' for _ in range(len(answer_word)))
        if len(answer_word)==0:
            raise InvalidWordException('Invalid length')
    
    def perform_attempt(self,guess=''):
        if len(guess)!=1:
            raise InvalidGuessedLetterException('One letter please')
        matches = []
        masked_list = list(self.masked)
        hit = False
        miss = True
        for pos,letter in enumerate(self.answer.lower()):
            if guess.lower()==letter:
                matches.append(pos)
                hit = True
                miss = False
        for pos,letter in enumerate(self.masked):
            if pos in matches:
                masked_list[pos] = guess.lower()
        self.masked = ''.join(masked_list)
        return GuessAttempt(guess,hit,miss)
    

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def is_finished(self):
        if self.finish==True:
            return True
        else:
            return False
    def is_won(self):
        if self.won==True:
            return True
        else:
            return False
    def is_lost(self):
        if self.lost==True:
            return True
        else:
            return False
    
    @classmethod
    def select_random_word(cls,wordList=WORD_LIST):
        if len(wordList)==0:
            raise InvalidListOfWordsException('Send a list')
        return random.choice(wordList)
    
    def __init__(self, wordList = WORD_LIST, number_of_guesses=5):
        
        self.remaining_misses=number_of_guesses
        self.answer = HangmanGame.select_random_word(wordList)
        self.word = GuessWord(self.answer)
        self.previous_guesses = []
        self.finish = False
        self.won = False
        self.lost = False
    
    def guess(self,letter=''):
        if self.finish == True:
            raise GameFinishedException(Exception)
            
        thisGuess = self.word
        thisGuess.perform_attempt(letter)
        
        
        if thisGuess.masked == self.answer:
            self.won = True
            self.finish = True
            self.previous_guesses.append(letter.lower())
            raise GameWonException("Game Won")
            
            
        elif thisGuess.perform_attempt(letter).is_miss():
            self.remaining_misses-=1
            self.previous_guesses.append(letter.lower())
            if self.remaining_misses==0:
                self.lost = True
                self.finish = True
                raise GameLostException("Game Lost")  

        else:
            self.previous_guesses.append(letter.lower())
      
          
    
                
        return thisGuess.perform_attempt(letter) 
    
    
    

