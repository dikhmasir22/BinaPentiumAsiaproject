from flask import Blueprint, render_template, current_app, redirect, url_for, request
import jwt

profile_ = Blueprint('profile', __name__)

@profile_.route('/profile')
def profile():
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
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        
        if user_admin:
            return render_template('admin_panel/profile.html', user_info=user_info, status_admin = status)
        elif super_admin:
            return render_template('admin_panel/profile.html', user_info = user_info, status_superadmin = status)
        else:
            return render_template('admin_panel/profile.html', user_info=user_info, status = status)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))

