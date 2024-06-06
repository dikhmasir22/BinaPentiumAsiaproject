from flask import Flask
from config import Config
from pymongo import MongoClient
import hashlib
import jwt
from datetime import datetime, timedelta
from bson import ObjectId

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

    from .routes.kontak import kontak_
    app.register_blueprint(kontak_)

    from .routes.detail_siswa import detail_siswa
    app.register_blueprint(detail_siswa)

    from .routes.detailkelas import detailkelas_
    app.register_blueprint(detailkelas_)

    from .routes.materi import materi_
    app.register_blueprint(materi_)

    from .routes.kelassaya import kelassaya_
    app.register_blueprint(kelassaya_)

    return app
