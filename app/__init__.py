from flask import Flask
from .config import Config
from .extensions import db
from .routes import read_bp  # Importamos el Blueprint para las rutas
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    Swagger(app, template_file="swagger_config.yaml")
    CORS(app)  # Habilitar CORS para todas las rutas

    # Registrar Blueprint de las rutas
    app.register_blueprint(read_bp)

    return app
