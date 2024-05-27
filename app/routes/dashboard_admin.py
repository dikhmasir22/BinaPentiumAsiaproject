from flask import Blueprint, render_template, request, current_app,redirect,url_for
import jwt

dashboard_admin = Blueprint('dashboard_admin', __name__)

@dashboard_admin.route('/dashboard', methods = ['GET'])
def dashboard():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        status = payload.get('id')
        return render_template('admin_panel/dashboard_admin.html', user_info=user_info, status = status)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))

