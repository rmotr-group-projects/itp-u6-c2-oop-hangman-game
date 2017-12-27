from .exceptions import *
import random

#GuessAttempt: An attempt to guess a letter.
class GuessAttempt(object):
    
    def __init__(self, c, hit=False, miss=False):
        self.char = c
        self.hit = hit
        self.miss = miss
        if hit == miss:
            raise InvalidGuessAttempt
            
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss
        
#GuessWord: A word to guess. Is used by a HangmanGame to keep track of the word to guess.
class GuessWord(object):

    def __init__(self, word):
        self.answer = word
        
        if len(word) == 0:
            raise InvalidWordException
        
        self.masked = '*'*(len(word))
        
    def perform_attempt(self, letter):
            
        if len(letter) != 1 or not letter.isalpha():
            raise InvalidGuessedLetterException
        
        new_masked = ''
        
        for i in range(len(self.answer)):
            if self.answer[i].lower() == letter.lower():
                new_masked += self.answer[i].lower()
            else:
                new_masked += self.masked[i]   
        
        self.masked = new_masked
        
        for i in range(len(self.answer)):
            if self.answer[i].lower() == letter.lower():
                return GuessAttempt(letter, hit=True)
        return GuessAttempt(letter, miss=True)
        
#HangmanGame: the main interface for the user, the "general" game that will be used.
class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=WORD_LIST, number_of_guesses=5):
        self.word_list = word_list
        if not self.word_list:
            self.word_list = HangmanGame.WORD_LIST   
        self.guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        random_word = HangmanGame.select_random_word(self.word_list)
        self.word = GuessWord(random_word)
        self.previous_guesses = []
    
    def select_random_word(list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        i = random.randint(0, len(list_of_words) - 1)
        #print(list_of_words[i])
        return list_of_words[i]
        
    def guess(self, c):
        if self.is_finished():
            raise GameFinishedException
        result = self.word.perform_attempt(c)
        self.previous_guesses.append(c.lower())
        if result.is_miss():
            self.remaining_misses -= 1
        if self.remaining_misses <= 0:
            raise GameLostException
        if self.word.masked.find('*') == -1:
            raise GameWonException
        
        return result
    
    def is_finished(self):
        if self.is_won() or self.remaining_misses <= 0:
            return True
        else:
            return False
        
    def is_won(self):
        if self.word.masked.find('*') == -1:
            return True
        else:
            return False
            
    def is_lost(self):
        return self.is_finished() and not self.is_won()
        
        
    
        
        
    
