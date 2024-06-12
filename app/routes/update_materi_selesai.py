from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from bson import ObjectId

update_status_materi = Blueprint('update_status_materi', __name__)


@update_status_materi.route('/update_status_materi/<_id_menu>/<_id_siswa>', methods=['POST'])
def updatestatusmateri_(_id_menu, _id_siswa):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,algorithms=['HS256'])

            doc_materi = {
                '_id_kelas' : ObjectId(_id_kelas),
                '_id_menu' : ObjectId(_id_menu),
                'link_video': link_video,
                'gambar_konten' : '',
                'judul_penjelasan' : '',
                'deskripsi_penjelasan' : '',
                'tipe' : 'video'
            }

            current_app.db.kontenmateri.insert_one(doc_konten)
            msg = 'tambah_yutub'
            return redirect(url_for('detail_materi.det_materi', msg=msg, _id_kelas = _id_kelas, _id_menu = _id_menu))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
