from flask import Blueprint, render_template, request, current_app, redirect, url_for
import jwt
from datetime import datetime
import os
from bson import ObjectId

admin_place = Blueprint('adminplace', __name__)

# Carousel Image Routes
@admin_place.route('/admin')
def admin():
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
        admin = list(current_app.db.user.find({'level': 'admin'}))
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        status = payload.get('id')
        if super_admin:
            return render_template('admin_panel/admin_place.html', user_info = user_info, status_superadmin = status, msg = msg, admin = admin)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return redirect(url_for('homepage.homepage', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return redirect(url_for('homepage.homepage', msg = msg))