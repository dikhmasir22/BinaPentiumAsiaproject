from flask import Blueprint, render_template, current_app, redirect, url_for, request
import jwt
from datetime import datetime
from bson import ObjectId

update_profile_ = Blueprint('update_profile', __name__)

@update_profile_.route('/update_profile', methods = ['GET', 'POST'])
def update_profile():

    if request.method == 'POST':
        
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive,SECRET_KEY,algorithms=['HS256'])
            user_info = current_app.db.user.find_one({'email': payload.get('id')})

            email = request.form['email']
            namalengkap = request.form['nama_lengkap']
            namadepan = namalengkap.split(' ')[0]
            no_telepon = request.form['no_telepon']
            no_ktp = request.form['no_ktp']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']
            deskripsi = request.form['deskripsi']

            gambar = request.files['foto_profile']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambar-{mytime}.{extension}'
            save_to = f'app/static/image/Imgprofile/{gambar_name}'
            gambar.save(save_to)

            password = user_info.get('password', '')

            doc = {
                "email": email,                             
                "password": password,                          
                "nama_lengkap": namalengkap,
                "nama_depan": namadepan,
                "deskripsi" : deskripsi,
                "no_telepon": no_telepon,
                "no_ktp": no_ktp,
                "jenis_kelamin": jenis_kelamin,
                "tempat_tanggal_lahir": tempat_tanggal_lahir,
                "alamat": alamat,
                "level" : user_info['level'],
            }

            if gambar:
                doc['foto_profile'] = gambar_name
            
            current_app.db.user.update_one({'_id' : ObjectId(user_info['_id'])}, {'$set' : doc})
            msg = 'edit'
            return redirect(url_for('update_profile.update_profile', msg=msg))
        
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
            msg = request.args.get('msg')
            user_info = current_app.db.user.find_one({'email': payload.get('id')})
            status = payload.get('id')
            user_admin = current_app.db.user.find_one({
                'email': payload.get('id'),
                'level': 'admin'})
            super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        
            if user_admin:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status_admin = status, msg = msg)
            elif super_admin:
                return render_template('admin_panel/update_profile.html', user_info = user_info, status_superadmin = status)
            else:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status = status, msg = msg)
        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))

