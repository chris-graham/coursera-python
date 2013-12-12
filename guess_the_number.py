import math
import random
import simplegui

guess = 0
guess_count = 0
secret_number = 0
upper_bound = 100


def new_game():
    """
    starts a new game by generating a new secret number, calculating number of guesses
    and outputing game state
    """
    global secret_number
    global guess_count

    guess_count = int(math.ceil(math.log(upper_bound, 2)))
    secret_number = random.randrange(0, upper_bound)

    print "New game"
    print "Range is from 0 -", upper_bound
    print "You have", guess_count, "guesses remaining\n"


# event handler definitions for control panel
def range100():
    # button that changes range to range [0,100) and restarts
    global upper_bound
    upper_bound = 100
    new_game()

def range1000():
    # button that changes range to range [0,1000) and restarts
    global upper_bound
    upper_bound = 1000
    new_game()
    
def input_guess(guess):
    """
    accepts user guess as input, evaluates the guess and secret number,
    outputs the results and starts a new game when the user wins or 
    runs out of guesses
    """
    global guess_count

    guess_count -= 1

    print "You guessed", guess
    print "You have", guess_count, "guesses remaining"
    
    if int(guess) == secret_number:
        print "You are correct!\n"
        new_game()
    elif guess_count == 0:
        print "You have exhausted all your guesses; the secret number was", secret_number, "\n"
        new_game()
    elif int(guess) < secret_number:
        print "Guess higher!\n"
    else:
        print "Guess lower!\n"


# create frame and register event handlers for control elements
f = simplegui.create_frame('Guess The Number', 200, 200)
f.add_button('Range: 0 - 100', range100, 200)
f.add_button('Range: 0 - 1000', range1000, 200)
f.add_input('Enter a guess', input_guess, 200)

new_game()
f.start()