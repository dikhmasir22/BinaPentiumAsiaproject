from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt

semuakelas = Blueprint('semuakelas', __name__)


@semuakelas.route('/semuakelas', methods=['GET', 'POST'])
def semuakelas_():
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
        Datakelas = list(current_app.db.semuakelas.find({}))   
        status = payload.get('id')
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
        
        if user_admin:
            return render_template('admin_panel/semuakelas_admin.html', user_info=user_info, status_admin = status, datakelas = Datakelas, msg = msg)
        else:
            return render_template('admin_panel/semuakelas_admin.html', user_info=user_info, status = status, datakelas = Datakelas)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
