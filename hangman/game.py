from .exceptions import *
import random


class GuessAttempt(object):
    
    def __init__(self, chara, hit = None, miss = None):
        self.chara = chara
        self.hit =hit
        self.miss = miss
        
        if  hit is True and  miss is True:
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
    def __init__(self,word):
        
        if len(word) == 0:
            raise InvalidWordException()
        
        self.answer = word
        self.masked = '*' * len(self.answer)
        
        
    def discovery(self,  chara ):
       
        holder = ''
        for j in range(len(self.answer)):
            wordLetter = self.answer[j].lower()
            maskedLetter =self. masked[j]
    
            if maskedLetter != '*':
                holder += maskedLetter
            elif chara.lower() == wordLetter:
                holder += wordLetter
    
            else:
                holder += '*'
        return holder    
    
    
    
        
    def perform_attempt (self, chara):
        if len(chara)>1:
            raise InvalidGuessedLetterException()
            
        
            
        if chara.lower() in self.answer.lower():
            
            self.masked = self.discovery( chara)
            
            return GuessAttempt(chara, hit=True )
        else:
            return GuessAttempt(chara, miss=True )
        


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, word_list = None, number_of_guesses = 5 ):
        
        if  not word_list :
            word_list =self.WORD_LIST
        else:
            self.word_list = word_list
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(word_list))
        self.previous_guesses = []
        
    @classmethod
    def select_random_word(cls, word_list):
        if len(word_list) == 0:
            raise InvalidListOfWordsException()
        chosenWord = random.choice(word_list)
        return chosenWord
        
        
    def guess(self,character):
        
        if self.is_finished():
            raise GameFinishedException()
        
        attempt = self.word.perform_attempt(character)
        self.previous_guesses.append(character.lower())
        
        if attempt.is_miss():
            self.remaining_misses -=1
            
            if self.remaining_misses == 0:
                raise GameLostException()
        
        if '*' not in self.word.masked:
            
            raise GameWonException()
        
        return attempt
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
        
    def is_lost(self):  
        if self.remaining_misses == 0:
            return True
        return False
        
        
    def is_won(self):
        
        if '*' not in self.word.masked:
            return True
        return False
    
    
