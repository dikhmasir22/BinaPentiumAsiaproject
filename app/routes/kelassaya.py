from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt

kelassaya_ = Blueprint('kelassaya', __name__)


@kelassaya_.route('/kelassaya', methods=['GET', 'POST'])
def kelassaya():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        msg = request.args.get('msg')
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        Datakelas = list(current_app.db.kelassaya.find({'_id_siswa' : user_info['_id']}))
        status = payload.get('id')
        return render_template('admin_panel/kelassaya.html', user_info=user_info, status = status, datakelas = Datakelas, msg = msg)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
