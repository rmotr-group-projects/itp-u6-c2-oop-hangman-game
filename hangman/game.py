from .exceptions import *
from random import shuffle

class GuessAttempt(object):
    
    def __init__(self, letter, hit = None, miss = None):
        self.hit = hit or False
        self.miss = miss or False
        self.letter = letter
        if hit and miss:
            raise InvalidGuessAttempt()
        
        # use or to choose True or False


    # These functions will return either True or False
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss

class GuessWord(object):
    
    def __init__(self, answer = None):
        # Return invalid if answer is empty
        if not answer:
            raise InvalidWordException()
        self.answer = answer
        self.masked =''.join(['*' for i in answer])
        self.masked_list = list(self.masked)
        self.hit = bool
        self.miss = bool
    
    def perform_attempt(self, attempt):
        if len(attempt) > 1 or not attempt :
            raise InvalidGuessedLetterException()
            
        if attempt.lower() in self.answer.lower():
            self.masked =''.join([attempt.lower() if self.answer[i].lower() == attempt.lower() 
            else list(self.masked)[i] for i in range(len(self.answer))])
            self.hit = True
        else:
            self.hit = False
        self.miss = not self.hit
        
        return(GuessAttempt(attempt, self.hit , self.miss ))

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list = WORD_LIST, number_of_guesses = 5):
        self.word = GuessWord(HangmanGame.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
    
    def guess(self,letter):
        if self.is_finished():
            raise GameFinishedException()
                
        self.previous_guesses.append(letter.lower())
        store =  self.word.perform_attempt(letter)
        if store.is_miss():
            self.remaining_misses -=1
        if self.is_won():
            raise GameWonException()
        elif self.is_lost():
            raise GameLostException()
        
        return store
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if list_of_words:
            shuffle(list_of_words)
            return list_of_words[0]
        raise InvalidListOfWordsException()
        
    def is_finished(self):
      
      return self.is_lost() or self.is_won()
        
    def is_won(self):
        
        if self.word.masked == self.word.answer:
            return True
        return False
        
    def is_lost(self):
        return not self.remaining_misses