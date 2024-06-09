from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt

ikuti_kelas_ = Blueprint('ikuti_kelas', __name__)

@ikuti_kelas_.route('/ikuti_kelas/<_id>/<_idsiswa>',methods=['POST'])
def siswa(_id,_idsiswa):
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        kelas = current_app.db.semuakelas.find_one
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
