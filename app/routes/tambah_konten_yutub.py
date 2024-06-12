from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from bson import ObjectId

tambah_konten_yutub = Blueprint('tambah_konten_yutub', __name__)


@tambah_konten_yutub.route('/save_video/<_id_kelas>/<_id_menu>', methods=['POST'])
def tambah_konten_yutub_(_id_kelas, _id_menu):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,algorithms=['HS256'])
            link_video = request.form['link_video']
            link_video = link_video.split('=')[-1]

            doc_konten = {
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
