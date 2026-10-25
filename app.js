/**
 * VALORANT // Replik Tahmin Oyunu - Application Logic
 * %100 Doğrudan Oyun İçi Orijinal Karakter Sesleri
 */

(function () {
    'use strict';

    // State Variables
    let agents = {};
    let quotes = [];
    let unplayedQuotes = [];
    let currentQuote = null;
    let currentAgent = null;
    let isRevealed = false;
    let isPlayingAudio = false;
    let sfxEnabled = true;

    let score = parseInt(localStorage.getItem('val_score') || '0', 10);
    let streak = parseInt(localStorage.getItem('val_streak') || '0', 10);
    let bestStreak = parseInt(localStorage.getItem('val_best_streak') || '0', 10);
    let totalPlayed = 0;

    let activeAudio = null;

    // DOM Elements
    const quoteTextEl = document.getElementById('quote-text');
    const quoteCategoryEl = document.getElementById('quote-category');
    const cardCounterEl = document.getElementById('card-counter');
    const voiceHintBtn = document.getElementById('voice-hint-btn');
    const voiceBtnText = document.getElementById('voice-btn-text');
    const revealBtn = document.getElementById('reveal-btn');
    const agentRevealCard = document.getElementById('agent-reveal-card');
    const scoringActions = document.getElementById('scoring-actions');
    const agentPortraitEl = document.getElementById('agent-portrait');
    const agentNameEl = document.getElementById('agent-name');
    const agentRoleEl = document.getElementById('agent-role');
    const agentOriginEl = document.getElementById('agent-origin');
    const agentGlowBg = document.getElementById('agent-glow-bg');
    
    const btnCorrect = document.getElementById('btn-correct');
    const btnWrong = document.getElementById('btn-wrong');
    const nextBtn = document.getElementById('next-btn');

    const scoreValEl = document.getElementById('score-val');
    const streakValEl = document.getElementById('streak-val');
    const bestValEl = document.getElementById('best-val');
    const sfxToggleBtn = document.getElementById('sfx-toggle-btn');
    const sfxIcon = document.getElementById('sfx-icon');

    // Web Audio Context for UI Sound Effects
    let audioCtx = null;
    function getAudioCtx() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) audioCtx = new AudioContext();
        }
        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }
        return audioCtx;
    }

    // Sound FX Synthesizers (Futuristic UI Sounds)
    function playSfx(type) {
        if (!sfxEnabled) return;
        try {
            const ctx = getAudioCtx();
            if (!ctx) return;
            const now = ctx.currentTime;

            if (type === 'click') {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(600, now);
                osc.frequency.exponentialRampToValueAtTime(300, now + 0.05);
                gain.gain.setValueAtTime(0.2, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.05);
            } else if (type === 'reveal') {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(260, now);
                osc.frequency.exponentialRampToValueAtTime(780, now + 0.2);
                gain.gain.setValueAtTime(0.3, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.2);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.2);
            } else if (type === 'success') {
                [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, now + i * 0.08);
                    gain.gain.setValueAtTime(0.25, now + i * 0.08);
                    gain.gain.exponentialRampToValueAtTime(0.01, now + (i + 1) * 0.12);
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.start(now + i * 0.08);
                    osc.stop(now + (i + 1) * 0.12);
                });
            } else if (type === 'fail') {
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(180, now);
                osc.frequency.linearRampToValueAtTime(110, now + 0.25);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + 0.25);
            }
        } catch (e) {
            console.warn("SFX error:", e);
        }
    }

    // Initialize Data
    async function init() {
        try {
            updateStatsUI();

            const [agentsRes, quotesRes] = await Promise.all([
                fetch('data/agents.json?v=' + Date.now()),
                fetch('data/quotes.json?v=' + Date.now())
            ]);

            agents = await agentsRes.json();
            quotes = await quotesRes.json();

            resetQuoteQueue();
            loadNextQuote();
        } catch (err) {
            console.error("Veri yüklenirken hata:", err);
            quoteTextEl.textContent = "Veriler yüklenemedi. Lütfen sayfayı yenileyin.";
        }
    }

    // Shuffled Queue (No repeat until all quotes played)
    function resetQuoteQueue() {
        unplayedQuotes = [...quotes];
        for (let i = unplayedQuotes.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [unplayedQuotes[i], unplayedQuotes[j]] = [unplayedQuotes[j], unplayedQuotes[i]];
        }
    }

    // Load Next Quote Card
    function loadNextQuote() {
        stopVoiceAudio();

        if (unplayedQuotes.length === 0) {
            resetQuoteQueue();
        }

        currentQuote = unplayedQuotes.pop();
        totalPlayed++;

        // Find agent object
        const agentKey = Object.keys(agents).find(k => 
            k.toLowerCase() === currentQuote.agent.toLowerCase() ||
            agents[k].name.toLowerCase() === currentQuote.agent.toLowerCase()
        );
        currentAgent = agentKey ? agents[agentKey] : {
            name: currentQuote.agent,
            role: "Ajan",
            portrait: "https://media.valorant-api.com/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png"
        };

        // Reset UI State
        isRevealed = false;
        quoteTextEl.textContent = currentQuote.quote;
        quoteCategoryEl.textContent = currentQuote.category || "VALORANT REPLİK";
        cardCounterEl.textContent = `#${totalPlayed}`;

        // Reset Answer Elements
        revealBtn.style.display = 'flex';
        agentRevealCard.style.display = 'none';
        scoringActions.style.display = 'none';

        // Prepare Revealed Card info in advance
        agentNameEl.textContent = (currentAgent.displayName || currentAgent.name).toUpperCase();
        agentRoleEl.textContent = currentAgent.role || "Ajan";
        agentPortraitEl.src = currentAgent.portrait || currentAgent.icon || "";
        agentPortraitEl.onerror = () => {
            if (currentAgent.icon && agentPortraitEl.src !== currentAgent.icon) {
                agentPortraitEl.src = currentAgent.icon;
            }
        };
        agentOriginEl.textContent = currentAgent.name === 'Hush' ? 'Çin / Guangdong' : 'VALORANT PROTOKOL';

        if (currentAgent.colors && currentAgent.colors.length > 0) {
            const hex = '#' + currentAgent.colors[0].substring(0, 6);
            agentGlowBg.style.background = `radial-gradient(circle, ${hex}aa 0%, transparent 70%)`;
        } else {
            agentGlowBg.style.background = 'radial-gradient(circle, rgba(0,240,255,0.4) 0%, transparent 70%)';
        }

        // Reset Voice Button
        setPlayingState(false);
    }

    // Direct In-Game Character Voice Player (No TTS!)
    function playVoiceHint() {
        getAudioCtx();

        if (isPlayingAudio) {
            stopVoiceAudio();
            return;
        }

        if (!currentQuote || !currentQuote.audioUrl) {
            console.warn("Ses dosyası bulunamadı:", currentQuote);
            return;
        }

        playSfx('click');
        setPlayingState(true);

        const freshAudioUrl = currentQuote.audioUrl + (currentQuote.audioUrl.includes('?') ? '&' : '?') + 't=' + Date.now();
        activeAudio = new Audio(freshAudioUrl);
        activeAudio.play().then(() => {
            activeAudio.onended = () => setPlayingState(false);
            activeAudio.onerror = (e) => {
                console.warn("Ses çalma hatası:", e);
                setPlayingState(false);
            };
        }).catch((err) => {
            console.warn("Ses oynatma engellendi:", err);
            setPlayingState(false);
        });
    }

    function stopVoiceAudio() {
        if (activeAudio) {
            try {
                activeAudio.pause();
                activeAudio.currentTime = 0;
            } catch (e) {}
            activeAudio = null;
        }
        setPlayingState(false);
    }

    function setPlayingState(playing) {
        isPlayingAudio = playing;
        if (playing) {
            voiceHintBtn.classList.add('playing');
            voiceBtnText.textContent = "Orijinal Ses Çalıyor... (Durdur)";
        } else {
            voiceHintBtn.classList.remove('playing');
            voiceBtnText.textContent = "Orijinal Karakter Sesi (Dinlet)";
        }
    }

    // Reveal Agent Answer
    function revealAnswer() {
        if (isRevealed) return;
        isRevealed = true;
        playSfx('reveal');

        revealBtn.style.display = 'none';
        agentRevealCard.style.display = 'flex';
        scoringActions.style.display = 'grid';
    }

    // Scoring Handlers
    function handleCorrect() {
        playSfx('success');
        score += 10;
        streak += 1;
        if (streak > bestStreak) {
            bestStreak = streak;
        }
        saveStats();
        updateStatsUI();

        btnCorrect.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btnCorrect.style.transform = '';
            loadNextQuote();
        }, 350);
    }

    function handleWrong() {
        playSfx('fail');
        streak = 0;
        saveStats();
        updateStatsUI();

        btnWrong.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btnWrong.style.transform = '';
            loadNextQuote();
        }, 350);
    }

    function saveStats() {
        localStorage.setItem('val_score', score.toString());
        localStorage.setItem('val_streak', streak.toString());
        localStorage.setItem('val_best_streak', bestStreak.toString());
    }

    function updateStatsUI() {
        scoreValEl.textContent = score;
        streakValEl.textContent = streak;
        bestValEl.textContent = bestStreak;
    }

    // Event Listeners
    voiceHintBtn.addEventListener('click', playVoiceHint);

    revealBtn.addEventListener('click', () => {
        getAudioCtx();
        revealAnswer();
    });

    btnCorrect.addEventListener('click', () => {
        getAudioCtx();
        handleCorrect();
    });

    btnWrong.addEventListener('click', () => {
        getAudioCtx();
        handleWrong();
    });

    nextBtn.addEventListener('click', () => {
        getAudioCtx();
        playSfx('click');
        loadNextQuote();
    });

    sfxToggleBtn.addEventListener('click', () => {
        sfxEnabled = !sfxEnabled;
        sfxIcon.textContent = sfxEnabled ? '🔊' : '🔇';
        if (sfxEnabled) playSfx('click');
    });

    // Mobile audio unlock on first user gesture
    document.addEventListener('touchstart', function unlockAudio() {
        getAudioCtx();
        document.removeEventListener('touchstart', unlockAudio);
    }, { passive: true });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            e.preventDefault();
            playVoiceHint();
        } else if (e.code === 'Enter') {
            e.preventDefault();
            if (!isRevealed) revealAnswer();
            else loadNextQuote();
        } else if (e.key === '1') {
            if (isRevealed) handleCorrect();
        } else if (e.key === '2') {
            if (isRevealed) handleWrong();
        }
    });

    // Boot
    window.addEventListener('DOMContentLoaded', init);
})();
