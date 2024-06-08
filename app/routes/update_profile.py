from flask import Blueprint, render_template, current_app, redirect, url_for, request
import jwt

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
            email = email.lower()
            email = email.split('@')[0]
            namalengkap = request.form['nama_lengkap']
            no_telepon = request.form['no_telepon']
            no_ktp = request.form['no_ktp']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            tempat_tanggal_lahir = request.form['tempat_tanggal_lahir']



            

            doc = {
                "email": email,                             
                "password": password_hash,                          
                "nama_lengkap": namalengkap,
                "nama_depan": namadepan,
                "deskripsi" : "",
                "no_telepon": "",
                "no_ktp": "",
                "jenis_kelamin": "",
                "tempat_tanggal_lahir": "",
                "alamat": "",
                "level" : "user",
                "foto_profile" : ""
            }



            status = payload.get('id')
            user_admin = current_app.db.user.find_one({'email': payload.get('id'),'level': 'admin'})
        
            if user_admin:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status_admin = status)
            else:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status = status)
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
            user_admin = current_app.db.user.find_one({
                'email': payload.get('id'),
                'level': 'admin'})
        
            if user_admin:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status_admin = status)
            else:
                return render_template('admin_panel/update_profile.html', user_info=user_info, status = status)
        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
