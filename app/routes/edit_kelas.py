from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta
from bson import ObjectId
import os

edit_kelas_ = Blueprint('edit_kelas', __name__)


@edit_kelas_.route('/editkelas/<_id>', methods=['GET', 'POST'])
def editkelas(_id):
    if request.method == 'POST':
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,
                                 algorithms=['HS256'])
            Nama_kelas = request.form['nama_kelas']
            sub_Nama_kelas = request.form['sub_nama_kelas']
            kategori_kelas = request.form['kategori_kelas']
            harga_kelas = request.form['harga_kelas']
            deskripsi_kelas = request.form['deskripsi_kelas']
            tingkatan_kelas = request.form['tingkatan_kelas']

            gambar = request.files['gambar_kelas']
            if gambar :
                kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
                gambar_name = kelas.get('gambar_kelas')
                if gambar_name:
                    lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Imgkelas', gambar_name)
                    if os.path.exists(lokasi_gambar):
                        os.remove(lokasi_gambar)

                extension = gambar.filename.split('.')[-1]
                today = datetime.now()
                mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
                gambar_name = f'gambar-{mytime}.{extension}'
                save_to = f'app/static/image/Imgkelas/{gambar_name}'
                gambar.save(save_to)

            doc_kelas = {
                'nama_kelas': Nama_kelas,
                'sub_nama_kelas': sub_Nama_kelas,
                'kategori_kelas': kategori_kelas,
                'harga_kelas': harga_kelas,
                'deskripsi_kelas': deskripsi_kelas,
                'tingkatan_kelas': tingkatan_kelas
            }

            if gambar:
                doc_kelas['gambar_kelas'] = gambar_name

            current_app.db.semuakelas.update_one({'_id' : ObjectId(_id)}, {'$set' : doc_kelas})
            msg = 'edit'
            return redirect(url_for('semuakelas.semuakelas_', msg=msg))

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
    else:
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(
                token_receive,
                SECRET_KEY,
                algorithms=['HS256']
            )
            user_info = current_app.db.user.find_one(
                {'email': payload.get('id')})
            status = payload.get('id')
            user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
            data_kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
        
            if user_admin:
                return render_template('admin_panel/tambah_kelas.html', user_info=user_info, status_admin=status, kelas = data_kelas)

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
