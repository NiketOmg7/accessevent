with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Подключаем CSRF-защиту
if 'CSRFProtect' not in code:
    code = code.replace('from flask import Flask', 'from flask import Flask\nfrom flask_wtf.csrf import CSRFProtect')
    code = code.replace('app = create_app()', 'app = create_app()\ncsrf = CSRFProtect(app)')
    print('✅ CSRF-защита подключена')

# 2. Защита профиля: пользователь видит только свой профиль
old_profile = '''    @app.route('/profile/<int:user_id>')
    def profile_page(user_id):
        user = User.query.get_or_404(user_id)'''
new_profile = '''    @app.route('/profile/<int:user_id>')
    def profile_page(user_id):
        # Если пользователь не авторизован или пытается зайти в чужой профиль
        if 'user_id' not in session or session['user_id'] != user_id:
            return redirect(url_for('login_page'))
            
        user = User.query.get_or_404(user_id)'''
if old_profile in code:
    code = code.replace(old_profile, new_profile)
    print('✅ Профиль защищен от чужих глаз')

# 3. Защита удаления: только автор может удалить
# (это уже есть, но на всякий случай проверяем)
if 'if event.organizer_id == session[\'user_id\']:' not in code:
    print('⚠️ Проверка авторства при удалении не найдена, возможно, нужно обновить вручную')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('✅ Защита сайта настроена!')
