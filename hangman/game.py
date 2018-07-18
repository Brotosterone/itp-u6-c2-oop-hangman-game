from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self,guess,hit=False,miss=False):
        if hit and miss:
            raise InvalidGuessAttempt
        self.guess = guess
        self.hit = hit
        self.miss = miss
    
    def is_hit(self):
        return self.hit
    
    def is_miss(self):
        return self.miss

class GuessWord(object):
    def __init__(self,answer):
        if not answer:
            raise InvalidWordException
        self.answer = answer
        self.masked = '*' * len(answer)
        
    
    def perform_attempt(self,guess):
        hit = False
        miss = True
        
        if len(guess) > 1:
            raise InvalidGuessedLetterException
        orig_masked = self.masked
        list_masked = list(self.masked)
        list_answer = list(self.answer)
        
        if guess.lower() in self.answer.lower():
            for i,v in enumerate(self.answer):
                if v.lower() == guess.lower():
                    list_masked[i] = guess.lower()
            self.masked = ''.join(list_masked)
            
        if orig_masked != self.masked:
            hit = True
            miss = False
                  
        attempt = GuessAttempt(guess,hit,miss)
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list=['rmotr', 'python', 'awesome'],number_of_guesses=5):
        self.WORD_LIST = word_list
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(random.choice(word_list))
    
    @classmethod
    def select_random_word(cls, w_list):
        cls.word = cls.get_random(w_list)
        return cls.word.answer
        
    @classmethod
    def get_random(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException
        word = random.choice(word_list)
        return GuessWord(word)

    def guess (self, guess):
        if self.is_lost() or self.is_won():
            raise GameFinishedException()
        attempt = self.word.perform_attempt(guess)
        if attempt.is_miss():
            self.remaining_misses -= 1
        self.previous_guesses.append(attempt.guess.lower())
        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()
        return attempt
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
        
    def is_lost(self):
        return self.remaining_misses < 1
        
    def is_won(self):
        return self.word.answer == self.word.masked
        