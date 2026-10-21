with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Добавляем импорты
if 'from flask_socketio import SocketIO, emit' not in code:
    code = code.replace('from flask import Flask', 'from flask import Flask\nfrom flask_socketio import SocketIO, emit')

# 2. Добавляем инициализацию SocketIO
if 'socketio = SocketIO' not in code:
    code = code.replace('app = create_app()', 'app = create_app()\nsocketio = SocketIO(app, cors_allowed_origins="*")')

# 3. Добавляем обработчик сообщений
if "def handle_message(data):" not in code:
    socket_code = '''
@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', {
        'username': data.get('username', 'Аноним'),
        'message': data.get('message', '')
    }, broadcast=True)
'''
    code = code.replace("if __name__ == '__main__':", socket_code + "\nif __name__ == '__main__':")
    
    # 4. Меняем запуск на socketio.run
    code = code.replace("app.run(host='0.0.0.0', port=5001, debug=True)", "socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('✅ app.py настроен для работы с чатом!')
