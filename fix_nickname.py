import os

# 1. Обновляем app.py (добавляем маршрут для смены ника)
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'def update_username' not in code:
    func = '''
    @app.route('/profile/<int:user_id>/update_username', methods=['POST'])
    def update_username(user_id):
        if 'user_id' not in session or session['user_id'] != user_id:
            return redirect(url_for('login_page'))
        
        user = User.query.get_or_404(user_id)
        new_username = request.form.get('username', '').strip()
        
        if new_username and len(new_username) >= 2:
            user.username = new_username
            db.session.commit()
            session['username'] = new_username
            
        return redirect(url_for('profile_page', user_id=user.id))
    '''
    code = code.replace('    @app.route(\'/events/create\'', func + '\n    @app.route(\'/events/create\'')
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('✅ Маршрут для смены ника добавлен в app.py')
else:
    print('ℹ️ Маршрут уже есть')

# 2. Обновляем шаблон профиля
with open('templates/profile.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Добавляем форму смены ника, если её нет
if 'update_username' not in html:
    form = '''
        <!-- Форма смены никнейма -->
        <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid var(--nav-border);">
            <h4 style="margin-top: 0; margin-bottom: 10px;">Сменить никнейм</h4>
            <form action="/profile/{{ user.id }}/update_username" method="POST" style="display: flex; gap: 10px; align-items: center;">
                <input type="text" name="username" value="{{ user.username }}" placeholder="Новый никнейм" style="flex: 1; padding: 10px; border-radius: 8px; border: 1px solid var(--nav-border); background: var(--bg-color); color: var(--text-main);">
                <button type="submit" class="btn btn-primary" style="padding: 10px 20px; border-radius: 8px; font-weight: 500;">Сохранить</button>
            </form>
        </div>
    '''
    # Вставляем перед формой смены аватарки
    html = html.replace('<h4 style="margin-top: 0; margin-bottom: 15px;">Сменить аватарку</h4>', form + '\n        <h4 style="margin-top: 0; margin-bottom: 15px;">Сменить аватарку</h4>')
    with open('templates/profile.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('✅ Форма смены ника добавлена в profile.html')
else:
    print('ℹ️ Форма смены ника уже есть')

# 3. Обновляем сессию при входе, чтобы ник отображался в чате
with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'session[\'username\'] = user.username' not in code:
    # Добавляем сохранение имени в сессию при логине
    code = code.replace('session[\'user_id\'] = user.id', 'session[\'user_id\'] = user.id\n                session[\'username\'] = user.username')
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('✅ Никнейм сохраняется в сессию при входе')
else:
    print('ℹ️ Никнейм уже сохраняется в сессию')
