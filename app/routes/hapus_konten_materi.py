from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
import os
from bson import ObjectId

hapus_konten_materi = Blueprint('hapuskontenmateri', __name__)


@hapus_konten_materi.route('/hapus_konten_materi/<_id_kelas>/<_id_menu>/<_id_konten>', methods=['GET', 'POST'])
def hapus_konten_materi_(_id_kelas, _id_menu, _id_konten):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )

            konten = current_app.db.kontenmateri.find_one({'_id': ObjectId(_id_konten), '_id_menu': ObjectId(_id_menu), '_id_kelas': ObjectId(_id_kelas)})
            if konten and konten['tipe'] == 'gambar':
                nama_gambar = konten['gambar_konten']
                lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Img_konten', nama_gambar)
                if os.path.exists(lokasi_gambar):
                    os.remove(lokasi_gambar)


            current_app.db.kontenmateri.delete_one({'_id' : ObjectId(_id_konten), '_id_menu' : ObjectId(_id_menu), '_id_kelas' : ObjectId(_id_kelas)})
            msg = 'hapus'
            return redirect(url_for('detail_materi.det_materi', msg = msg, _id_kelas = _id_kelas, _id_menu = _id_menu))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
