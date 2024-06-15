from flask import Blueprint, render_template, request, current_app
import jwt

homepage_ = Blueprint('homepage', __name__)

@homepage_.route('/')
def homepage():
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
        status = payload.get('id')
        return render_template('template/homepage.html', status = status, msg = msg)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/homepage.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/homepage.html', msg=msg)

