from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId
import os

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

            materi_kelas = list(current_app.db.menumateri.find({'_id_kelas' : ObjectId(_id)}))
            for materi in materi_kelas:
                konten_materi = list(current_app.db.kontenmateri.find({'_id_menu' : materi['_id']}))
                for konten in konten_materi:
                    if konten['tipe'] == 'gambar':
                        gambar_name = konten['gambar_konten']
                        lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Img_konten', gambar_name)
                        if os.path.exists(lokasi_gambar):
                            os.remove(lokasi_gambar)

            kelas_sekarang = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
            nama_gambar = kelas_sekarang['gambar_kelas']
            lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Imgkelas', nama_gambar)
            if os.path.exists(lokasi_gambar):
                os.remove(lokasi_gambar)
            
            current_app.db.menumateri.delete_many({'_id_kelas' : ObjectId(_id)})
            current_app.db.kontenmateri.delete_many({'id_kelas' : ObjectId(_id)})
            current_app.db.menumaterisiswa.delete_many({'_id_kelas' : ObjectId(_id)})
            current_app.db.semuakelas.delete_one({'_id': ObjectId(_id)})
            msg = 'hapus'
            
            return redirect(url_for('semuakelas.semuakelas_', msg = msg))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
