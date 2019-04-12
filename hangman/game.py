from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self,char, hit=None, miss=None ):
        if hit==miss:
            raise InvalidGuessAttempt
        self.char=char
        if hit:
            self.hit=hit
            self.miss=not hit
        if miss:
            self.miss=miss
            self.hit=not miss
            
    def is_hit (self):
        return self.hit
    
    def is_miss (self):
        return self.miss
            
    


class GuessWord(object):
    
    def __init__(self, word):
        if len(word)<1:
            raise InvalidWordException
        self.answer=word
        self.masked=""
        for char in word:
            self.masked+='*'
            
    def perform_attempt (self, char):
        if len (char)>1:
            raise InvalidGuessedLetterException
            
        masked_list=list(self.masked)    
        if char.lower() in self.answer.lower():
            for index, c in enumerate (self.answer):
                if char.lower()==c.lower():
                    masked_list[index]=c.lower()
            self.masked=''.join(masked_list)       
                    
            return GuessAttempt(char.lower(),hit=True)
        
        else:
            return GuessAttempt(char.lower(),miss=True)
            
            
    


class HangmanGame(object):
    
    WORD_LIST= ['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls,list):
        if len(list)==0:
            raise InvalidListOfWordsException()
        word = random.choice(list)
        return word
    
    def __init__(self, word_list=None, number_of_guesses=5):
        
       
        self.remaining_misses=number_of_guesses
           
        if word_list:
            self.word_list = word_list
            self.word = GuessWord (HangmanGame.select_random_word(word_list))
        else:    
            self.word_list=HangmanGame.WORD_LIST
            self.word = GuessWord(HangmanGame.select_random_word(HangmanGame.WORD_LIST))
        self.previous_guesses=[]
        
   
            
    def is_won(self):
        if self.word.answer==self.word.masked:
            return True  
        return False
            
    def is_lost(self):
        if self.remaining_misses==0:
            return True
        return False
            
    def is_finished(self):
        if self.word.answer==self.word.masked or self.remaining_misses==0:
            return True 
        return False
            
    def guess(self, char):
        if self.is_finished():
            raise GameFinishedException
        guess= self.word.perform_attempt(char)
        self.previous_guesses.append(char.lower())
        if guess.is_miss():
            self.remaining_misses-=1   
        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException
           
       
        return guess
    
    
        
        
       
       
        

    
    
        
