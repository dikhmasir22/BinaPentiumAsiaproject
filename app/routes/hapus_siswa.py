from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId
import os

hapus_siswa = Blueprint('hapus_siswa', __name__)


@hapus_siswa.route('/hapus_siswa/<_id_siswa>')
def hapus_siswa_(_id_siswa):
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive,SECRET_KEY,algorithms=['HS256'])
            siswa = current_app.db.user.find_one({'_id' : ObjectId(_id_siswa)})

            gambar_name = siswa.get('foto_profile')
            if gambar_name:  
                lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Imgprofile', gambar_name)
                if os.path.exists(lokasi_gambar):
                    os.remove(lokasi_gambar)
            
            current_app.db.user.delete_one({'_id' : ObjectId(_id_siswa)})
            current_app.db.kelassaya.delete_many({'_id_siswa' : ObjectId(_id_siswa)})
            current_app.db.menumaterisiswa.delete_many({'_id_siswa' : ObjectId(_id_siswa)})
            current_app.db.transaksi.delete_many({'$or': [{'_id_siswa': ObjectId(_id_siswa)},{'user_id': ObjectId(_id_siswa)}]})
            msg = 'hapus_siswa'
            return redirect(url_for('siswa.siswa', msg = msg))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
