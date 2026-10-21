with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'global-chat-widget' not in html:
    chat_html = '''
    <!-- Глобальный чат -->
    <div id="global-chat-widget" style="position: fixed; bottom: 90px; right: 20px; z-index: 9998; font-family: Inter, sans-serif;">
        <div id="global-chat-window" style="display: none; width: 340px; height: 480px; background: var(--card-bg); border: 1px solid var(--nav-border); border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); flex-direction: column; margin-bottom: 15px; overflow: hidden;">
            <div style="background: #8b5cf6; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 600;">🌍 Общий чат</div>
                <button id="close-global-chat" style="background: none; border: none; color: white; font-size: 1.2rem; cursor: pointer;">✖</button>
            </div>
            <div id="global-chat-messages" style="flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; background: var(--bg-color);">
                <div style="text-align: center; color: var(--text-muted); font-size: 0.8rem;">Добро пожаловать в общий чат!</div>
            </div>
            <form id="global-chat-form" style="display: flex; border-top: 1px solid var(--nav-border); background: var(--card-bg);">
                <input type="text" id="global-chat-input" placeholder="Написать сообщение..." style="flex: 1; border: none; padding: 12px; outline: none; background: transparent; color: var(--text-main);" autocomplete="off">
                <button type="submit" style="background: #8b5cf6; color: white; border: none; padding: 0 20px; cursor: pointer;">➤</button>
            </form>
        </div>
        <button id="global-chat-toggle" style="background: #8b5cf6; color: white; border: none; width: 60px; height: 60px; border-radius: 50%; font-size: 1.5rem; cursor: pointer; box-shadow: 0 4px 12px rgba(139,92,246,0.4); display: flex; align-items: center; justify-content: center;">🌍</button>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const socket = io();
            const chatToggle = document.getElementById('global-chat-toggle');
            const chatWindow = document.getElementById('global-chat-window');
            const closeChat = document.getElementById('close-global-chat');
            const chatForm = document.getElementById('global-chat-form');
            const chatInput = document.getElementById('global-chat-input');
            const chatMessages = document.getElementById('global-chat-messages');
            const username = "{{ session.get('username', 'Гость') }}";

            chatToggle.addEventListener('click', () => {
                if (chatWindow.style.display === 'none' || chatWindow.style.display === '') {
                    chatWindow.style.display = 'flex';
                    chatToggle.style.display = 'none';
                }
            });

            closeChat.addEventListener('click', () => {
                chatWindow.style.display = 'none';
                chatToggle.style.display = 'flex';
            });

            chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const message = chatInput.value.trim();
                if (!message) return;
                socket.emit('send_message', { username: username, message: message });
                chatInput.value = '';
            });

            socket.on('receive_message', (data) => {
                const msgDiv = document.createElement('div');
                msgDiv.style.cssText = 'background: var(--card-bg); padding: 10px; border-radius: 10px; border: 1px solid var(--nav-border); align-self: flex-start; max-width: 80%;';
                msgDiv.innerHTML = '<strong style="color: #8b5cf6; font-size: 0.85rem;">' + data.username + '</strong><br>' + data.message;
                chatMessages.appendChild(msgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
        });
    </script>
    '''
    html = html.replace('</body>', chat_html + '\n</body>')
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ Кнопка чата добавлена в base.html!')
else:
    print('ℹ️ Кнопка чата уже есть.')
