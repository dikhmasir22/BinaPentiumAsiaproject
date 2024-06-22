from flask import Blueprint, render_template, current_app, redirect, url_for, request,jsonify
import jwt
from datetime import datetime
from bson import ObjectId
import midtransclient
import uuid

transaksi_ = Blueprint('transaksi', __name__)

@transaksi_.route('/transaksi', methods=['POST'])
def transaksi():
    id_kelas = request.form.get('kelas_id')
    nama_lengkap = request.form.get('nama')
    user_id = request.form.get('user_id')
    kelas_harga = request.form.get('kelas_harga')
    kelas_nama = request.form.get('kelas_nama')
    email = request.form.get('email')
    order_id = str(uuid.uuid1())

    snap = midtransclient.Snap(
        is_production = False,
        server_key = 'SB-Mid-server-FMMkLWM6rj2RGC2XiHMevXfH',
        client_key = 'SB-Mid-client-EUKPwnA2TMKkqkoq'
    )

    data = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": int(kelas_harga)
        },
        "item_details": [{
            "id": id_kelas,
            "price": int(kelas_harga),
            "quantity": 1,
            "name": kelas_nama
        }],
        "customer_details": {
            "first_name": nama_lengkap
        }
    }

    transaction = snap.create_transaction(data)
    transaction_token = transaction['token']

    data_transaksi = {
        "_id_kelas": ObjectId(id_kelas),
        "_id_siswa": ObjectId(user_id),
        "kelas_nama": kelas_nama,
        "kelas_harga": int(kelas_harga),
        "order_id": order_id,
        "transaction_token": transaction_token,
        "status": "pending"
    }

    current_app.db.transaksi.insert_one(data_transaksi)

    return jsonify({
        'order_id' : order_id
    })

@transaksi_.route('/daftar_transaksi')
def riwayat_transaksi():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try :
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        msg = request.args.get('msg')
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        status = payload.get('id')
        data_transaksi = list(current_app.db.transaksi.find({'_id_siswa' : user_info['_id']}))
        return render_template('admin_panel/daftar_transaksi.html', status = status, transaksi = data_transaksi, user_info = user_info, msg = msg)

    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))

@transaksi_.route('/transaksi_sukses', methods = ['POST'])
def sukses_bayar():
    _id_transaksi = request.form.get('_id_transaksi')
    _id_kelas = request.form.get('_id_kelas')
    _id_siswa = request.form.get('_id_siswa')
    print(_id_kelas)

    current_app.db.transaksi.update_one({'_id' : ObjectId(_id_transaksi)}, {'$set' : {'status' : 'sudah bayar'}})
    return redirect(url_for('ikuti_kelas.ikuti_kelas', _id=str(_id_kelas), _idsiswa=str(_id_siswa)))

@transaksi_.route('/transaksi/<id>')
def payment(id):
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try :
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_info = current_app.db.user.find_one({'email': payload.get('id')})
        data = current_app.db.transaksi.find_one({'order_id' : id})
        status = payload.get('id')
        return render_template('admin_panel/payment.html', data=data, user_info = user_info, status = status )

    except jwt.ExpiredSignatureError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))
    except jwt.exceptions.DecodeError:
        msg = 'Your Token Has Expired'
        return redirect(url_for('homepage.homepage', msg=msg))

@transaksi_.route('/hapus_transaksi/<_id_transaksi>')
def hapus_transaksi(_id_transaksi):
    current_app.db.transaksi.delete_one({'_id' : ObjectId(_id_transaksi)})
    msg = 'hapus_transaksi'
    return redirect(url_for('transaksi.riwayat_transaksi', msg = msg))