#!/usr/bin/env python3
import os
import json

os.chdir('/workspaces/bigbeantest2.github.io')

games_dir = 'game'
game_folders = sorted([d for d in os.listdir(games_dir) if os.path.isdir(os.path.join(games_dir, d))])

main_index = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GameHub - Play Premium Games</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            overflow-x: hidden;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }

        header {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1429 100%);
            border-bottom: 1px solid #2a2f4a;
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .auth-buttons {
            display: flex;
            gap: 15px;
        }

        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .btn-google {
            background: #ffffff;
            color: #0a0e27;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .btn-google:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
        }

        .btn-login {
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            color: #0a0e27;
        }

        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
        }

        .btn-logout {
            background: rgba(255, 59, 48, 0.1);
            color: #ff3b30;
            border: 1px solid #ff3b30;
        }

        .btn-logout:hover {
            background: rgba(255, 59, 48, 0.2);
        }

        .user-info {
            display: none;
            align-items: center;
            gap: 15px;
        }

        .user-info.active {
            display: flex;
        }

        .user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }

        .hero {
            padding: 60px 0 80px 0;
            text-align: center;
        }

        .hero h1 {
            font-size: 48px;
            margin-bottom: 20px;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: 18px;
            color: #a0a0a0;
            margin-bottom: 40px;
        }

        .search-box {
            max-width: 500px;
            margin: 0 auto 60px;
            position: relative;
        }

        .search-box input {
            width: 100%;
            padding: 15px 20px;
            border: 1px solid #2a2f4a;
            border-radius: 12px;
            background: #1a1f3a;
            color: #e0e0e0;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .search-box input:focus {
            outline: none;
            border-color: #00d4ff;
            background: #1f2540;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
        }

        .games-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 25px;
            padding: 40px 0;
        }

        .game-card {
            background: linear-gradient(135deg, #1a1f3a 0%, #15192b 100%);
            border: 1px solid #2a2f4a;
            border-radius: 12px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
        }

        .game-card:hover {
            transform: translateY(-8px);
            border-color: #00d4ff;
            box-shadow: 0 20px 40px rgba(0, 212, 255, 0.15);
        }

        .game-poster {
            width: 100%;
            height: 280px;
            background: linear-gradient(135deg, #2a2f4a 0%, #1f2540 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 48px;
            color: #2a2f4a;
        }

        .game-info {
            padding: 20px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .game-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            color: #00d4ff;
        }

        .game-description {
            font-size: 12px;
            color: #7a7a7a;
            flex-grow: 1;
            margin-bottom: 15px;
            line-height: 1.4;
        }

        .play-btn {
            width: 100%;
            padding: 10px;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            color: #0a0e27;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .play-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 20px rgba(0, 212, 255, 0.3);
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: #1a1f3a;
            border: 1px solid #2a2f4a;
            border-radius: 12px;
            padding: 40px;
            max-width: 400px;
            width: 90%;
        }

        .modal-content h2 {
            margin-bottom: 30px;
            color: #00d4ff;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-size: 14px;
            font-weight: 500;
        }

        .form-group input {
            width: 100%;
            padding: 12px;
            border: 1px solid #2a2f4a;
            border-radius: 6px;
            background: #0f1429;
            color: #e0e0e0;
            font-size: 14px;
        }

        .form-group input:focus {
            outline: none;
            border-color: #00d4ff;
            background: #141829;
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            margin-top: 30px;
        }

        .modal-buttons button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .modal-buttons .btn-cancel {
            background: #2a2f4a;
            color: #e0e0e0;
        }

        .modal-buttons .btn-confirm {
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            color: #0a0e27;
        }

        .divider {
            text-align: center;
            margin: 20px 0;
            color: #7a7a7a;
        }

        .error {
            background: rgba(255, 59, 48, 0.1);
            border: 1px solid #ff3b30;
            color: #ff6b63;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .hero h1 {
                font-size: 32px;
            }

            .games-grid {
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 15px;
            }

            .auth-buttons {
                flex-direction: column;
                gap: 10px;
            }

            .btn {
                padding: 8px 12px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">🎮 GameHub</div>
                <div class="auth-buttons">
                    <div class="user-info" id="userInfo">
                        <div class="user-avatar" id="userAvatar"></div>
                        <button class="btn btn-logout" onclick="logout()">Logout</button>
                    </div>
                    <div id="authButtons">
                        <button class="btn btn-google" onclick="loginGoogle()">🔵 Google</button>
                        <button class="btn btn-login" onclick="openLoginModal()">Login</button>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main>
        <div class="container">
            <div class="hero">
                <h1>Play Premium Games</h1>
                <p>Enjoy unlimited gaming without time limits</p>
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="Search games..." onkeyup="filterGames()">
                </div>
            </div>

            <div class="games-grid" id="gamesGrid"></div>
        </div>
    </main>

    <div class="modal" id="loginModal">
        <div class="modal-content">
            <h2>Login</h2>
            <div id="loginError"></div>
            <button class="btn btn-google" style="width: 100%; justify-content: center;" onclick="loginGoogle()">🔵 Continue with Google</button>
            <div class="divider">OR</div>
            <div class="form-group">
                <label>Email</label>
                <input type="email" id="loginEmail" placeholder="your@email.com">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" id="loginPassword" placeholder="Enter password">
            </div>
            <div class="modal-buttons">
                <button class="btn-cancel" onclick="closeLoginModal()">Cancel</button>
                <button class="btn-confirm" onclick="loginWithCredentials()">Login</button>
            </div>
        </div>
    </div>

    <script>
        const gamesData = ''' + json.dumps(game_folders) + ''';

        function initGames() {
            const gamesGrid = document.getElementById('gamesGrid');
            gamesGrid.innerHTML = gamesData.map((gameId, index) => `
                <a href="game/${gameId}/" class="game-card">
                    <div class="game-poster">🎮</div>
                    <div class="game-info">
                        <div class="game-title">${formatGameName(gameId)}</div>
                        <div class="game-description">Tap to play this amazing game</div>
                        <button class="play-btn" onclick="playGame(event, '${gameId}')">Play Now</button>
                    </div>
                </a>
            `).join('');
        }

        function formatGameName(id) {
            return id.split('.').pop().replace(/([A-Z])/g, ' $1').trim();
        }

        function filterGames() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.game-card');
            cards.forEach(card => {
                const title = card.querySelector('.game-title').textContent.toLowerCase();
                card.style.display = title.includes(searchTerm) ? '' : 'none';
            });
        }

        function playGame(e, gameId) {
            if (!isLoggedIn()) {
                e.preventDefault();
                openLoginModal();
            }
        }

        function openLoginModal() {
            document.getElementById('loginModal').classList.add('active');
        }

        function closeLoginModal() {
            document.getElementById('loginModal').classList.remove('active');
            document.getElementById('loginError').innerHTML = '';
        }

        function loginGoogle() {
            const user = { name: 'Google User', email: 'user@google.com', avatar: 'G' };
            setCurrentUser(user);
            closeLoginModal();
        }

        function loginWithCredentials() {
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            if (!email || !password) {
                document.getElementById('loginError').innerHTML = '<div class="error">Please enter email and password</div>';
                return;
            }

            const user = { name: email.split('@')[0], email, avatar: email[0].toUpperCase() };
            setCurrentUser(user);
            closeLoginModal();
        }

        function setCurrentUser(user) {
            localStorage.setItem('currentUser', JSON.stringify(user));
            updateUI();
        }

        function isLoggedIn() {
            return localStorage.getItem('currentUser') !== null;
        }

        function getCurrentUser() {
            return JSON.parse(localStorage.getItem('currentUser'));
        }

        function updateUI() {
            const userInfo = document.getElementById('userInfo');
            const authButtons = document.getElementById('authButtons');

            if (isLoggedIn()) {
                const user = getCurrentUser();
                userInfo.classList.add('active');
                authButtons.style.display = 'none';
                document.getElementById('userAvatar').textContent = user.avatar;
            } else {
                userInfo.classList.remove('active');
                authButtons.style.display = 'flex';
            }
        }

        function logout() {
            localStorage.removeItem('currentUser');
            updateUI();
        }

        window.addEventListener('click', (e) => {
            const modal = document.getElementById('loginModal');
            if (e.target === modal) closeLoginModal();
        });

        initGames();
        updateUI();
    </script>
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(main_index)

game_page = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game - GameHub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0a0e27;
            color: #e0e0e0;
            overflow: hidden;
        }

        header {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1429 100%);
            border-bottom: 1px solid #2a2f4a;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
        }

        .back-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 212, 255, 0.1);
            border: 1px solid #00d4ff;
            color: #00d4ff;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
        }

        .back-btn:hover {
            background: rgba(0, 212, 255, 0.2);
            transform: translateX(-4px);
        }

        .game-title {
            font-size: 20px;
            font-weight: 700;
            color: #00d4ff;
        }

        .user-section {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #00d4ff, #0099ff);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }

        .logout-btn {
            background: rgba(255, 59, 48, 0.1);
            border: 1px solid #ff3b30;
            color: #ff3b30;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .logout-btn:hover {
            background: rgba(255, 59, 48, 0.2);
        }

        .game-container {
            width: 100%;
            height: 100vh;
            margin-top: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .game-frame {
            width: 100%;
            height: 100%;
            border: none;
            background: #0a0e27;
        }

        .loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 20px;
            color: #7a7a7a;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #2a2f4a;
            border-top-color: #00d4ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <header>
        <a href="/" class="back-btn">← Back</a>
        <div class="game-title">Game</div>
        <div class="user-section">
            <div class="user-avatar" id="userAvatar"></div>
            <button class="logout-btn" onclick="logout()">Logout</button>
        </div>
    </header>

    <div class="game-container">
        <div class="loading">
            <div class="spinner"></div>
            <p>Loading game...</p>
        </div>
    </div>

    <script>
        function loadGame() {
            const gameId = window.location.pathname.split('/').filter(Boolean)[1];
            const user = JSON.parse(localStorage.getItem('currentUser'));

            if (!user) {
                window.location.href = '/';
                return;
            }

            document.getElementById('userAvatar').textContent = user.avatar;

            const container = document.querySelector('.game-container');
            const gameUrl = 'https://example.com/games/' + gameId;

            container.innerHTML = `<iframe src="${gameUrl}" class="game-frame"></iframe>`;
        }

        function logout() {
            localStorage.removeItem('currentUser');
            window.location.href = '/';
        }

        window.addEventListener('load', loadGame);
    </script>
</body>
</html>
'''

for game in game_folders:
    game_index = os.path.join(games_dir, game, 'index.html')
    os.makedirs(os.path.dirname(game_index), exist_ok=True)
    with open(game_index, 'w') as f:
        f.write(game_page)

print(f"✅ Frontend generated successfully!")
print(f"✅ Main index.html created")
print(f"✅ {len(game_folders)} game pages created")
