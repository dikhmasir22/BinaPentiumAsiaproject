from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId

hapuskelas_ = Blueprint('hapuskelas', __name__)


@hapuskelas_.route('/hapus_kelas/<_id>', methods=['GET', 'POST'])
def hapuskelas(_id):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            current_app.db.semuakelas.delete_one({'_id': ObjectId(_id)})
            msg = 'hapus'
            
            return redirect(url_for('semuakelas.semuakelas_', msg = msg))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
