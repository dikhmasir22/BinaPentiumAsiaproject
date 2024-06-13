from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId
import os

hapus_materi = Blueprint('hapusmateri', __name__)


@hapus_materi.route('/hapus_materi/<_id_kelas>/<_id_menu>', methods=['GET', 'POST'])
def hapus_materi_(_id_kelas, _id_menu):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            konten_materi = list(current_app.db.kontenmateri.find({'_id_menu': ObjectId(_id_menu)}))

            for konten in konten_materi:
                if konten['tipe'] == 'gambar':
                    gambar_name = konten['gambar_konten']
                    lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Img_konten', gambar_name)
                    if os.path.exists(lokasi_gambar):
                        os.remove(lokasi_gambar)

            current_app.db.menumateri.delete_one({'_id' : ObjectId(_id_menu), '_id_kelas' : ObjectId(_id_kelas)})
            current_app.db.kontenmateri.delete_many({'_id_menu' : ObjectId(_id_menu)})
            msg = 'hapus'
            return redirect(url_for('detail_materi.det_materi', msg = msg, _id_kelas = _id_kelas, _id_menu = 'none'))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
