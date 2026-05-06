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
    import os
    port = int(os.environ.get('PORT', 5000))  # Берём порт Render или 5000 для локального запуска
    print(f'Сервер "Лапки Добра" запущен на порту {port}!')
    app.run(debug=False, host='0.0.0.0', port=port)  # Слушаем всё и используем правильный порт