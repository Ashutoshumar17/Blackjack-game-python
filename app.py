# ============================================================
# app.py — Flask Web Server for Blackjack
# ============================================================
# This file creates a web server that:
#   1. Serves the game HTML page
#   2. Provides API endpoints for game actions
#   3. Stores game instances server-side (keyed by session)
# ============================================================

from flask import Flask, render_template, jsonify, session
import uuid
from game_engine import BlackjackGame

app = Flask(__name__)
app.secret_key = 'blackjack-secret-key-2026'

# Store active games server-side (game_id -> BlackjackGame instance)
# In production, you'd use Redis or a database. For local play, this is fine.
games = {}


@app.route('/')
def index():
    """Serve the main game page."""
    return render_template('index.html')


@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game: create deck, shuffle, deal 2 cards each."""
    # Clean up old game if exists
    old_game_id = session.get('game_id')
    if old_game_id and old_game_id in games:
        del games[old_game_id]

    # Create new game
    game_id = str(uuid.uuid4())
    session['game_id'] = game_id

    game = BlackjackGame()
    game.deal_initial_cards()
    games[game_id] = game

    return jsonify(game.get_state())


@app.route('/api/hit', methods=['POST'])
def hit():
    """Player draws a card."""
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    game = games[game_id]
    state = game.player_hit()
    return jsonify(state)


@app.route('/api/stand', methods=['POST'])
def stand():
    """Player stands. Dealer plays, then determine winner."""
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    game = games[game_id]
    state = game.player_stand()
    return jsonify(state)


@app.route('/api/game-state', methods=['GET'])
def game_state():
    """Get the current game state."""
    game_id = session.get('game_id')
    if not game_id or game_id not in games:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    game = games[game_id]
    return jsonify(game.get_state())


if __name__ == '__main__':
    print("\n[*] Blackjack Server starting...")
    print("[*] Open http://localhost:5000 in your browser to play!\n")
    app.run(debug=True, port=5000)
