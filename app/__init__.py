from flask import Flask
from config import Config
from pymongo import MongoClient
import hashlib
import jwt
from datetime import datetime, timedelta

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['DBNAME']]

    from .routes.dashboard_admin import dashboard_admin
    app.register_blueprint(dashboard_admin)

    from .routes.homepage import homepage_
    app.register_blueprint(homepage_)

    from .routes.profile_admin import profile_
    app.register_blueprint(profile_)

    from .routes.semuakelas import semuakelas
    app.register_blueprint(semuakelas)

    from .routes.siswa import siswa_
    app.register_blueprint(siswa_)

    from .routes.daftar import daftar_
    app.register_blueprint(daftar_)

    from .routes.login import login_
    app.register_blueprint(login_)

    from .routes.program import program_
    app.register_blueprint(program_)

    return app
