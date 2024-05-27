from flask import Blueprint, render_template, request, current_app
import jwt

program_ = Blueprint('program', __name__)

@program_.route('/program')
def program():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = payload.get('id')
        return render_template('template/program.html', status = status)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/program.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/program.html', msg=msg)

