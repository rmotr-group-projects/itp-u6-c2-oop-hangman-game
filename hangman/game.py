from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess_letter,miss = None, hit=None ):
        if hit and miss:
            raise InvalidGuessAttempt ("Can't be both hit and miss")
        self.miss = miss
        self.hit = hit
        
    def is_hit(self):
        return bool(self.hit)
    
    def is_miss(self):
        return bool(self.miss)
        
            
class GuessWord(object):
    
    
    def __init__(self, true_word):
        if true_word:
            self.answer = true_word.lower()
            self.masked = len(self.answer)*'*'
        else:
            raise InvalidWordException ('Guessed word is invalid')
    
    def perform_attempt(self, guess_letter):
        guess_letter = guess_letter.lower()
        if len(guess_letter) != 1:
            raise InvalidGuessedLetterException ('Only 1 char allowed')
        
        result = ''         
        if guess_letter in self.answer:
            for idx, char in enumerate(self.answer):
                if char != guess_letter:
                    result += self.masked[idx] #instead of hardcoding *, it takes the char from the masked word
                else:
                    result += char
            self.masked = result
            return GuessAttempt(guess_letter, hit = True, miss = False)
        else:
            return GuessAttempt(guess_letter, miss = True, hit = False)



class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome'] #class variable
    
    def __init__(self, word_list = None, number_of_guesses = 5):
        if word_list == None:
            word_list = HangmanGame.WORD_LIST
        self.word = GuessWord(HangmanGame.select_random_word(word_list))
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
    
    @ classmethod
    def select_random_word(cls, word_list): 
        if word_list == []:            
            raise InvalidListOfWordsException ('Word List is empty')
        else:
            return random.choice(word_list)
    
      
    def guess(self,letter):
        if self.is_finished():  # call another method
            raise GameFinishedException
        
        letter = letter.lower()
        attempt = self.word.perform_attempt(letter) #Hangman.GuessWord.perform_attempt
        self.previous_guesses.append(letter)
        
        if attempt.is_miss(): #incorrect guess
            self.remaining_misses-=1
            if self.is_lost(): # call another method
                raise GameLostException ('No more chances, you lost!')
        if self.is_won():   #correct guess # call another method
            raise GameWonException ('You won!')
            
        return attempt
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def is_won(self):
        return self.word.answer == self.word.masked
    
    def is_lost(self):
        return self.remaining_misses <= 0 
"""
def test_select_random_word_with_one_word(): --- didn't create instance

"""