from flask import Flask, request, render_template, current_app, Blueprint, jsonify
import hashlib

daftar_ = Blueprint('daftar', __name__)
@daftar_.route("/daftar", methods=["POST"])
def sign_up():
    namalengkap = request.form['nama']
    namadepan = namalengkap.split(' ')[0]
    email = request.form['email']
    email = email.lower()
    email = email.split('@')[0]
    password_receive = request.form['password']
    password2 = request.form['password2']
    user_sudah_login = current_app.db.user.find_one({'email' : email})

    if user_sudah_login is None:
        if password_receive == password2:
            password_hash = hashlib.sha256(
                password_receive.encode('utf-8')).hexdigest()
            doc = {
                "email": email,                             
                "password": password_hash,                          
                "nama_lengkap": namalengkap,
                "nama_depan": namadepan,
                "deskripsi" : "",
                "no_telepon": "",
                "no_ktp": "",
                "jenis_kelamin": "",
                "tempat_tanggal_lahir": "",
                "alamat": ""
            }
            current_app.db.user.insert_one(doc)
            return jsonify({'result': 'success'})
        return 'password tidak sama'
    return 'user sudah ada'