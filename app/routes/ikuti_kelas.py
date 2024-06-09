from flask import Blueprint, render_template, current_app, request, redirect, url_for
import jwt
from bson import ObjectId

ikuti_kelas_ = Blueprint('ikuti_kelas', __name__)

@ikuti_kelas_.route('/ikuti_kelas/<_id>/<_idsiswa>',methods=['POST'])
def ikuti_kelas(_id,_idsiswa):
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        kelas = current_app.db.semuakelas.find_one({'_id' : ObjectId(_id)})

        kelas_sudah_diambil = current_app.db.kelassaya.find_one({
            '_id_kelas' : ObjectId(_id),
            '_id_siswa' : ObjectId(_idsiswa) 
        })

        if kelas_sudah_diambil:
            msg = 'sudah'
            return redirect(url_for('kelassaya.kelassaya', msg = msg))
        
        else:
            doc = {
                '_id_kelas' : ObjectId(_id),
                '_id_siswa' : ObjectId(_idsiswa),
                'nama_kelas': kelas['nama_kelas'],
                'sub_nama_kelas': kelas['sub_nama_kelas'],
                'kategori_kelas': kelas['kategori_kelas'],
                'harga_kelas': kelas['harga_kelas'],
                'deskripsi_kelas': kelas['deskripsi_kelas'],
                'tingkatan_kelas': kelas['tingkatan_kelas'],
                'gambar_kelas': kelas['gambar_kelas']
            }
            current_app.db.kelassaya.insert_one(doc)
            msg = 'ikut_kelas'
            return redirect(url_for('kelassaya.kelassaya', msg = msg))
    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
