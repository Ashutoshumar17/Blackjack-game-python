# 📘 Blackjack Web Game — Full Documentation

> **How a Python Console Game Was Converted Into a Web Application**

This document explains the complete architecture, how the original Python code was adapted as a backend, and how every piece fits together.

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture — How It Works](#2-architecture--how-it-works)
3. [How Python Became the Backend](#3-how-python-became-the-backend)
4. [Original vs Web Code — Side-by-Side Comparison](#4-original-vs-web-code--side-by-side-comparison)
5. [API Reference](#5-api-reference)
6. [Frontend — How the UI Works](#6-frontend--how-the-ui-works)
7. [Tech Stack](#7-tech-stack)
8. [How to Run](#8-how-to-run)
9. [File Structure](#9-file-structure)

---

## 1. Project Overview

### The Original Game (`main.py`)
The original Blackjack game was a **console-based Python program**. It used:
- `print()` statements to show cards and scores
- `input()` to ask the player to Hit or Stand
- All interaction happened in the terminal/command prompt

### The Problem
Console games can't be played in a web browser. We needed a way to:
1. Keep the Python game logic (it already works perfectly!)
2. Show a beautiful visual interface in the browser
3. Let the browser communicate with Python

### The Solution
We used **Flask** (a Python web framework) to turn the Python game into a **web server**. The browser sends requests ("I want to hit"), Python processes the game logic, and sends back the result as JSON data. The browser then displays it beautifully.

---

## 2. Architecture — How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR BROWSER                          │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  index.html  +  style.css  +  game.js            │   │
│  │                                                    │   │
│  │  • Displays cards, scores, buttons                │   │
│  │  • Sends API requests when you click Hit/Stand    │   │
│  │  • Receives JSON data and renders it visually     │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                                │
└─────────────────────────┼────────────────────────────────┘
                          │  HTTP Requests (fetch API)
                          │
                          │  POST /api/new-game
                          │  POST /api/hit
                          │  POST /api/stand
                          │  GET  /api/game-state
                          │
┌─────────────────────────┼────────────────────────────────┐
│                  FLASK SERVER (Python)                     │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐   │
│  │  app.py                                           │   │
│  │                                                    │   │
│  │  • Receives HTTP requests                         │   │
│  │  • Creates/manages game instances                 │   │
│  │  • Returns JSON responses                         │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐   │
│  │  game_engine.py                                   │   │
│  │                                                    │   │
│  │  • Card class        (from your main.py)          │   │
│  │  • Deck class        (from your main.py)          │   │
│  │  • Player class      (from your main.py)          │   │
│  │  • BlackjackGame     (from your main.py)          │   │
│  │                                                    │   │
│  │  Same logic, but returns data instead of printing │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### The Flow (Step by Step)

1. **You open `http://localhost:5000`** → Flask serves `index.html`
2. **You click "NEW GAME"** → JavaScript sends `POST /api/new-game`
3. **Flask receives the request** → Creates a new `BlackjackGame`, deals 2 cards each
4. **Flask sends back JSON** → `{ player_hand: [...], dealer_hand: [...], scores, etc. }`
5. **JavaScript receives JSON** → Renders beautiful card elements in the browser
6. **You click "HIT"** → JavaScript sends `POST /api/hit`
7. **Flask calls `game.player_hit()`** → Your Python code draws a card, checks for bust
8. **Flask sends updated state** → JavaScript adds the new card with animation
9. **You click "STAND"** → Flask runs dealer AI (hits below 17), determines winner
10. **Result displayed** → Winner overlay with confetti (if you win!)

---

## 3. How Python Became the Backend

### What is a Backend?
A **backend** is the server-side code that runs on your computer (not in the browser). It handles the game logic, data processing, and sends results to the browser.

### What is Flask?
**Flask** is a lightweight Python library that turns your Python code into a web server. It can:
- Listen for HTTP requests (like when a browser visits a URL)
- Run Python code in response
- Send back HTML pages or JSON data

### What Was Changed (and What Wasn't)

#### ✅ KEPT IDENTICAL (Game Logic)
These parts of your code were **not changed at all**:

| Feature | Your Original Code | Web Version |
|---------|-------------------|-------------|
| Card creation | `Card(suits, rank)` | Same |
| Deck building | 52 cards, 4 suits × 13 ranks | Same |
| Shuffling | `random.shuffle(self.cards)` | Same |
| Dealing | `self.cards.pop()` | Same |
| Score calculation | Face=10, Ace=11/1, number=value | Same |
| Ace handling | While score>21 and aces>0, subtract 10 | Same |
| Dealer AI | Hits while score < 17 | Same |
| Win conditions | Compare scores, check bust | Same |

#### 🔄 CHANGED (Input/Output Only)

| Original (`main.py`) | Web (`game_engine.py`) | Why |
|---|---|---|
| `print("Your cards:")` | Returns data in `get_state()` | Browser shows cards visually, no need to print |
| `input("Hit or Stand?")` | Separate `player_hit()` and `player_stand()` methods | Buttons replace text input |
| `print(f"Dealer draws: {card}")` | Included in JSON response | JavaScript renders the card |
| Game runs as one continuous loop | Game state stored between API calls | Web is request-based, not loop-based |

#### ➕ ADDED (New for Web)

| Addition | Purpose |
|---|---|
| `to_dict()` on Card | Converts card to JSON: `{"rank": "Ace", "suit": "Hearts", "suit_symbol": "♥", ...}` |
| `hand_to_dict()` on Player | Converts entire hand to a list of card dicts |
| `get_state()` on BlackjackGame | Returns complete game state as a dictionary |
| `game_over`, `result`, `message` | Track game state between requests |
| Dealer's hidden card logic | During player's turn, only dealer's first card is visible |

### The Key Insight

> **Your Python code IS the game.** Flask just makes it accessible from a browser.
> Think of it like this: your Python code is the **engine** of a car. Flask is the **steering wheel and dashboard** — it lets someone drive the car without touching the engine directly.

---

## 4. Original vs Web Code — Side-by-Side Comparison

### Card Class

```python
# ═══ ORIGINAL (main.py) ═══
class Card:
    def __init__(self, suits, rank):
        self.suits = suits
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suits}"


# ═══ WEB VERSION (game_engine.py) ═══
class Card:
    def __init__(self, suits, rank):      # ← SAME
        self.suits = suits                 # ← SAME
        self.rank = rank                   # ← SAME

    def __str__(self):                     # ← SAME
        return f"{self.rank} of {self.suits}"

    def to_dict(self):                     # ← NEW: for JSON
        return {
            "suit": self.suits,
            "rank": self.rank,
            "suit_symbol": {"Hearts":"♥", ...}[self.suits],
            "rank_short": {"Ace":"A", "King":"K", ...}[self.rank],
            "color": "red" if self.suits in ["Hearts","Diamonds"] else "black"
        }
```

### Player Turn (The Biggest Change)

```python
# ═══ ORIGINAL (main.py) ═══
def player_turn(self):
    while True:                              # Loop until bust or stand
        print("Your current hand:")
        self.player.showhand()
        print("Score:", self.player.calculate_score())

        if self.player.calculate_score() > 21:
            print("You busted! Dealer wins.")
            return False

        choice = input("Hit or Stand? ")     # Wait for text input

        if choice == "hit":
            card = self.deck.deal_card()
            self.player.take_card(card)
            print(f"You got: {card}")
        elif choice == "stand":
            print("You stand.")
            return True


# ═══ WEB VERSION (game_engine.py) ═══
# The loop is GONE — replaced by two separate methods
# Each method is called once per button click

def player_hit(self):                        # Called when "HIT" clicked
    card = self.deck.deal_card()             # ← Same logic
    self.player.take_card(card)              # ← Same logic

    if self.player.calculate_score() > 21:   # ← Same bust check
        self.game_over = True
        self.result = "dealer_wins"
        self.message = "You busted! Dealer wins."

    return self.get_state()                  # ← Returns data (no print)

def player_stand(self):                      # Called when "STAND" clicked
    while self.dealer.calculate_score() < 17:  # ← Same dealer AI
        self.dealer.take_card(self.deck.deal_card())
    # ... determine winner (same logic) ...
    return self.get_state()                  # ← Returns data (no print)
```

### How the API Bridges the Gap

```python
# ═══ app.py — The Bridge ═══

@app.route('/api/hit', methods=['POST'])
def hit():
    game = games[session['game_id']]    # Get the game instance
    state = game.player_hit()            # Call YOUR game logic
    return jsonify(state)                # Send result as JSON
```

```javascript
// ═══ game.js — The Browser Side ═══

async function handleHit() {
    const state = await fetch('/api/hit', { method: 'POST' })
        .then(res => res.json());

    // state = { player_hand: [...], player_score: 18, ... }
    // Now render it visually!
    addNewCard(state.player_hand.at(-1), playerCardsEl);
    updateScore(playerScoreEl, state.player_score);
}
```

---

## 5. API Reference

### `POST /api/new-game`
Starts a new game. Creates a fresh deck, shuffles, deals 2 cards to player and dealer.

**Response:**
```json
{
    "player_hand": [
        {"suit": "Hearts", "rank": "Ace", "suit_symbol": "♥", "rank_short": "A", "color": "red"},
        {"suit": "Spades", "rank": "King", "suit_symbol": "♠", "rank_short": "K", "color": "black"}
    ],
    "player_score": 21,
    "dealer_hand": [
        {"suit": "Clubs", "rank": "Seven", "suit_symbol": "♣", "rank_short": "7", "color": "black"},
        {"hidden": true}
    ],
    "dealer_score": 7,
    "dealer_score_hidden": true,
    "game_over": false,
    "result": null,
    "message": ""
}
```

### `POST /api/hit`
Player draws one card. Checks for bust (score > 21).

### `POST /api/stand`
Player stands. Dealer plays (hits while < 17). Determines winner.

### `GET /api/game-state`
Returns current game state without making any moves.

---

## 6. Frontend — How the UI Works

### HTML (`templates/index.html`)
- **Dealer section**: Shows dealer's cards and score
- **Player section**: Shows your cards and score
- **Controls**: HIT, STAND, NEW GAME buttons
- **Result overlay**: Win/lose/tie popup with scores

### CSS (`static/css/style.css`)
- **Casino theme**: Dark green felt background with gold accents
- **Glassmorphism**: Frosted glass effect on containers
- **Playing cards**: CSS-only cards with suit symbols (♠ ♥ ♦ ♣)
- **Animations**: Card dealing slide-in, score pop, confetti on win
- **Responsive**: Works on both desktop and mobile

### JavaScript (`static/js/game.js`)
- **API calls**: Uses `fetch()` to communicate with Flask
- **Card rendering**: Dynamically creates card elements from JSON
- **Animations**: Manages card deal animations and result celebrations
- **Keyboard shortcuts**: H = Hit, S = Stand, N = New Game

---

## 7. Tech Stack

| Technology | Role | Why This Choice |
|---|---|---|
| **Python** | Game logic (backend) | Your original code was in Python |
| **Flask** | Web server framework | Simplest way to serve Python as a web backend. Minimal setup. |
| **HTML5** | Page structure | Standard web markup |
| **CSS3** | Visual styling | Casino-themed design with animations |
| **JavaScript** | Browser logic | Handles user interaction and API calls |
| **JSON** | Data format | Standard way to send data between server and browser |

### What is JSON?
JSON (JavaScript Object Notation) is a text format for sending data. Example:
```json
{"rank": "Ace", "suit": "Hearts", "score": 21}
```
Flask converts Python dictionaries to JSON. JavaScript can read JSON natively.

### What is an API?
API (Application Programming Interface) is a set of URLs that your server responds to. Instead of serving web pages, API endpoints serve **data** (JSON). The browser's JavaScript code calls these URLs to get game data.

---

## 8. How to Run

### Prerequisites
- Python 3.7+ installed
- pip (Python package manager)

### Setup Steps

1. **Open terminal/command prompt** in the project folder:
   ```
   cd "c:\College softwares\vs code\python\Black Jack"
   ```

2. **Install Flask**:
   ```
   pip install flask
   ```

3. **Run the server**:
   ```
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

5. **Play!** Click NEW GAME to start.

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `N` | New Game |
| `H` | Hit |
| `S` | Stand |
| `Esc` | Close result popup |

---

## 9. File Structure

```
Black Jack/
│
├── main.py              ← Your ORIGINAL code (untouched, preserved)
│
├── game_engine.py       ← Your game logic adapted for web
│                          (same classes, returns data instead of printing)
│
├── app.py               ← Flask web server
│                          (creates API endpoints, manages game sessions)
│
├── requirements.txt     ← Python dependencies (just Flask)
│
├── templates/
│   └── index.html       ← Game UI (HTML structure)
│
├── static/
│   ├── css/
│   │   └── style.css    ← Casino-themed visual design
│   └── js/
│       └── game.js      ← Browser-side game logic
│
└── DOCUMENTATION.md     ← This file!
```

---

## Summary

> Your Python Blackjack game logic is the **brain**. Flask is the **nervous system** that connects it to the browser. HTML/CSS/JS are the **face** — making it look and feel like a real casino game.
>
> The core game rules (scoring, ace handling, dealer AI, win conditions) are **100% identical** to your original `main.py`. We just changed how the game talks to the player — from text in a terminal to a beautiful visual interface in a browser.
