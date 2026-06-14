// ============================================================
// game.js — Blackjack Frontend Game Logic
// ============================================================
// Communicates with the Flask API using fetch()
// Renders cards, manages animations, and handles UI state
// ============================================================

// ─── DOM Elements ────────────────────────────────────
const dealerCardsEl = document.getElementById('dealer-cards');
const playerCardsEl = document.getElementById('player-cards');
const dealerScoreEl = document.getElementById('dealer-score');
const playerScoreEl = document.getElementById('player-score');
const dealerScoreBadge = document.getElementById('dealer-score-badge');
const playerScoreBadge = document.getElementById('player-score-badge');
const btnHit = document.getElementById('btn-hit');
const btnStand = document.getElementById('btn-stand');
const btnNewGame = document.getElementById('btn-new-game');
const messageBar = document.getElementById('message-bar');
const messageText = document.getElementById('message-text');
const resultOverlay = document.getElementById('result-overlay');
const resultEmoji = document.getElementById('result-emoji');
const resultTitle = document.getElementById('result-title');
const resultPlayerScore = document.getElementById('result-player-score');
const resultDealerScore = document.getElementById('result-dealer-score');

// ─── Game State ──────────────────────────────────────
let currentState = null;
let isAnimating = false;

// ─── API Functions ───────────────────────────────────

async function apiNewGame() {
    const res = await fetch('/api/new-game', { method: 'POST' });
    return await res.json();
}

async function apiHit() {
    const res = await fetch('/api/hit', { method: 'POST' });
    return await res.json();
}

async function apiStand() {
    const res = await fetch('/api/stand', { method: 'POST' });
    return await res.json();
}

// ─── Card Rendering ──────────────────────────────────

function createCardElement(cardData, isNew = false) {
    const card = document.createElement('div');
    
    if (cardData.hidden) {
        // Hidden card (dealer's face-down card)
        card.className = 'card card-hidden';
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-back-face">
                    <div class="card-back-pattern"></div>
                </div>
            </div>
        `;
    } else {
        // Visible card
        const isFace = ['J', 'Q', 'K'].includes(cardData.rank_short);
        card.className = `card ${cardData.color}${isFace ? ' face-card' : ''}${isNew ? ' new-card' : ''}`;
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-face">
                    <div class="card-corner top-left">
                        <span class="rank">${cardData.rank_short}</span>
                        <span class="suit">${cardData.suit_symbol}</span>
                    </div>
                    <div class="card-center">
                        <span class="suit-large">${cardData.suit_symbol}</span>
                    </div>
                    <div class="card-corner bottom-right">
                        <span class="rank">${cardData.rank_short}</span>
                        <span class="suit">${cardData.suit_symbol}</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    return card;
}

function renderCards(cards, containerEl, allNew = false) {
    containerEl.innerHTML = '';
    cards.forEach((card, index) => {
        const cardEl = createCardElement(card, allNew);
        containerEl.appendChild(cardEl);
    });
}

function addNewCard(cardData, containerEl) {
    const cardEl = createCardElement(cardData, true);
    containerEl.appendChild(cardEl);
}

// ─── Score Update ────────────────────────────────────

function updateScore(element, value, badge) {
    const displayValue = (typeof value === 'number') ? value : value;
    element.textContent = displayValue;
    
    // Pop animation
    element.classList.remove('pop');
    void element.offsetWidth; // Trigger reflow
    element.classList.add('pop');
    
    // Highlight badge if score is 21 (blackjack!)
    if (value === 21) {
        badge.classList.add('highlight');
    } else {
        badge.classList.remove('highlight');
    }
}

// ─── UI State Management ─────────────────────────────

function setButtonsEnabled(enabled) {
    btnHit.disabled = !enabled;
    btnStand.disabled = !enabled;
}

function setMessage(text, type = '') {
    messageText.textContent = text;
    messageBar.className = 'message-bar';
    if (type) {
        messageBar.classList.add(type);
    }
}

// ─── Game Handlers ───────────────────────────────────

async function handleNewGame() {
    if (isAnimating) return;
    isAnimating = true;
    
    // Hide result overlay if showing
    hideResult();
    
    // Clear the table
    dealerCardsEl.innerHTML = '';
    playerCardsEl.innerHTML = '';
    dealerScoreEl.textContent = '0';
    playerScoreEl.textContent = '0';
    dealerScoreBadge.classList.remove('highlight');
    playerScoreBadge.classList.remove('highlight');
    
    setMessage('Dealing cards...', 'active');
    setButtonsEnabled(false);
    
    try {
        const state = await apiNewGame();
        currentState = state;
        
        // Short delay for dramatic effect, then render
        await delay(300);
        
        // Render initial cards
        renderCards(state.dealer_hand, dealerCardsEl, true);
        renderCards(state.player_hand, playerCardsEl, true);
        
        // Update scores with a small delay
        await delay(500);
        updateScore(dealerScoreEl, state.dealer_score_hidden ? state.dealer_score + '+?' : state.dealer_score, dealerScoreBadge);
        updateScore(playerScoreEl, state.player_score, playerScoreBadge);
        
        if (state.game_over) {
            // Natural blackjack or immediate result
            setMessage(state.message, state.result === 'player_wins' ? 'win' : 'bust');
            await delay(1200);
            showResult(state);
        } else {
            setMessage('Your turn — Hit or Stand?', 'active');
            setButtonsEnabled(true);
        }
    } catch (err) {
        setMessage('Error starting game. Try again.', 'bust');
        console.error('New game error:', err);
    }
    
    isAnimating = false;
}

async function handleHit() {
    if (isAnimating) return;
    isAnimating = true;
    setButtonsEnabled(false);
    
    try {
        const state = await apiHit();
        currentState = state;
        
        // Get the new card (last card in player's hand)
        const newCard = state.player_hand[state.player_hand.length - 1];
        addNewCard(newCard, playerCardsEl);
        
        await delay(300);
        updateScore(playerScoreEl, state.player_score, playerScoreBadge);
        
        if (state.game_over) {
            // Player busted or got 21
            // Reveal dealer cards
            await delay(600);
            renderCards(state.dealer_hand, dealerCardsEl, false);
            updateScore(dealerScoreEl, state.dealer_score, dealerScoreBadge);
            
            const msgType = state.result === 'player_wins' ? 'win' : 'bust';
            setMessage(state.message, msgType);
            
            await delay(1200);
            showResult(state);
        } else {
            setMessage(`Score: ${state.player_score} — Hit or Stand?`, 'active');
            setButtonsEnabled(true);
        }
    } catch (err) {
        setMessage('Error. Try again.', 'bust');
        setButtonsEnabled(true);
        console.error('Hit error:', err);
    }
    
    isAnimating = false;
}

async function handleStand() {
    if (isAnimating) return;
    isAnimating = true;
    setButtonsEnabled(false);
    
    setMessage('You stand. Dealer\'s turn...', 'active');
    
    try {
        const state = await apiStand();
        currentState = state;
        
        // Reveal dealer's hidden card with animation
        await delay(600);
        renderCards(state.dealer_hand, dealerCardsEl, true);
        updateScore(dealerScoreEl, state.dealer_score, dealerScoreBadge);
        
        // Update player score display too
        updateScore(playerScoreEl, state.player_score, playerScoreBadge);
        
        await delay(800);
        
        const msgType = state.result === 'player_wins' ? 'win' : 
                        state.result === 'tie' ? 'active' : 'bust';
        setMessage(state.message, msgType);
        
        await delay(1000);
        showResult(state);
    } catch (err) {
        setMessage('Error. Try again.', 'bust');
        console.error('Stand error:', err);
    }
    
    isAnimating = false;
}

// ─── Result Overlay ──────────────────────────────────

function showResult(state) {
    // Set result content
    resultPlayerScore.textContent = state.player_score;
    resultDealerScore.textContent = state.dealer_score;
    
    // Remove previous result classes
    resultOverlay.classList.remove('win', 'lose', 'tie');
    
    if (state.result === 'player_wins') {
        resultEmoji.textContent = '🏆';
        resultTitle.textContent = state.message;
        resultOverlay.classList.add('win');
        launchConfetti();
    } else if (state.result === 'dealer_wins') {
        resultEmoji.textContent = '😔';
        resultTitle.textContent = state.message;
        resultOverlay.classList.add('lose');
    } else {
        resultEmoji.textContent = '🤝';
        resultTitle.textContent = state.message;
        resultOverlay.classList.add('tie');
    }
    
    resultOverlay.classList.add('visible');
}

function hideResult() {
    resultOverlay.classList.remove('visible');
    // Clear confetti
    document.querySelectorAll('.confetti').forEach(el => el.remove());
}

// ─── Confetti Effect ─────────────────────────────────

function launchConfetti() {
    const colors = ['#d4a843', '#f0d078', '#27ae60', '#e74c3c', '#3498db', '#f39c12', '#9b59b6'];
    const shapes = ['■', '●', '▲', '♦', '★'];
    
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.textContent = shapes[Math.floor(Math.random() * shapes.length)];
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.color = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.fontSize = (Math.random() * 14 + 6) + 'px';
        confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
        confetti.style.animationDelay = (Math.random() * 1.5) + 's';
        document.body.appendChild(confetti);
        
        // Clean up after animation
        setTimeout(() => confetti.remove(), 5000);
    }
}

// ─── Ambient Particles ───────────────────────────────

function createParticles() {
    const container = document.getElementById('particles');
    const particleCount = 15;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (Math.random() * 6 + 6) + 's';
        container.appendChild(particle);
    }
}

// ─── Utility ─────────────────────────────────────────

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ─── Keyboard Shortcuts ──────────────────────────────

document.addEventListener('keydown', (e) => {
    if (e.key === 'h' || e.key === 'H') {
        if (!btnHit.disabled) handleHit();
    } else if (e.key === 's' || e.key === 'S') {
        if (!btnStand.disabled) handleStand();
    } else if (e.key === 'n' || e.key === 'N') {
        handleNewGame();
    } else if (e.key === 'Escape') {
        hideResult();
    }
});

// ─── Initialize ──────────────────────────────────────

createParticles();
setMessage('Press NEW GAME to start playing!  (Keyboard: N = New, H = Hit, S = Stand)', '');
