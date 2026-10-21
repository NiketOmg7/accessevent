import os

with open('templates/base.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'chat-widget' not in html:
    chat_html = '''
    <!-- Чат-виджет -->
    <div id="chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; font-family: Inter, sans-serif;">
        <div id="chat-window" style="display: none; width: 320px; height: 450px; background: var(--card-bg); border: 1px solid var(--nav-border); border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); flex-direction: column; margin-bottom: 15px; overflow: hidden;">
            <div style="background: var(--primary); color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center;">
                <div style="font-weight: 600;">🤖 ИИ-Помощник</div>
                <button id="close-chat" style="background: none; border: none; color: white; font-size: 1.2rem; cursor: pointer;">✖</button>
            </div>
            <div id="chat-messages" style="flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px;">
                <div style="background: var(--bg-color); padding: 10px; border-radius: 10px; align-self: flex-start; max-width: 80%;">
                    Привет! Я ИИ-помощник AccessEvent. Спросите меня, как создать мероприятие или записаться на него.
                </div>
            </div>
            <form id="chat-form" style="display: flex; border-top: 1px solid var(--nav-border);">
                <input type="text" id="chat-input" placeholder="Ваш вопрос..." style="flex: 1; border: none; padding: 12px; outline: none; background: transparent; color: var(--text-main);" autocomplete="off">
                <button type="submit" style="background: var(--primary); color: white; border: none; padding: 0 20px; cursor: pointer;">➤</button>
            </form>
        </div>
        <button id="chat-toggle" style="background: var(--primary); color: white; border: none; width: 60px; height: 60px; border-radius: 50%; font-size: 1.5rem; cursor: pointer; box-shadow: 0 4px 12px rgba(59,130,246,0.4); display: flex; align-items: center; justify-content: center; transition: transform 0.2s;">💬</button>
    </div>

    <script>
        const chatToggle = document.getElementById('chat-toggle');
        const chatWindow = document.getElementById('chat-window');
        const closeChat = document.getElementById('close-chat');
        const chatForm = document.getElementById('chat-form');
        const chatInput = document.getElementById('chat-input');
        const chatMessages = document.getElementById('chat-messages');

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

        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            const userMsgDiv = document.createElement('div');
            userMsgDiv.style.cssText = 'background: var(--primary); color: white; padding: 10px; border-radius: 10px; align-self: flex-end; max-width: 80%;';
            userMsgDiv.textContent = message;
            chatMessages.appendChild(userMsgDiv);
            chatInput.value = '';
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                const data = await response.json();
                
                const botMsgDiv = document.createElement('div');
                botMsgDiv.style.cssText = 'background: var(--bg-color); padding: 10px; border-radius: 10px; align-self: flex-start; max-width: 80%;';
                botMsgDiv.textContent = data.reply;
                chatMessages.appendChild(botMsgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (err) {
                console.error(err);
            }
        });
    </script>
    '''
    html = html.replace('</body>', chat_html + '\n</body>')
    with open('templates/base.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ Чат-виджет успешно возвращен!')
else:
    print('ℹ️ Чат уже есть в коде.')
