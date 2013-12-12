# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")


# global variables
action = ""
action_width = 0
dealer = None
deck = None
in_play = False
outcome = ""
outcome_width = 0
player = None
score = 0
score_width = 409


# constants
CARD_BACK_CENTER = (35.5, 48)
CARD_BACK_SIZE = (71, 96)
CARD_CENTER = (36.5, 49)
CARD_SIZE = (73, 98)
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
SUITS = ('C', 'S', 'H', 'D')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# helper functions
def get_width(s):
    return 525 - frame.get_canvas_textwidth(s, 30)

# class definitions
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card:", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)


class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        cards_in_hand = ""

        for card in self.hand:
            cards_in_hand += str(card) + " "

        return "hand contains " + cards_in_hand

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        # aces count as 1
        # if hand has an ace, add 10 to hand value if it doesn't exceed 21
        value = 0
        has_ace = False

        for card in self.hand:
            if card.get_rank() == 'A':
                has_ace = True
            value += VALUES[card.get_rank()]

        if has_ace and value + 10 <= 21:
            value += 10

        return value

    def draw(self, canvas, pos):
        for idx, card in enumerate(self.hand):
            card_pos = [pos[0] + idx * (73 + 21.25), pos[1]]
            card.draw(canvas, card_pos)


class Deck:
    def __init__(self):
        self.deck = [Card(i, j) for i in SUITS for j in RANKS]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        deck_str = ""

        for i in self.deck:
            deck_str += str(i) + " "

        return "Deck contains " + deck_str


# event handlers
def deal():
    global action, action_width, dealer, deck, in_play, outcome, player, score, score_width

    # Player loses hand if deal is pressed before hand is complete
    if in_play:
        score -= 1
        score_width = get_width('Score = ' + str(score))

    # intialize game state
    action = "Hit or Stand?"
    action_width = get_width(action)
    in_play = True
    outcome = ""
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()

    # deal hand
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())

    in_play = True


def hit():
    global action, action_width, in_play, outcome, outcome_width, score, score_width

    # if the hand is in play, hit the player
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())

            if player.get_value() > 21:
                in_play = False
                score -= 1
                score_width = get_width('Score = ' + str(score))
                outcome = "Player Busts"
                outcome_width = get_width(outcome)
                action = "New Deal?"
                action_width = get_width(action)


def stand():
    global action, action_width, in_play, outcome, outcome_width, score, score_width

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if player.get_value() <= 21:
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())

        # determine winning hand
        if dealer.get_value() > 21:
            score += 1
            score_width = get_width('Score = ' + str(score))
            outcome = "Dealer Busts"
            outcome_width = get_width(outcome)
        elif dealer.get_value() >= player.get_value():
            score -= 1
            score_width = get_width('Score = ' + str(score))
            outcome = "Dealer Wins!"
            outcome_width = get_width(outcome)
        else:
            score += 1
            score_width = get_width('Score = ' + str(score))
            outcome = "Player Wins!"
            outcome_width = get_width(outcome)

    in_play = False
    action = "New Deal?"
    action_width = get_width(action)


def draw(canvas):
    canvas.draw_text('Blackjack', [75, 117], 42,'Aqua', 'sans-serif')
    canvas.draw_text('Score = ' + str(score), [score_width, 114], 30,'Black', 'sans-serif')

    if in_play:
        canvas.draw_text('Dealer', [75, 222], 30, 'Black', 'sans-serif')
    else:
        canvas.draw_text('Dealer has ' + str(dealer.get_value()), [75, 222], 30, 'Black', 'sans-serif')

    canvas.draw_text(outcome, [outcome_width, 222], 30, 'Black', 'sans-serif')
    dealer.draw(canvas, [75, 250])

    # hide dealer hole card if game is active
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [CARD_BACK_CENTER[0] + 75, CARD_BACK_CENTER[1] + 250], CARD_BACK_SIZE)

    canvas.draw_text('Player has ' + str(player.get_value()), [75, 422], 30, 'Black', 'sans-serif')
    canvas.draw_text(action, [action_width, 422], 30, 'Black', 'sans-serif')
    player.draw(canvas, [75, 450])


# initialize frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")


#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()