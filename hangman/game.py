from .exceptions import *
import random

class GuessAttempt(object):
    
    
    def __init__ (self,letter,hit=None,miss=None):
        
        self.letter=letter
        self.hit=hit
        self.miss=miss
        
        if hit and miss:
            raise InvalidGuessAttempt()
    
    def is_hit(self):
        
        if self.hit == True:
            return True
        return False
    
    def is_miss(self):
        
        if self.miss == True:
            return True
        return False
            


class GuessWord(object):
    
    def __init__ (self,word):
        
        self.answer = word
        self.masked = '*' *len(word)
        
        if not word:
            raise InvalidWordException()
            
    
    def perform_attempt(self,letter):
        
        if len(letter)>1:
            raise InvalidGuessedLetterException()
            
            
        if letter.lower() in self.answer.lower():
            
            a_str=""
            
            for idx, elem in enumerate(self.masked.lower()):
                
                if elem == '*' and self.answer.lower()[idx] == letter.lower():
                                        
                    a_str += letter.lower()
                
                elif elem == '*' and self.answer.lower()[idx] != letter.lower():
                
                    a_str += '*'
                
                elif elem != '*':
                    a_str += elem
                    
            
            self.masked = a_str
            
            
            return GuessAttempt(letter,hit=True)
            
        else:
            
            return GuessAttempt(letter,miss=True)
        
    

class HangmanGame(object):
    
    WORD_LIST=['rmotr', 'python', 'awesome']
    
    @classmethod
    def select_random_word(cls,list_of_words):
        
        if not list_of_words:
            raise InvalidListOfWordsException()
            
        else:
            return random.choice(list_of_words)

        
        
        
    
    def __init__ (self,word_list=None,number_of_guesses=5):
        
        if not word_list:
            word_list = self.WORD_LIST
        
        self.word=GuessWord(self.select_random_word(word_list))        
        self.remaining_misses = number_of_guesses
        self.previous_guesses=[]
    
    def is_won(self):
        
        if self.word.answer == self.word.masked:
            return True
        return False
        
        
    def is_lost(self):
        
        if self.remaining_misses==0 and self.word.answer != self.word.masked:
            return True
        
        return False
        
        
    def is_finished(self):
        if self.is_won() or self.is_lost():
            
            return True

        return False
    
    def guess(self,letter):
        
        
        
        if self.is_finished():
            raise GameFinishedException()
            
        self.previous_guesses.append(letter.lower())
        
        attempt =self.word.perform_attempt(letter)
        
        if attempt.is_miss():
                       
            self.remaining_misses -= 1      
        
        
        
        if self.is_won():
            raise GameWonException()
            
        
        if self.is_lost():
            raise GameLostException()
        
        return attempt
        
    
        
        
    
