from flask import Blueprint, render_template, request, current_app
import jwt
from bson import ObjectId

detailkelas_ = Blueprint('detailkelas', __name__)

@detailkelas_.route('/detailkelas/<_id>')
def detailkelas(_id):
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
    menu_materi = list(current_app.db.menumateri.find({'_id_kelas' : kelas['_id']}))
    medsos = current_app.db.medsos.find_one({})
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})
        kelas_diambil = current_app.db.kelassaya.find_one({'_id_kelas' : ObjectId(_id), '_id_siswa' :user_info['_id']})
        user_admin = current_app.db.user.find_one({
            'email': payload.get('id'),
            'level': 'admin'})     
        status = payload.get('id')

        if kelas_diambil:
            user_pernah_mulai = current_app.db.menumaterisiswa.find_one({'_id_siswa' : user_info['_id'], '_id_kelas' : kelas_diambil['_id_kelas']})

        if user_admin:
            return render_template('admin_panel/detailkelas.html', status_admin = status, user_info=user_info, kelas = kelas, menu_materi = menu_materi)
        else:
            if kelas_diambil:
                if user_pernah_mulai:
                    return render_template('admin_panel/detailkelas.html', status = status, user_info=user_info, kelas = kelas, kelas_diambil = kelas_diambil, user_pernah_mulai = user_pernah_mulai, menu_materi = menu_materi)
                else:
                    return render_template('admin_panel/detailkelas.html', status = status, user_info=user_info, kelas = kelas, kelas_diambil = kelas_diambil, menu_materi = menu_materi)
            else :
                return render_template('admin_panel/detailkelas.html', status = status, user_info=user_info, kelas = kelas, menu_materi = menu_materi)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/detail_kelas_guest.html', msg=msg, kelas = kelas, menu_materi = menu_materi, medsos = medsos)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/detail_kelas_guest.html', msg=msg, kelas = kelas, menu_materi = menu_materi, medsos = medsos)

