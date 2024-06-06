from flask import Blueprint, render_template, request, current_app
import jwt
from bson import ObjectId

detailkelas_ = Blueprint('detailkelas', __name__)

@detailkelas_.route('/detailkelas/<_id>')
def detailkelas(_id):
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        status = payload.get('id')
        return render_template('template/detailkelas.html', status = status, user_info=user_info, kelas = kelas)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/detailkelas.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/detailkelas.html', msg=msg)

