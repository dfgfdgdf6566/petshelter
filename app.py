from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DATA_FILE = 'data.json'

# ==================== ЗАГРУЗКА И СОХРАНЕНИЕ ДАННЫХ ====================

def load_data():
    """Загружает данные из файла data.json"""
    if not os.path.exists(DATA_FILE):
        # Создаём файл с начальными данными, если его нет
        initial_data = {
            'users': [],
            'donations': [],
            'carts': {}
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        return initial_data
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    """Сохраняет данные в файл data.json"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== СТРАНИЦЫ ====================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# ==================== API ДЛЯ ПОЛЬЗОВАТЕЛЕЙ ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.json
    app_data = load_data()
    
    # Проверяем, не занят ли логин
    if any(u['username'] == data.get('username') for u in app_data['users']):
        return jsonify({'error': 'Такой логин уже существует'}), 400
    
    # Добавляем нового пользователя
    app_data['users'].append({
        'username': data.get('username'),
        'password': data.get('password'),
        'fullname': data.get('fullname')
    })
    
    save_data(app_data)
    return jsonify({'message': 'Регистрация успешна! Теперь войдите в аккаунт.'})

@app.route('/api/login', methods=['POST'])
def login():
    """Вход пользователя"""
    data = request.json
    app_data = load_data()
    
    # Ищем пользователя с таким логином и паролем
    user = next((u for u in app_data['users'] 
                 if u['username'] == data.get('username') 
                 and u['password'] == data.get('password')), None)
    
    if user:
        return jsonify({
            'success': True,
            'user': {
                'username': user['username'],
                'fullname': user['fullname']
            }
        })
    return jsonify({'success': False, 'error': 'Неверный логин или пароль'}), 401

# ==================== ЗАПУСК СЕРВЕРА ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'🐾 Сервер "Лапки Добра" запущен на порту {port}!')
    print(f'📱 Откройте в браузере: http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=False)