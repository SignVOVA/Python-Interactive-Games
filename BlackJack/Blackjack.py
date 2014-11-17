# import modules
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")


CARD_BACK_SIZE = (71, 96)   
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/BlackJack/rsz_card_back.jpg")

BG_WIDTH, BG_HEIGHT = 600, 600
BG_IMAGE = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/BlackJack/rsz_green_wool_7x7_pool_table_cloth.jpg")

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
score = 0
FRAME_WIDTH = 600 
FRAME_HEIGHT = 600

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# load some sound
sound_5 = simplegui.load_sound("https://dl.dropboxusercontent.com/u/280794727/BlackJack/Short_triumphal.wav")
background_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/280794727/BlackJack/Frank_Sinatra_Snow.wav")

# set the volume and play
background_sound.set_volume(.2)
background_sound.play()


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print ("Invalid card: ", suit, rank)

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
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.cards = []

    def __str__(self):
        # return a string representation of a hand
        return "Hand contains " + " ".join([str(s) for s in self.cards])

    def add_card(self, card):
        self.cards.append(card)
        #pass    # add a card object to a hand later

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        self.value = 0
        ace_count = 0
        for card in self.cards:
            self.value += VALUES[card.get_rank()]
            if card.get_rank() == 'A' :
                ace_count += 1
                
        if ace_count > 0:
            if self.value + 10 <= 21:
                self.value += 10
                
        return self.value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for c in self.cards:
            c.draw(canvas, [pos[0] + self.cards.index(c) * CARD_SIZE[0], pos[1]])
     
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        # random.shuffle() will do the job
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        k = self.deck[-1]
        self.deck.remove(k)
        return k
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return ans


#define event handlers for buttons
def new_game():
    global outcome, in_play, deck, player, dealer, message, score
    deck = Deck()
    deck.shuffle()
    dealer = Hand()
    player = Hand()
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
       
    score = 0
    
    in_play = True

def deal():
    global outcome, in_play, deck, player, dealer, message, score
    # deck and shuffle
    deck = Deck()
    deck.shuffle()
    # Add 1 Card to daler and player
    dealer = Hand()
    player = Hand()
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    if in_play:
        outcome = "Hit or Stand ?"
        message = "Round Terminated"
        score -= 1
    else:
        outcome = "Hit or Stand ?"
        message = ""
    
    in_play = True

def hit():
    global in_play, outcome, message, score
 
    # if the hand is in play, hit the player
    if in_play and player.get_value() <= 21:
        player.add_card(deck.deal_card())
        outcome = "Hit or Stand ?"
        message = ""
        if player.get_value() > 21:
            score -= 1
            outcome = "New Deal ?"
            message = "You have Busted!"
            in_play = False
   
    # if busted, assign a message to outcome, update in_play and score
    outcome = str(outcome)
       
def stand():
    global outcome, in_play, message, score
    
    if message == "Round Terminated" :
        message = ""
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            
        if dealer.get_value() > 21:
            sound_5.play()
            message = "Dealer busted. You win! Play again?"
            score += 1
        else:
            if dealer.get_value() >= player.get_value():
                outcome = "New Deal?"
                message = "Dealer wins."
                score -= 1
            else:
                outcome = "New Deal?"
                message = "Dealer busted. You win! Play again?"
                score += 1

    # assign a message to outcome, update in_play and score
    in_play = False
    outcome = str(outcome)

# draw handler    
def draw(canvas):
    canvas.draw_image(BG_IMAGE, 
                      [BG_WIDTH // 2, BG_HEIGHT // 2], [BG_WIDTH, BG_HEIGHT],
                      [FRAME_WIDTH // 2, FRAME_HEIGHT // 2], [FRAME_WIDTH, FRAME_HEIGHT])
    canvas.draw_text("Player", [30, 400 + CARD_CENTER[1]], 20, "Black")
    canvas.draw_text("Dealer", [30, 200 + CARD_CENTER[1]], 20, "Black")
    canvas.draw_text("BLACKJACK", [243, 50], 20, "Black")
    canvas.draw_text(str(message), [300 - frame.get_canvas_textwidth(str(message), 35) / 2, 125], 35, "Yellow")
    canvas.draw_text((outcome), [300 - frame.get_canvas_textwidth((outcome), 40) / 2, 360], 40, "Aqua")
    canvas.draw_text("Score " + str(score), [500, 100], 20, "Black")
    player.draw(canvas, [FRAME_WIDTH / 2 - CARD_SIZE[1] * 2, 400])
    dealer.draw(canvas, [100, 200])
    if in_play :
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_BACK_SIZE)
    if background_sound.play():
        background_sound.rewind()
        background_sound.play()
    else:
        pass
        
    


# initialization frame
frame = simplegui.create_frame("Blackjack", FRAME_WIDTH, FRAME_HEIGHT)

#create buttons and canvas callback
frame.add_button("Restart Game", new_game, 200)
frame.add_button("Deal - (New Game)", deal, 200)
frame.add_button("Hit - (Add card)",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()