import os
from dotenv import load_dotenv
from flask import Flask, render_template
from .database.db import init_db

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 't')
    app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
    app.config['FLASK_DEBUG'] = os.environ.get('FLASK_DEBUG', '1')

    init_db(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

def main():
    app = create_app()
    debug_mode = os.environ.get('FLASK_DEBUG', '1') in ('true', '1', 't', 'True')
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(debug=debug_mode, host=host, port=port)

if __name__ == '__main__':
    main()
