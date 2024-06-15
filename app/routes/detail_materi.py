from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId

detail_materi = Blueprint('detail_materi', __name__)

@detail_materi.route('/detailmateri/<_id_kelas>/<_id_menu>',methods=['GET','POST'])
def det_materi(_id_kelas, _id_menu):
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

        if _id_kelas is None:
            _id_kelas = request.args.get('_id_kelas')

        detail_kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id_kelas)})
        info_kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id_kelas)})
        status = payload.get('id')
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})
        
        if _id_menu == 'none':
            menu_materi = list(current_app.db.menumateri.find({'_id_kelas' : detail_kelas['_id']}))
            if menu_materi:
                if user_admin:
                    belum_klik_menu = 'belum'
                    return render_template('materi/laman_materi.html', user_info=user_info, status_admin = status, menu_materi = menu_materi, info_kelas = info_kelas, belum_klik_menu= belum_klik_menu)
                else:
                    print('user masuk Kesini')
                    for item in menu_materi:
                        menu_materi_siswa = list(current_app.db.menumaterisiswa.find({'_id_menu' : item['_id'], '_id_siswa' : user_info['_id'], '_id_kelas' : ObjectId(_id_kelas)}))
                        if not menu_materi_siswa:
                            doc_menu_materi_siswa = {
                                '_id_siswa' : user_info['_id'],
                                '_id_kelas' : ObjectId(_id_kelas),
                                '_id_menu' : item['_id'],
                                'judul_materi' : item['judul_materi'],
                                'status' : 'belum'
                            }
                            current_app.db.menumaterisiswa.insert_one(doc_menu_materi_siswa)
                    menu_materi_siswa = current_app.db.menumaterisiswa.find_one({'_id_siswa' : user_info['_id'], '_id_kelas' : ObjectId(_id_kelas)})
                    return redirect(url_for('detail_materi.det_materi', _id_kelas = _id_kelas, _id_menu = menu_materi_siswa['_id_menu']))
            else:
                if user_admin:
                    return render_template('materi/laman_materi.html', user_info=user_info, status_admin = status, kosong = 'kosong', info_kelas = info_kelas)
                else:
                    return render_template('materi/laman_materi.html', user_info=user_info, status = status, kosong = 'kosong', info_kelas = info_kelas)
        else:
            menu_materi = list(current_app.db.menumateri.find({'_id_kelas' : detail_kelas['_id']}))
            menu_materi_sekarang = current_app.db.menumateri.find_one({'_id' : ObjectId(_id_menu)})
            konten_materi = list(current_app.db.kontenmateri.find({'_id_menu' : ObjectId(_id_menu)}))

            if not konten_materi:
                konten_materi = current_app.db.menumateri.find({'_id' : ObjectId(_id_menu)})
            if user_admin:
                return render_template('materi/laman_materi.html', user_info=user_info, status_admin = status, menu_materi = menu_materi, konten_materi = konten_materi, info_kelas = info_kelas, menu_materi_sekarang = menu_materi_sekarang)
            else:
                for item in menu_materi:
                        menu_materi_siswa = list(current_app.db.menumaterisiswa.find({'_id_menu' : item['_id'], '_id_siswa' : user_info['_id'], '_id_kelas' : ObjectId(_id_kelas)}))
                        if not menu_materi_siswa:
                            doc_menu_materi_siswa = {
                                '_id_siswa' : user_info['_id'],
                                '_id_kelas' : ObjectId(_id_kelas),
                                '_id_menu' : item['_id'],
                                'judul_materi' : item['judul_materi'],
                                'status' : 'belum'
                            }
                            current_app.db.menumaterisiswa.insert_one(doc_menu_materi_siswa)
                menu_materi_siswa = list(current_app.db.menumaterisiswa.find({'_id_siswa' : user_info['_id'], '_id_kelas' : ObjectId(_id_kelas)}))
                return render_template('materi/laman_materi.html', user_info=user_info, status = status, menu_materi_siswa = menu_materi_siswa, konten_materi = konten_materi, info_kelas = info_kelas, menu_materi_sekarang = menu_materi_sekarang)

    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
