#black jack

import random

class Card:
    def __init__(self,suits,rank):
        self.suits = suits
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suits}"    

card1=Card("Hearts", "Ace")


print(card1)


class Deck:
    def __init__(self):
        self.cards=[]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

deck = Deck()
print(f"Deck has {len(deck.cards)} cards")

deck.shuffle()
print(f"Deck has {len(deck.cards)} cards before shuffling")

card=deck.deal_card()
print(f"Dealt card: {card}")
print(f"Deck has {len(deck.cards)} cards after dealing one card")       




#     for card in deck.cards:                     ; check the cards in the deck
 #    print(card)                               


class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []

    def take_card(self,card):
        self.hand.append(card)

    def showhand(self):
        for card in self.hand:
            print(card)

    def calculate_score(self):
        score = 0
        aces = 0

        for card in self.hand:
            if card.rank in ["Jack", "Queen", "King"]:
                score += 10

            elif card.rank == "Ace":
                score += 11
                aces += 1

            else:
                values = {
                    "Two": 2,
                    "Three": 3,
                    "Four": 4,
                    "Five": 5,
                    "Six": 6,
                    "Seven": 7,
                    "Eight": 8,
                    "Nine": 9,
                    "Ten": 10
            }
                score += values[card.rank]

    # Convert Ace from 11 to 1 if needed
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        return score


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def deal_initial_cards(self):
        for _ in range(2):
            self.player.take_card(self.deck.deal_card())
            self.dealer.take_card(self.deck.deal_card())

    def show_start(self):
        print("\nPlayer cards:")
        self.player.showhand()
        print("Score:", self.player.calculate_score())

        print("\nDealer cards:")
        self.dealer.showhand()
        print("Score:", self.dealer.calculate_score())


    def player_turn(self):
        while True:
            print("\nYour current hand:")
            self.player.showhand()
            print("Score:", self.player.calculate_score())

        # Check if player busts
            if self.player.calculate_score() > 21:
                print("You busted! Dealer wins.")
                return False

            choice = input("Hit or Stand? ").lower()

            if choice == "hit":
                card = self.deck.deal_card()
                self.player.take_card(card)
                print(f"You got: {card}")

            elif choice == "stand":
                print("You stand.")
                return True

            else:
                print("Invalid choice. Please type Hit or Stand.")

    def dealer_turn(self):
        print("\nDealer's turn:")

        self.dealer.showhand()
        print("Score:", self.dealer.calculate_score())

        while self.dealer.calculate_score() < 17:
            card = self.deck.deal_card()
            self.dealer.take_card(card)

            print(f"Dealer draws: {card}")
            print("Dealer's new score:", self.dealer.calculate_score())

        if self.dealer.calculate_score() > 21:
            print("Dealer busted! You win.")
        else:
            print("Dealer stands.")

    def check_winner(self):
        player_score = self.player.calculate_score()
        dealer_score = self.dealer.calculate_score()

        print("\nFinal Result")
        print("----------------")
        print(f"Player Score: {player_score}")
        print(f"Dealer Score: {dealer_score}")

        if dealer_score > 21:
            print("Dealer busted! You win!")

        elif player_score > dealer_score:
            print("You win!")

        elif dealer_score > player_score:
            print("Dealer wins!")

        else:
            print("It's a tie!")
    
    
    def play(self):
        print("===== WELCOME TO BLACKJACK =====")

        self.deal_initial_cards()

        if self.player_turn():
            self.dealer_turn()
            self.check_winner()

game = BlackjackGame()
game.play()