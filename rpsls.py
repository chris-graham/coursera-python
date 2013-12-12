import random

def number_to_name(num):
    """
    Map RPSLS number to corresponding name and return the name
    """
    
    if num == 0:
        return "rock"
    elif num == 1:
        return "Spock"
    elif num == 2:
        return "paper"
    elif num == 3:
        return "lizard"
    elif num == 4:
        return "scissors"
    else:
        print "number_to_name(): Number does not match RPSLS options"
    
def name_to_number(name):
    """
    Map RPSLS name to corresponding number and return the number
    """

    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "name_to_number(): Name does not match RPSLS options"

def rpsls(name):
    """
    Implement rock, paper, scissors, lizard, Spock game that takes as input the
    players choice and generate the competing choice. Determine the winner of
    the two choices and output the results.
    """
    
    # Convert name to player_number using name_to_number
    player_number = name_to_number(name)
    
    # Compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)
    
    # Compute difference of player_number and comp_number modulo five
    difference = (player_number - comp_number) % 5
    
    # Determine winner
    win = False
    tie = False
    if difference == 0:
        tie = True
    elif difference == 1 or difference == 2:
        win = True
    elif difference == 3 or difference == 4:
        win = False
    else:
        print "Error determining winner: difference = ", difference

    # Print results
    print "Player chooses", name
    print "Computer chooses", number_to_name(comp_number)
    if tie:
        print "Player and computer tie!\n"
    elif win:
        print "Player wins!\n"
    elif not win:
        print "Computer wins!\n"
    else:
        print "Error printing results: win = ", win

# Test code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")