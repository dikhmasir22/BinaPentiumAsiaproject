from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from bson import ObjectId

edit_materi = Blueprint('edit_materi', __name__)


@edit_materi.route('/edit_materi/<_id_kelas>/<_id_menu>', methods=['POST'])
def edit_materi_(_id_kelas, _id_menu):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,algorithms=['HS256'])
            judul_materi = request.form['judul_materi']

            doc_materi = {
                '_id_kelas' : ObjectId(_id_kelas),
                'judul_materi': judul_materi,
            }

            current_app.db.menumateri.update_one({'_id' : ObjectId(_id_menu), '_id_kelas' : ObjectId(_id_kelas)}, {'$set' : doc_materi})
            msg = 'edit_materi'
            return redirect(url_for('detail_materi.det_materi', msg=msg, _id_kelas = _id_kelas, _id_menu = _id_menu))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
