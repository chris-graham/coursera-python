# implementation of card game - Memory

import random
import simplegui

CARD_WIDTH = 50

deck = []
exposed = []
selection1 = 0
selection2 = 0
state = 0
turn = 0

# helper function to initialize globals
def new_game():
    global deck, exposed, selection1, selection2, state, turn

    deck = range(8)
    deck.extend(range (8))
    random.shuffle(deck)
    exposed = [False] * 16
    state = 0
    turn = 0
    label.set_text("Turns = 0")
    selection1 = 0
    selection2 = 0


# define event handlers
def mouseclick(pos):
    global selection1, selection2, state, turn

    card_idx = pos[0] / CARD_WIDTH

    if not exposed[card_idx]:
        exposed[card_idx] = True

        if state == 0:
            selection1 = card_idx
            state = 1
        elif state == 1:
            selection2 = card_idx
            state = 2
            turn += 1
            label.set_text("Turns = " + str(turn))
        else:
            if deck[selection1] != deck[selection2]:
                exposed[selection1] = False
                exposed[selection2] = False
            selection1 = card_idx
            state = 1


# cards are logically 50x100 pixels in size    
def draw(canvas):
    for idx, n in enumerate(deck):
        if exposed[idx]:
            canvas.draw_text(str(deck[idx]), (13 + idx * CARD_WIDTH, 67), 48, 'White')
        else:
            canvas.draw_polygon([(idx * CARD_WIDTH, 0), (idx * CARD_WIDTH, 100), 
                                 (idx * CARD_WIDTH + CARD_WIDTH, 100), 
                                 (idx * CARD_WIDTH + CARD_WIDTH, 0)], 2, 'Maroon', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()