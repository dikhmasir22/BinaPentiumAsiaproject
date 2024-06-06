from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from datetime import datetime, timedelta

tambah_kelas_ = Blueprint('tambah_kelas', __name__)


@tambah_kelas_.route('/tambahkelas', methods=['GET', 'POST'])
def tambah_kelas():
    if request.method == 'POST':
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive,SECRET_KEY,algorithms=['HS256'])
            Nama_kelas = request.form['nama_kelas']
            sub_Nama_kelas = request.form['sub_nama_kelas']
            kategori_kelas = request.form['kategori_kelas']
            harga_kelas = request.form['harga_kelas']
            deskripsi_kelas = request.form['deskripsi_kelas']

            gambar = request.files['gambar_kelas']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambar-{mytime}.{extension}'
            save_to = f'app/static/image/Imgkelas/{gambar_name}'
            gambar.save(save_to)

            doc_kelas = {
                'nama_kelas' : Nama_kelas,
                'sub_nama_kelas' : sub_Nama_kelas,
                'kategori_kelas' : kategori_kelas,
                'harga_kelas' : harga_kelas,
                'deskripsi_kelas' : deskripsi_kelas,
                'gambar_kelas' : gambar_name
            }

            current_app.db.semuakelas.insert_one(doc_kelas)
            msg = 'Kelas Berhasil Ditambahkan'
            return redirect(url_for('semuakelas.semuakelas_', msg = msg))
        
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
            user_info = current_app.db.user.find_one({'email': payload.get('id')})
            status = payload.get('id')
            return render_template('admin_panel/tambah_kelas.html', user_info=user_info, status_admin = status)
        
        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
