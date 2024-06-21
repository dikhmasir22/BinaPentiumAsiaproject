from flask import Blueprint, render_template, request, current_app, redirect, url_for
import jwt

dashboard_admin = Blueprint('dashboard_admin', __name__)


@dashboard_admin.route('/dashboard', methods=['GET'])
def dashboard():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        msg = request.args.get('msg')
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        status = payload.get('id')
        siswa = list(current_app.db.user.find({'level': 'user'}))
        jumlah_siswa = len(siswa)
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})

        if user_admin:
            semua_kelas = list(current_app.db.semuakelas.find({}))
            data_kelas = []
            for item in semua_kelas:
                kelas_saya = list(current_app.db.kelassaya.find({'_id_kelas': item['_id']}))
                jumlah_siswa_ambil_kelas = len(kelas_saya)

                data_kelas.append({
                    'nama_kelas': item['nama_kelas'],
                    'sub_nama_kelas': item['sub_nama_kelas'],
                    'kategori_kelas': item['kategori_kelas'],
                    'harga_kelas': item['harga_kelas'],
                    'deskripsi_kelas': item['deskripsi_kelas'],
                    'tingkatan_kelas': item['tingkatan_kelas'],
                    'gambar_kelas': item['gambar_kelas'],
                    'jumlah_siswa' : jumlah_siswa_ambil_kelas
                })
            
            return render_template('admin_panel/dashboard_admin.html', user_info=user_info, status_admin=status, msg=msg, jumlah_siswa=jumlah_siswa, data_kelas = data_kelas)
        elif super_admin:
            carousel_image = list(current_app.db.carousel.find({}))
            return render_template('admin_panel/dashboard_admin.html', user_info = user_info, status_superadmin = status, carousel = carousel_image)
        else:
            kelas_diambil = list(current_app.db.kelassaya.find(
                {'_id_siswa': user_info['_id']}))
            jumlah_kelas_diambil = len(kelas_diambil)
            return render_template('admin_panel/dashboard_admin.html', user_info=user_info, status=status, msg=msg, jumlah_kelas_diambil=jumlah_kelas_diambil)
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
