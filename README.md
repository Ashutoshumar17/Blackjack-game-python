# 🃏 Blackjack — Casino Royale

A premium web-based Blackjack card game built with **Python (Flask)** backend and a stunning **casino-themed** frontend.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Full Blackjack game** — Hit, Stand, Bust, Dealer AI, Ace handling
- **Casino-themed dark UI** — Emerald felt, gold accents, glassmorphism
- **Animated cards** — Deal animations, card flip, score pop effects
- **Confetti celebration** — Win effects with particle confetti
- **Keyboard shortcuts** — H = Hit, S = Stand, N = New Game
- **Responsive design** — Works on desktop and mobile
- **Python backend** — Game logic runs on Flask server

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Ashutoshumar17/blackjack-casino-royale.git
cd blackjack-casino-royale

# 2. Install dependencies
pip install flask

# 3. Run the server
python app.py

# 4. Open in browser
# Go to http://localhost:5000
```

---

## 🏗️ Architecture

```
Browser (HTML/CSS/JS)  ←→  Flask API (Python)  ←→  Game Engine (Your Python classes)
```

The original Python console game (`main.py`) was adapted into a web app:
- **`game_engine.py`** — Same game logic, returns data instead of printing
- **`app.py`** — Flask server with REST API endpoints
- **Frontend** — Renders cards and handles user interaction

See [DOCUMENTATION.md](DOCUMENTATION.md) for full technical details.

---

## 📁 Project Structure

```
├── main.py              # Original console game (preserved)
├── game_engine.py       # Web-adapted game engine
├── app.py               # Flask web server
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Game UI
├── static/
│   ├── css/style.css    # Casino theme
│   └── js/game.js       # Frontend logic
├── DOCUMENTATION.md     # Full technical documentation
└── README.md            # This file
```

---

## 🎮 How to Play

1. Click **NEW GAME** to start
2. You and the dealer each get 2 cards
3. **HIT** to draw another card
4. **STAND** to keep your hand — dealer plays automatically
5. Closest to 21 without going over wins!

### Card Values
| Card | Value |
|------|-------|
| 2-10 | Face value |
| J, Q, K | 10 |
| Ace | 11 (or 1 if would bust) |

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| Python 3.12 | Game logic |
| Flask | Web server & API |
| HTML5 | Page structure |
| CSS3 | Casino-themed styling |
| JavaScript | Browser-side logic |

---

Made with ♠ by Ashutosh
