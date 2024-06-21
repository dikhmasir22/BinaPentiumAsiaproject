from flask import Flask, current_app
from config import Config
from pymongo import MongoClient
import hashlib
import jwt
from datetime import datetime, timedelta
from bson import ObjectId
from google_auth_oauthlib.flow import Flow
from authlib.integrations.flask_client import OAuth
import os
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import pathlib

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # MONGODB
    client = MongoClient(app.config['MONGODB_URI'])
    app.db = client[app.config['DBNAME']]
    # DATABASE

    GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']

    from .routes.dashboard_admin import dashboard_admin
    app.register_blueprint(dashboard_admin)

    from .routes.homepage import homepage_
    app.register_blueprint(homepage_)

    from .routes.profile import profile_
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

    from .routes.konten_homepage_route import konten_homepage
    app.register_blueprint(konten_homepage)
    
    from .routes.kelassaya import kelassaya_
    app.register_blueprint(kelassaya_)

    from .routes.tambah_kelas import tambah_kelas_
    app.register_blueprint(tambah_kelas_)

    from .routes.hapus_kelas import hapuskelas_
    app.register_blueprint(hapuskelas_)

    from .routes.edit_kelas import edit_kelas_
    app.register_blueprint(edit_kelas_)

    from .routes.update_profile import update_profile_
    app.register_blueprint(update_profile_)

    from .routes.ikuti_kelas import ikuti_kelas_
    app.register_blueprint(ikuti_kelas_)

    from .routes.detail_materi import detail_materi
    app.register_blueprint(detail_materi)

    from .routes.tambah_materi_baru import tambah_materi_baru
    app.register_blueprint(tambah_materi_baru)

    from .routes.tambah_konten_yutub import tambah_konten_yutub
    app.register_blueprint(tambah_konten_yutub)

    from .routes.tambah_konten_gambar import tambah_konten_gambar
    app.register_blueprint(tambah_konten_gambar)

    from .routes.tambah_konten_penjelasan import tambah_konten_penjelasan
    app.register_blueprint(tambah_konten_penjelasan)

    from .routes.update_materi_selesai import update_status_materi
    app.register_blueprint(update_status_materi)

    from .routes.hapus_konten_materi import hapus_konten_materi
    app.register_blueprint(hapus_konten_materi)

    from .routes.hapus_materi import hapus_materi
    app.register_blueprint(hapus_materi)

    from .routes.edit_konten_yutub import edit_konten_yutub
    app.register_blueprint(edit_konten_yutub)

    from .routes.edit_konten_gambar import edit_konten_gambar
    app.register_blueprint(edit_konten_gambar)

    from .routes.edit_konten_penjelasan import edit_konten_penjelasan
    app.register_blueprint(edit_konten_penjelasan)

    from .routes.login_gugel import login_gugel
    app.register_blueprint(login_gugel)

    from .routes.edit_materi import edit_materi
    app.register_blueprint(edit_materi)

    from .routes.transaksi import transaksi_
    app.register_blueprint(transaksi_)

    from .routes.hapus_siswa import hapus_siswa
    app.register_blueprint(hapus_siswa)


    return app
