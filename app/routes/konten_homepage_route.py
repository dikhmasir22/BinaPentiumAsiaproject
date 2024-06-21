from flask import Blueprint, render_template, request, current_app, redirect, url_for
import jwt
from datetime import datetime
import os
from bson import ObjectId

konten_homepage = Blueprint('homepagekonten', __name__)

# Carousel Image Routes
@konten_homepage.route('/carousel')
def carousel():
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
        carousel_image = list(current_app.db.carousel.find({}))
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        status = payload.get('id')
        if super_admin:
            return render_template('admin_panel/carousel.html', user_info = user_info, status_superadmin = status, msg = msg, carousel = carousel_image)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return redirect(url_for('homepage.homepage', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return redirect(url_for('homepage.homepage', msg = msg))
    
@konten_homepage.route('/tambah_carousel', methods = ['GET', 'POST'])
def tambah_carousel():
    if request.method == 'POST':
        TOKEN_KEY = current_app.config['TOKEN_KEY']
        SECRET_KEY = current_app.config['SECRET_KEY']
        token_receive = request.cookies.get(TOKEN_KEY)
        try:
            payload = jwt.decode(token_receive, SECRET_KEY,
                                 algorithms=['HS256'])
            
            gambar = request.files['gambar_carousel']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambar_carousel-{mytime}.{extension}'
            save_to = f'app/static/image/Imgcarousel/{gambar_name}'
            gambar.save(save_to)

            doc_carousel = {
                'gambar_carousel': gambar_name
            }

            current_app.db.carousel.insert_one(doc_carousel)
            msg = 'tambah_carousel'
            return redirect(url_for('homepagekonten.carousel', msg=msg))

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
            super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        
            if super_admin:
                return render_template('admin_panel/tambah_carousel.html', user_info = user_info, status_superadmin = status)

        except jwt.ExpiredSignatureError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))
        except jwt.exceptions.DecodeError:
            msg = 'Your Token Has Expired'
            return redirect(url_for('homepage.homepage', msg=msg))

@konten_homepage.route('/hapus_carousel/<_id_carousel>')
def hapus_carousel(_id_carousel):
    carousel = current_app.db.carousel.find_one({'_id' : ObjectId(_id_carousel)})
    gambar_name = carousel.get('gambar_carousel')
    if gambar_name:
        lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Imgcarousel', gambar_name)
        if os.path.exists(lokasi_gambar):
            os.remove(lokasi_gambar)
    
    current_app.db.carousel.delete_one({'_id' : ObjectId(_id_carousel)})
    msg = 'hapus_carousel'
    return redirect(url_for('homepagekonten.carousel', msg = msg))

@konten_homepage.route('/edit_carousel/<_id_carousel>', methods = ['POST'])
def edit_carousel(_id_carousel):
    carousel = current_app.db.carousel.find_one({'_id' : ObjectId(_id_carousel)})
    gambar_name = carousel.get('gambar_carousel')
    if gambar_name:
        lokasi_gambar = os.path.join(current_app.root_path, 'static', 'image', 'Imgcarousel', gambar_name)
        if os.path.exists(lokasi_gambar):
            os.remove(lokasi_gambar)
    
    gambar = request.files['gambar_carousel']
    extension = gambar.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
    gambar_name = f'gambar_carousel-{mytime}.{extension}'
    save_to = f'app/static/image/Imgcarousel/{gambar_name}'
    gambar.save(save_to)

    doc_carousel = {
        'gambar_carousel': gambar_name
    }
    
    current_app.db.carousel.update_one({'_id' : ObjectId(_id_carousel)}, {'$set' : doc_carousel})
    msg = 'edit_carousel'
    return redirect(url_for('homepagekonten.carousel', msg = msg))



# Carousel Image Routes

@konten_homepage.route('/media_sosial')
def media_sosial():
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
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        status = payload.get('id')
        if super_admin:
            return render_template('admin_panel/media_sosial.html', user_info = user_info, status_superadmin = status)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/materi.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/materi.html', msg=msg)
    
@konten_homepage.route('/pesan')
def pesan():
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
        super_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'superadmin'})
        status = payload.get('id')
        if super_admin:
            return render_template('admin_panel/pesan.html', user_info = user_info, status_superadmin = status)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/materi.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/materi.html', msg=msg)

