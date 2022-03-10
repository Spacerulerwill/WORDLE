from random import choice
from colorama import Fore, init
import os
import enchant
import collections

class Game():
    def __init__(self):
        #get length of word
        while True:
            try:
                word_length = int(input("Enter length of word to guess (4-18): "))
                lines=open(f"words/{word_length}.txt").read().splitlines()
            except:
                continue
            else:
                break            

        self.guess_count = 0
        self.max_guesses = word_length + 1
        self.word_length = word_length
        self.playing = True
        self.win = False
        self.progress = []
        self.d = enchant.Dict("en_US")

        self.word = choice(lines).upper()

        self.alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        
        #set to blue
        for count, i in enumerate(self.alphabet):
            self.alphabet[count] = Fore.CYAN + i + Fore.WHITE
        
        self.error_messages = []   
        for i in range(self.max_guesses):
            row = []
            for j in range(self.word_length):
                row.append("-")
            self.progress.append(row)  

        self.update_frame()      

    def update_frame(self):
        os.system('cls||clear')
        #print(self.word) <-- for testing purposes
        print(f"Welcome to terminal wordle! You have {self.max_guesses - self.guess_count} guesses left!")
        
        for row in self.progress:
            for elem in row:
                print(elem, end=" ")
            print("\n")
       
        for i in range(13):
            print(self.alphabet[i], end=", ")
        print("\n")
        for i in range(13):
            if i != 12:
                print(self.alphabet[i+13], end=", ")
            else:
                print(self.alphabet[i+13], end="")

        print("\n")
        if self.error_messages != []:
            for error in self.error_messages:
                print(error)
            self.error_messages = []

    def game_loop(self):
        if self.playing:
            guess = repeatable_input(f"Enter {self.word_length} letter guess: ", lambda x: len(x) == self.word_length and x.isalpha() and self.d.check(str(x)), str)
           
            if guess[1] != False:
                guess = guess[0].upper()
                if guess == self.word:
                    self.playing = False
                    self.win = True
                else:
                    #get amount of each letter in guess
                    d = dict(collections.Counter(self.word))

                    #loop through and detect green letters
                    for count, letter in enumerate(guess):
                        if self.word[count] == letter:
                            self.progress[self.guess_count][count] = Fore.GREEN + letter + Fore.WHITE
                            
                            #update alphabet list
                            for count, alpha in enumerate(self.alphabet):   
                                if letter in alpha:
                                    self.alphabet[count] = Fore.GREEN + letter + Fore.WHITE

                            #remove letter counter
                            if d[letter] > 0:
                                d[letter] -= 1

                    #yellow letters
                    for count, letter in enumerate(guess):
                        if self.word[count] != letter and letter in self.word:
                            if d[letter] > 0:
                                self.progress[self.guess_count][count] = Fore.YELLOW + letter + Fore.WHITE

                                #update alphabet list
                                for count, alpha in enumerate(self.alphabet):
                                    if letter in alpha:
                                        if Fore.GREEN not in alpha:
                                            self.alphabet[count] = Fore.YELLOW + letter + Fore.WHITE

                                d[letter] -=1
                            else:
                                self.progress[self.guess_count][count] = Fore.WHITE + letter + Fore.WHITE

                    #not found letters
                    for count, letter in enumerate(guess):
                        if letter not in self.word:
                            self.progress[self.guess_count][count] = Fore.WHITE + letter + Fore.WHITE

                            #update alphabet list
                            for count, alpha in enumerate(self.alphabet):
                                if letter in alpha:
                                    if Fore.GREEN not in alpha:
                                        self.alphabet[count] = Fore.WHITE + letter + Fore.WHITE

                self.guess_count += 1

            else:
                #error message handling
                guess = guess[0].upper()
                if guess != "":
                    if len(guess) != self.word_length:
                        self.error_messages.append(Fore.RED + f"Guess must be {self.word_length} letters long!" + Fore.WHITE)
                    if not(guess.isalpha()):
                        self.error_messages.append(Fore.RED + f"Guess must only contains letters!" + Fore.WHITE)
                    if not(self.d.check(guess)):
                        self.error_messages.append(Fore.RED + f"Guess must be an english word!" + Fore.WHITE)
                else:
                    self.error_messages.append(Fore.RED + f"Guess must not be blank!" + Fore.WHITE)


            self.update_frame()

def play_game():
    init()
    g = Game()
    while g.guess_count < g.max_guesses and g.playing:
        g.game_loop()
    if g.win:
        #show word was correct
        for count, i in enumerate(g.progress[g.guess_count-1]):
            g.progress[g.guess_count-1][count] = Fore.GREEN + g.word[count] + Fore.WHITE
        g.update_frame()
        print("You Won!")
    else:
        print(f"You lost! The word was {g.word}")

    play_again = repeatable_input("Would you like to play again? (Y/N): ", lambda x: x == "Y" or x.upper() == "X", str)
    play_again[0] = play_again[0].upper()
    if play_again[0] == "Y":
        play_game()
        
if __name__ == "__main__":
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

def repeatable_input(message, lambda_condition, datatype):
  while True:
    usrinput = input(message)
    try:
      datatype(usrinput)
      try:
        if lambda_condition(datatype(usrinput)) == True:
          break
      
        else:
          return [usrinput, False]
      except:
        [usrinput, False]
    except:
      return [usrinput, False]
  return [usrinput, True]

if __name__ == "__main__": 
    play_game()