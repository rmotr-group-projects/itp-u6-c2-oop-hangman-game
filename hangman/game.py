from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit and miss:
            raise InvalidGuessAttempt("Can't be both hit and miss")
        self.letter = letter
        self.hit = hit
        self.miss = miss
        

    def is_hit(self):
        return bool(self.hit)
    
    def is_miss(self):
        return bool(self.miss)

          

class GuessWord(object):
    def __init__(self, answer):
        if answer == '':
            raise InvalidWordException("Words are empty")
        self.answer = answer
        self.masked = len(answer)*"*"
        
    def perform_attempt(self, letter):
        
        if len(letter) > 1:
            raise InvalidGuessedLetterException("Character to guess has len() > 1")
        
        def uncover(self, letter):
            unmask = ""

            for a, m in zip(self.answer,self.masked):
                if a.lower() == m.lower():
                    unmask += a.lower()
                elif letter.lower() == a.lower() and m == "*":
                    unmask += a.lower()
                else:
                    unmask += m.lower()
            return unmask

        if letter.lower() in self.answer.lower() and letter.lower() not in self.masked.lower():
            self.masked = uncover(self, letter)
        if letter.lower() not in self.answer.lower():
            return GuessAttempt(letter, miss=True)
            
            
        return GuessAttempt(letter, hit=True)
    



class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=WORD_LIST, number_of_guesses=5):
        if not list_of_words:
            list_of_words = self.WORD_LIST
        
        self.list_of_words = list_of_words
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(list_of_words))
    
    def is_won(self):
        return self.word.answer == self.word.masked

    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_won() or self.is_lost()
        
    
    

    
    
    def guess(self, letter):
        letter = letter.lower()
        

        if self.is_finished():
            raise GameFinishedException()
        
        if letter in self.previous_guesses:
            raise InvalidGuessedLetterException()
        
        self.previous_guesses.append(letter)
        attempt = self.word.perform_attempt(letter)
        
        if attempt.is_miss():
            self.remaining_misses -= 1
            
        if self.is_won():
            raise GameWonException()
            
        if self.is_lost():
            raise GameLostException()
            

        

        
        return attempt
    
    
    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException()
        return random.choice(word_list)
    
# # list_of_words = ['python', 'cat', 'dog']
   
# test2 = HangmanGame(['hippo'])
# test2.guess('p')
# test2.guess('o')
# print(test2)


# # print(isinstance(test2.word, GuessWord))
# # print(test2.word.masked)

# print(test2.previous_guesses)
# # print(type(test2))


# # print(test3.previous_guesses)
# # print(test3)
# # print(type(test3))
