from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from bson import ObjectId
import os

edit_konten_gambar = Blueprint('edit_konten_gambar', __name__)


@edit_konten_gambar.route('/edit_gambar/<_id_kelas>/<_id_menu>/<_id_konten>', methods=['POST'])
def edit_konten_gambar_(_id_kelas, _id_menu, _id_konten):
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,algorithms=['HS256'])

            konten_gambar = current_app.db.kontenmateri.find_one({'_id': ObjectId(_id_konten), '_id_menu': ObjectId(_id_menu), '_id_kelas': ObjectId(_id_kelas)})
            if konten_gambar and konten_gambar['tipe'] == 'gambar':
                nama_gambar = konten_gambar['gambar_konten']
                lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Img_konten', nama_gambar)
                if os.path.exists(lokasi_gambar):
                    os.remove(lokasi_gambar)
            
            gambar = request.files['gambar_konten']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambarkonten-{mytime}.{extension}'
            save_to = f'app/static/image/Img_konten/{gambar_name}'
            gambar.save(save_to)

            doc_konten = {
                '_id_kelas' : ObjectId(_id_kelas),
                '_id_menu' : ObjectId(_id_menu),
                'link_video': '',
                'gambar_konten' : gambar_name,
                'judul_penjelasan' : '',
                'deskripsi_penjelasan' : '',
                'tipe' : 'gambar'
            }

            current_app.db.kontenmateri.update_one({'_id' : ObjectId(_id_konten)}, {'$set' : doc_konten})
            msg = 'edit_gambar'
            return redirect(url_for('detail_materi.det_materi', msg=msg, _id_kelas = _id_kelas, _id_menu = _id_menu))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
