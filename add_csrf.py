import os

# Список файлов, где есть формы
files = ['templates/login.html', 'templates/register.html', 'templates/create_event.html', 'templates/events.html', 'templates/profile.html']

for file in files:
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Если токена нет — добавляем его во все формы
        if 'csrf_token()' not in html:
            # Находим все формы и вставляем токен сразу после открывающего тега <form ...>
            import re
            # Ищем <form ...> и добавляем токен после первого >
            html = re.sub(r'(<form[^>]*>)', r'\1\n        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">', html)
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'✅ CSRF-токен добавлен в {file}')
        else:
            print(f'ℹ️ Токен уже есть в {file}')
    else:
        print(f'⚠️ Файл {file} не найден')
