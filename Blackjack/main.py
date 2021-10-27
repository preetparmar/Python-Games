# Importing Libraries
import random

# Defining Variables
playing = True
game_session = True
suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {
    'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11
    }


# Defining Card Class
class Card:
    # Initializing Class
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    # Defining print method
    def __str__(self):
        return f'{self.rank} of {self.suit}'

# Defining Deck Class
class Deck:
    # Initializing Class
    def __init__(self):
        self.deck = []
        self.value = 0
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))
    
    # Defining print method
    def __str__(self):
        complete_deck = ''
        for card in self.deck:
            complete_deck += f'\n {card.__str__()}'
        return f'The deck has {complete_deck}'

    # Adding a method for shuffling the deck
    def shuffle(self):
        return random.shuffle(self.deck)

    # Adding a method for dealing the card
    def deal(self):
        return self.deck.pop()


# Defining Hand Class
class Hand:
    # Initializing the class
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # Function to add a card to the player cards
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    # Handling Ace's value (if total value exceeds 21 then the value of ace changes to 1)
    def adjust_ace_value(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Defining Chips Class
class Chips:
    # Initialzing Class
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    # Function if player wins the bet
    def bet_won(self):
        self.total += self.bet
    
    # Function if player loses the bet
    def bet_lost(self):
        self.total -= self.bet


#  Fucntion for taking bet
def bet_this(chips):
    while True:
        try: 
            chips.bet = int(input(f"\nHow much would you like to bet?\n(You have total of {chips.total} chips)\n"))
        except ValueError:
            print('Sorry, the bet amount should be an integer value\n')
        else:
            if chips.bet > chips.total:
                print(f"Sorry you don't have that many chips. You only have {chips.total} chips.\n")
            else:
                print(f"You bet {chips.bet} chips on this round!\n")
                break

# Function to show some cards
def show_some_cards(dealer, player):
    print(f"Dealer's Card: <Card Hidden> {dealer.cards[1]}\n")
    print("Your Cards:")
    print(*player.cards, sep='\n')
    print(f"Your current value: {player.value}\n")

# Function to show all the cards
def show_all_cards(dealer, player):
    print("Dealer's Cards:")
    print(*dealer.cards, sep='\n')
    print(f"Dealer's final value: {dealer.value}\n")

    print("Your Cards:")
    print(*player.cards, sep='\n')
    print(f"Your final value: {player.value}")

# Function to ask whether the player wants to hit or stand
def hit_or_stand(dealer_hand, player_hand, deck, chips):
    global playing

    while True:
        choice = input("Would you like to Hit or Stand?\nEnter 'h' or 's'\n")
        if choice[0].lower() == 'h':
            print('Player wants to hit\n')
            hit_card(player_hand, deck)
            player_hand.adjust_ace_value()


            if player_hand.value > 21:
                player_lost(chips)
                show_some_cards(dealer_hand, player_hand)
                playing = False
                break
            elif player_hand.value == 21:
                player_won(chips)
                show_some_cards(dealer_hand, player_hand)
                playing = False
                break
            else:
                show_some_cards(dealer_hand, player_hand)

        elif choice[0].lower() == 's':
            print('Player wants to stay\n')
            break

        else:
            print('Please select from the given options only!\n')
            continue

# Function for dealing the card
def hit_card(hand, deck):
    hand.add_card(deck.deal())
    hand.adjust_ace_value()

# Functions for all the game ending scenarios
def player_won(chips):
    chips.bet_won()
    print('\nCongratulation! You WON!!!')
    print(f'You won {chips.bet} chips\nYou have {chips.total} chips in total.\n')

def player_lost(chips):
    chips.bet_lost()
    print('\nOoops!!')
    print(f'Sorry you lost {chips.bet} chips\nYou have {chips.total} chips remaining.\n')

def dealer_won(chips):
    chips.bet_lost()
    print('\nOpps! Dealor Won!')
    print(f'Sorry you lost {chips.bet} chips\nYou have {chips.total} chips remaining.\n')

def dealer_lost(chips):
    chips.bet_won()
    print('\nDealer lost! That means YOU WON!!!')
    print(f'You won {chips.bet} chips\nYou have {chips.total} chips in total.\n')

def tie():
    print('\nDealer and Player Tie!')



""" GAME STARTS """
# Welcoming the player
print('Welcome to the game of Blackjack\n')

#  Initializing the player chips
player_chips = Chips(100)

while game_session:
    playing = True
    # Getting a fresh deck and shuffling it
    deck = Deck()
    deck.shuffle()

    # Dealing Player Hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Dealing Dealer Hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Asking for the bet amount and showing some cards
    bet_this(player_chips)
    show_some_cards(dealer_hand, player_hand)


    if player_hand.value == 21:
        player_won(player_chips)
        print(f"YOU won {player_chips.bet} chips!!!")
        print(f"You now have a total of {player_chips.total} chips")
    else:
        hit_or_stand(dealer_hand, player_hand, deck, player_chips)

        while playing:
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal())
            if dealer_hand.value > 21:
                dealer_lost(player_chips)
                show_all_cards(dealer_hand, player_hand)
                break
            elif dealer_hand.value > player_hand.value:
                dealer_won(player_chips)
                show_all_cards(dealer_hand, player_hand)
                break
            elif dealer_hand.value < player_hand.value:
                player_won(player_chips)
                show_all_cards(dealer_hand, player_hand)
                break
            else:
                tie()
                show_all_cards(dealer_hand, player_hand)
                break
    
    play_again = input("\nDo you want to play again?\nEnter 'y' or 'n'\n")
    if play_again[0].lower() == 'y':
        if player_chips.total > 0:
            continue
        else:
            print('Sorry you do not have any chips left.\nThank you for playing with us!')
            game_session = False
    else:
        game_session = False
        print('Thanks for playing with us')
