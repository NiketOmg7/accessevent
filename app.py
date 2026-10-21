from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO, emit
from config import Config
from models import db, User, Event, Registration
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from datetime import timedelta
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    app.config['WTF_CSRF_ENABLED'] = False
    app.secret_key = 'super_secret_key_2025'
    db.init_app(app)

    # --- Главная ---
    @app.route('/')
    def index_page():
        return render_template('index.html')

    # --- Список мероприятий (поиск + фильтры) ---
    @app.route('/events')
    def events_page():
        inclusive_only = request.args.get('inclusive') in ('1', 'true')
        wheelchair_only = request.args.get('wheelchair') == '1'
        search_query = request.args.get('q', '').strip()
        
        query = Event.query.order_by(Event.event_date)
        if inclusive_only:
            query = query.filter_by(is_inclusive=True)
        if wheelchair_only:
            query = query.filter_by(wheelchair_accessible=True)
        if search_query:
            query = query.filter(
                db.or_(
                    Event.title.ilike(f'%{search_query}%'),
                    Event.location.ilike(f'%{search_query}%')
                )
            )
        events = query.all()
        return render_template('events.html', events=events)

    # --- Создание мероприятия ---

    @app.route('/profile/<int:user_id>/avatar', methods=['POST'])
    def update_avatar(user_id):
        if 'user_id' not in session or session['user_id'] != user_id:
            return redirect(url_for('login_page'))
        
        user = User.query.get_or_404(user_id)
        
        # Если выбрали эмодзи
        emoji = request.form.get('avatar_emoji')
        if emoji:
            user.avatar = emoji
            db.session.commit()
            return redirect(url_for('profile_page', user_id=user.id))
            
        # Если загрузили файл
        file = request.files.get('avatar_file')
        if file and file.filename:
            import os
            from werkzeug.utils import secure_filename
            
            # Сохраняем в папку static/uploads
            upload_folder = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            filename = secure_filename(file.filename)
            # Добавляем ID пользователя к имени, чтобы не было конфликтов
            filename = f"user_{user.id}_{filename}"
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            user.avatar = '/static/uploads/' + filename
            db.session.commit()
            
        return redirect(url_for('profile_page', user_id=user.id))
    


    @app.route('/api/chat', methods=['POST'])
    def chat_api():
        data = request.get_json()
        msg = (data.get('message') or '').lower().strip()
        
        # Умные ответы
        if any(word in msg for word in ['привет', 'здравствуй', 'hello', 'хай']):
            reply = 'Привет! Рад тебя видеть. Я могу помочь тебе создать мероприятие, записаться на него или просто рассказать, как тут все устроено. Что тебя интересует?'
        elif 'создать' in msg or ('мероприятие' in msg and 'как' in msg):
            reply = 'Создать мероприятие очень просто! Нажми на кнопку «+ Создать мероприятие» на странице «Мероприятия». Заполни название, дату и отметь галочками доступные функции (сурдоперевод, пандусы и т.д.).'
        elif 'записаться' in msg or 'регистрация' in msg:
            reply = 'Чтобы записаться, найди интересующее событие на главной странице и нажми зеленую кнопку «Записаться». Оно сразу появится в твоем профиле в разделе «Мои регистрации».'
        elif 'удалить' in msg:
            reply = 'Удалить мероприятие может только его создатель. Если ты создал событие, зайди в свой профиль и в разделе «Мои созданные мероприятия» нажми красную кнопку «Удалить».'
        elif 'аватар' in msg or 'фото' in msg or 'картинка' in msg:
            reply = 'Сменить аватарку можно в профиле. Там есть форма: можно загрузить свою картинку или выбрать готовую эмоцию (например, 😎 или 🤟).'
        elif 'доступ' in msg or 'инвалид' in msg or 'коляск' in msg:
            reply = 'У нас есть фильтр «Для колясочников», который показывает мероприятия с пандусами. А бейджи «Сурдоперевод» и «Визуальные оповещения» помогают найти события для слабослышащих.'
        elif 'помощь' in msg or 'помоги' in msg or 'что ты умеешь' in msg:
            reply = 'Я умею: рассказывать, как создать мероприятие, как записаться на него, как сменить аватарку и как искать инклюзивные события. Просто спроси меня!'
        elif 'спасибо' in msg or 'благодар' in msg:
            reply = 'Всегда пожалуйста! Если что-то еще понадобится — я здесь.'
        elif 'как дела' in msg or 'как ты' in msg:
            reply = 'У меня все отлично! Работаю на благо инклюзивных мероприятий. А у тебя как дела?'
        else:
            reply = 'Хм, я не совсем понял вопрос. Попробуй спросить: «как создать мероприятие», «как записаться» или «как сменить аватарку».'
            
        return {'reply': reply}


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
    
    @app.route('/events/create', methods=['GET', 'POST'])
    def create_event():
        if 'user_id' not in session:
            return redirect(url_for('login_page'))

        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            event_date_str = request.form.get('event_date')
            location = request.form.get('location')

            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')
            except:
                event_date = datetime.utcnow()

            new_event = Event(
                title=title,
                description=description,
                event_date=event_date,
                location=location,
                is_inclusive=request.form.get('is_inclusive') == 'on',
                sign_language=request.form.get('sign_language') == 'on',
                visual_alerts=request.form.get('visual_alerts') == 'on',
                wheelchair_accessible=request.form.get('wheelchair_accessible') == 'on',
                organizer_id=session['user_id']
            )
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('events_page'))

        return render_template('create_event.html')

    # --- Удаление мероприятия (только для автора) ---
    @app.route('/events/<int:event_id>/delete', methods=['POST'])
    def delete_event(event_id):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        event = Event.query.get_or_404(event_id)
        # Удалять может только создатель
        if event.organizer_id == session['user_id']:
            # Сначала удаляем все записи на это мероприятие, чтобы не было ошибки базы
            Registration.query.filter_by(event_id=event_id).delete()
            db.session.delete(event)
            db.session.commit()
        return redirect(url_for('events_page'))

    # --- Запись ---
    @app.route('/events/<int:event_id>/register', methods=['POST'])
    def register_for_event(event_id):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        
        existing = Registration.query.filter_by(user_id=session['user_id'], event_id=event_id).first()
        if not existing:
            new_reg = Registration(
                user_id=session['user_id'],
                event_id=event_id,
                accessibility_request=''
            )
            db.session.add(new_reg)
            db.session.commit()
        
        return redirect(url_for('profile_page', user_id=session['user_id']))

    # --- Вход ---

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index_page'))
    
    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        if request.method == 'POST':
            email = (request.form.get('email') or '').strip().lower()
            password = request.form.get('password') or ''
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('profile_page', user_id=user.id))
                
            return render_template('login.html', error='Неверный email или пароль'), 401
        return render_template('login.html')

    # --- Регистрация ---
    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        if request.method == 'POST':
            username = (request.form.get('username') or '').strip()
            email = (request.form.get('email') or '').strip().lower()
            password = request.form.get('password') or ''
            role = request.form.get('role', 'participant')

            if User.query.filter_by(email=email).first():
                return render_template('register.html', error='Этот email уже зарегистрирован'), 400

            new_user = User(username=username, email=email, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login_page'))
        return render_template('register.html')

    # --- Профиль ---
    @app.route('/profile/<int:user_id>')
    def profile_page(user_id):
        # Если пользователь не авторизован или пытается зайти в чужой профиль
        if 'user_id' not in session or session['user_id'] != user_id:
            return redirect(url_for('login_page'))
            
        user = User.query.get_or_404(user_id)
        registrations = Registration.query.filter_by(user_id=user.id).all()
        return render_template('profile.html', user=user, registrations=registrations)

    with app.app_context():
        db.create_all()

    return app

app = create_app()
csrf = CSRFProtect(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('send_message')
def handle_message(data):
    emit('receive_message', {
        'username': data.get('username', 'Аноним'),
        'message': data.get('message', '')
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)
