from flask import Blueprint, render_template, request, current_app
import jwt

kontak_ = Blueprint('kontak', __name__)

@kontak_.route('/kontak')
def kontak():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    medsos = current_app.db.medsos.find_one({})
    msg = request.args.get('msg')
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = payload.get('id')
        return render_template('template/kontak.html', status = status, medsos = medsos, msg = msg)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/kontak.html', msg=msg,  medsos = medsos)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/kontak.html', msg=msg,  medsos = medsos)

