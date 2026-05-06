from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    print('\n🐾 Сервер "Лапки Добра" запущен!')
    print('🐾 Откройте в браузере: http://localhost:5000\n')
    print(f'📁 Файлы ищутся в: {os.getcwd()}')
    print(f'📄 index.html существует: {os.path.exists("index.html")}\n')
    app.run(debug=True, port=5000)