from flask import Flask, request, render_template, current_app, Blueprint, session, redirect, url_for, jsonify
import hashlib
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
from datetime import datetime, timedelta
import os
import pathlib

login_gugel = Blueprint('login_gugel', __name__)

GOOGLE_CLIENT_ID = '57554680057-dq9jles7nseck6k15m6ca8nra1nmgi9c.apps.googleusercontent.com'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# GOOGLE CLIENT
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=['https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email', 'openid'],
    redirect_uri='http://127.0.0.1:5000/callback'
)
# GOOGLE CLIENT


@login_gugel.route('/login/google')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


@login_gugel.route('/callback')
def callback():

    semua_kelas = list(current_app.db.semuakelas.find({}))
    medsos = current_app.db.medsos.find_one({})

    if 'error' in request.args:
      
        return redirect(url_for('homepage.homepage'))

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = google_requests.Request()
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=request_session,
        audience=GOOGLE_CLIENT_ID
    )

    email = id_info.get('email')
    user = current_app.db.user.find_one({'email': email})

    if user is None:
        
        namalengkap = id_info.get('name', '')
        namadepan = namalengkap.split(' ')[0]

        doc = {
            "email": email,
            "password": '',
            "nama_lengkap": namalengkap,
            "nama_depan": namadepan,
            "deskripsi": "",
            "no_telepon": "",
            "no_ktp": "",
            "jenis_kelamin": "",
            "tempat_tanggal_lahir": "",
            "alamat": "",
            "level": "user",
            'foto_profile': ''
        }
        current_app.db.user.insert_one(doc)

    payload = ({
        'id': email,
        "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
    })
    SECRET_KEY = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return render_template('template/homepage.html', token = token, semua_kelas = semua_kelas, medsos = medsos)
