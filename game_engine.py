# ============================================================
# game_engine.py — Blackjack Game Engine (Web-Adapted)
# ============================================================
# This file adapts the original main.py game classes for web use.
# Core logic (scoring, ace handling, dealer AI) is IDENTICAL
# to the original code. The only changes:
#   - Removed print() and input() calls
#   - Added to_dict() methods for JSON serialization
#   - Methods return data instead of printing to console
#   - Added game state management (game_over, result, message)
# ============================================================

import random


class Card:
    """Represents a single playing card. (Same as original main.py)"""

    def __init__(self, suits, rank):
        self.suits = suits
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suits}"

    # --- NEW: Added for web serialization ---
    def to_dict(self):
        """Convert card to a dictionary for JSON response."""
        suit_symbols = {
            "Hearts": "♥", "Diamonds": "♦",
            "Clubs": "♣", "Spades": "♠"
        }
        rank_short = {
            "Two": "2", "Three": "3", "Four": "4", "Five": "5",
            "Six": "6", "Seven": "7", "Eight": "8", "Nine": "9",
            "Ten": "10", "Jack": "J", "Queen": "Q", "King": "K", "Ace": "A"
        }
        return {
            "suit": self.suits,
            "rank": self.rank,
            "suit_symbol": suit_symbols[self.suits],
            "rank_short": rank_short[self.rank],
            "color": "red" if self.suits in ["Hearts", "Diamonds"] else "black"
        }


class Deck:
    """Represents a 52-card deck. (Same as original main.py)"""

    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = [
            "Two", "Three", "Four", "Five", "Six", "Seven",
            "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"
        ]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()


class Player:
    """Represents a player (or dealer). (Same as original main.py)"""

    def __init__(self, name):
        self.name = name
        self.hand = []

    def take_card(self, card):
        self.hand.append(card)

    # --- ORIGINAL: showhand() used print(), removed for web ---
    # def showhand(self):
    #     for card in self.hand:
    #         print(card)

    def calculate_score(self):
        """Calculate hand score with Ace handling. (IDENTICAL to original)"""
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

        # Convert Ace from 11 to 1 if needed (IDENTICAL to original)
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    # --- NEW: Added for web serialization ---
    def hand_to_dict(self):
        """Convert hand to a list of card dicts."""
        return [card.to_dict() for card in self.hand]


class BlackjackGame:
    """
    Main game controller. (Adapted from original main.py)

    Original used print()/input() for console interaction.
    This version returns game state as dictionaries for the web API.
    Game logic (dealer hits below 17, ace rules, win conditions)
    is IDENTICAL to the original.
    """

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player = Player("Player")
        self.dealer = Player("Dealer")

        # --- NEW: State tracking for web ---
        self.game_over = False
        self.result = None  # "player_wins", "dealer_wins", "tie"
        self.message = ""

    def deal_initial_cards(self):
        """Deal 2 cards each. (Same logic as original)"""
        for _ in range(2):
            self.player.take_card(self.deck.deal_card())
            self.dealer.take_card(self.deck.deal_card())

        # Check for natural blackjack
        if self.player.calculate_score() == 21:
            self.game_over = True
            if self.dealer.calculate_score() == 21:
                self.result = "tie"
                self.message = "Both have Blackjack! It's a push!"
            else:
                self.result = "player_wins"
                self.message = "Blackjack! You win!"

    def player_hit(self):
        """
        Player draws a card. (Replaces original player_turn loop)
        Original: while loop with input("Hit or Stand?")
        Web version: called once per hit via API
        """
        if self.game_over:
            return self.get_state()

        card = self.deck.deal_card()
        self.player.take_card(card)

        # Check if player busts (IDENTICAL logic to original)
        if self.player.calculate_score() > 21:
            self.game_over = True
            self.result = "dealer_wins"
            self.message = "You busted! Dealer wins."
        elif self.player.calculate_score() == 21:
            # Auto-stand on 21
            return self.player_stand()

        return self.get_state()

    def player_stand(self):
        """
        Player stands, dealer plays. (Same logic as original dealer_turn)
        Original: dealer hits while score < 17
        """
        if self.game_over:
            return self.get_state()

        # Dealer's turn — hits below 17 (IDENTICAL to original)
        while self.dealer.calculate_score() < 17:
            self.dealer.take_card(self.deck.deal_card())

        self.game_over = True

        # Determine winner (IDENTICAL logic to original check_winner)
        player_score = self.player.calculate_score()
        dealer_score = self.dealer.calculate_score()

        if dealer_score > 21:
            self.result = "player_wins"
            self.message = "Dealer busted! You win!"
        elif player_score > dealer_score:
            self.result = "player_wins"
            self.message = "You win!"
        elif dealer_score > player_score:
            self.result = "dealer_wins"
            self.message = "Dealer wins!"
        else:
            self.result = "tie"
            self.message = "It's a tie!"

        return self.get_state()

    def get_state(self):
        """
        Return the full game state as a dictionary (NEW for web).
        During player's turn: dealer's second card is hidden.
        After game over: all cards revealed.
        """
        # Dealer hand: hide second card if game is still ongoing
        if self.game_over:
            dealer_hand = self.dealer.hand_to_dict()
            dealer_score = self.dealer.calculate_score()
        else:
            # Show only the first card, hide the rest
            dealer_hand = [self.dealer.hand[0].to_dict(), {"hidden": True}]
            # Show only the visible card's value
            first_card = self.dealer.hand[0]
            temp_player = Player("temp")
            temp_player.take_card(first_card)
            dealer_score = temp_player.calculate_score()

        return {
            "player_hand": self.player.hand_to_dict(),
            "player_score": self.player.calculate_score(),
            "dealer_hand": dealer_hand,
            "dealer_score": dealer_score,
            "dealer_score_hidden": not self.game_over,
            "game_over": self.game_over,
            "result": self.result,
            "message": self.message
        }
