from flask import Flask, request, render_template, current_app, Blueprint, jsonify
import hashlib
import jwt
from datetime import datetime, timedelta
from app import Config

login_ = Blueprint('login', __name__)
@login_.route("/login", methods=["POST"])
def sign_in():
    email = request.form['email']
    email = email.lower()
    email = email.split('@')[0]
    user_sudah_login = current_app.db.user.find_one({'email' : email})
    if user_sudah_login :
        password_receive = request.form['password']
        pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

        hasil = current_app.db.user.find_one({
            'email' : email,
            'password' : pw_hash
        })

        if hasil :
            payload = ({
                'id' : email,
                "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
            })
            SECRET_KEY = current_app.config['SECRET_KEY']
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
   