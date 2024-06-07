from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId

detail_siswa = Blueprint('detail_siswa', __name__)

@detail_siswa.route('/detail_siswa/<_id>',methods=['GET','POST'])
def det_siswa(_id):
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
        detail_Siswa = current_app.db.user.find_one({'_id' : ObjectId(_id)})
        print(detail_Siswa)
        status = payload.get('id')
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
        
        if user_admin:
            return render_template('admin_panel/detail_siswa.html', user_info=user_info, status_admin = status, detail_Siswa = detail_Siswa)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
