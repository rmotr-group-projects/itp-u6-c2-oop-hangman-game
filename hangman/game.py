from hangman.exceptions import *
#from exceptions import *
import random

class GuessAttempt(object):
    #pass
    def __init__(self, passed_char, hit=None, miss=None):
        self.char = passed_char
        self.hit = hit
        self.miss = miss
        if self.hit is True and self.miss is True:
            raise InvalidGuessAttempt()
            
    def is_hit(self):
        if self.hit is True:
            return True
        return False
        
    def is_miss(self):
        if self.miss is True:
            return True
        return False


class GuessWord(object):
    
    def __init__(self, passed_word):
        if not passed_word:
            raise InvalidWordException()
        self.answer = passed_word.lower()
        self.masked = '*' * len(self.answer)
        
    def perform_attempt(self, character):
        if len(character) != 1:
            raise InvalidGuessedLetterException()
            
        elif character.lower() in self.answer:
            new_mask = ''
            for idx, val in enumerate(self.answer):
                if val == character.lower():
                    new_mask += val
                else:
                    new_mask += self.masked[idx]
            self.masked = new_mask
            att = GuessAttempt(character.lower(), hit=True)
        else:
            att = GuessAttempt(character.lower(), miss=True)
        return att

class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        self.word_list = HangmanGame.WORD_LIST if not word_list else word_list
        self.previous_guesses = []
        self.remaining_misses = number_of_guesses
        self.word = GuessWord(self.select_random_word(self.word_list))
        
    def guess(self, ltr):
        ltr = ltr.lower()
        if ltr in self.previous_guesses:
            raise InvalidGuessedLetterException()
        elif self.remaining_misses < 1 or '*' not in self.word.masked:
            raise GameFinishedException()
        elif self.remaining_misses < 1 and '*' in self.word.masked:
            raise GameLostException()
        else:
            check_obj = self.word.perform_attempt(ltr)
            print('masked word after attempt {}'.format(self.word.masked))
            if check_obj.is_hit() is True and ltr not in self.previous_guesses:
                self.previous_guesses.append(ltr)
            if check_obj.is_miss() is True:
                self.remaining_misses -= 1
                self.previous_guesses.append(ltr)
                if self.is_lost():
                    raise GameLostException()
            if check_obj.is_hit():
                if self.is_won():
                    raise GameWonException()
            return check_obj
    
    @classmethod   
    def select_random_word(cls, list_of_words):
        if list_of_words == []:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)
        
    def is_finished(self):
        print(self.word.masked, self.remaining_misses)
        if '*' not in self.word.masked and self.remaining_misses >= 1:
            return True
        elif self.remaining_misses < 1 and '*' in self.word.masked:
            return True
        return False
        
    def is_won(self):
        if '*' not in self.word.masked and self.remaining_misses >= 1:
            return True
        return False
    
    def is_lost(self):
        if '*' in self.word.masked and self.remaining_misses < 1:
            return True
        return False
        


# game = HangmanGame(['aba'])
# attempt = game.guess('a')
# print(attempt.is_hit())
# def test_game_wins_several_moves_repeated_words():
#     game = HangmanGame(['aba'])

#     attempt = game.guess('a')
#     assert attempt.is_hit() is True
#     assert game.remaining_misses == 5
#     assert game.previous_guesses == ['a']
#     assert game.word.masked == 'a*a'

#     with pytest.raises(GameWonException):
#         game.guess('b')

#     assert game.is_finished() is True
#     assert game.is_won() is True
#     assert game.is_lost() is False

#     assert game.remaining_misses == 5
#     assert game.previous_guesses == ['a', 'b']
#     assert game.word.masked == 'aba'
        

        






