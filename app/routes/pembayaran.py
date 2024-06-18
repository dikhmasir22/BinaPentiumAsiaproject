from flask import Blueprint, render_template, request, jsonify, current_app
import jwt
from bson import ObjectId

transaksi_ = Blueprint('transaksi', __name__)
buat_transaksi = Blueprint('buat_transaksi', __name__)

MIDTRANS_SERVER_KEY = 'SB-Mid-server-FMMkLWM6rj2RGC2XiHMevXfH'
MIDTRANS_BASE_URL = 'https://api.sandbox.midtrans.com/v2'

@transaksi_.route('/transaksi')
def transaksi():
    TOKEN_KEY = current_app.config['TOKEN_KEY']
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = jwt.decode(
            token_receive,
            SECRET_KEY,
            algorithms=['HS256']
        )
        status = payload.get('id')
        return render_template('materi/kelassaya.html', status = status)
    except jwt.ExpiredSignatureError:
        msg = request.args.get('msg')
        return render_template('template/homepage.html', msg=msg)
    except jwt.exceptions.DecodeError:
        msg = request.args.get('msg')
        return render_template('template/homepage.html', msg=msg)

@buat_transaksi.route('/buat_transaksi/<_id>/<id_kelas>', methods=["POST"])
def buat_transaksi(_id,id_kelas):
    user_info = current_app.db.user.find_one({'_id': ObjectId(_id)})
    _id_siswa = user_info['_id']

    doc_transaksi = {
        '_id_kelas': ObjectId(id_kelas),
        '_id_siswa': _id_siswa
    }

    current_app.db.transaksi.insert_one(doc_transaksi)
    id_transaksi = str(doc_transaksi['_id'])  # mengubah ObjectId menjadi string

    jumlah_total = request.json.get('jumlah_total')
    detail_user = {
        'first_name': user_info.get('first_name'),
        'last_name': user_info.get('last_name'),
        'email': user_info.get('email'),
        'phone': user_info.get('phone')
    }

    token_snap = dapatkan_token_snap(id_transaksi, jumlah_total, detail_user)
    return jsonify(token_snap)

@buat_transaksi.route('/buat_transaksi/<_id>/<id_kelas>', methods=["POST"])
def buat_transaksi(_id, id_kelas):
    user_info = current_app.db.user.find_one({'_id': ObjectId(_id)})
    _id_siswa = user_info['_id']

    doc_transaksi = {
        '_id_kelas': ObjectId(id_kelas),
        '_id_siswa': _id_siswa
    }

    current_app.db.transaksi.insert_one(doc_transaksi)
    id_transaksi = str(doc_transaksi['_id']) 

    jumlah_total = request.json.get('jumlah_total')
    detail_user = {
        'first_name': user_info.get('first_name'),
        'last_name': user_info.get('last_name'),
        'email': user_info.get('email'),
        'phone': user_info.get('phone')
    }

    token_snap = dapatkan_token_snap(id_transaksi, jumlah_total, detail_user)
    return jsonify(token_snap)

def dapatkan_token_snap(id_pesanan, jumlah_total, detail_pelanggan):
    url = f"{MIDTRANS_BASE_URL}/charge"

    header = {
        'Authorization': 'Basic ' + base64.b64encode((MIDTRANS_SERVER_KEY + ':').encode()).decode(),
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    payload = {
        "transaction_details": {
            "order_id": id_pesanan,
            "gross_amount": jumlah_total
        },
        "credit_card": {
            "secure": True
        },
        "customer_details": detail_pelanggan
    }

    response = requests.post(url, headers=header, json=payload)
    return response.json()

@transaksi_.route('/notifikasi_pembayaran', methods=['POST'])
def notifikasi_pembayaran():
    notifikasi_json = request.json
    status_transaksi = notifikasi_json.get('transaction_status')
    id_pesanan = notifikasi_json.get('order_id')

    if status_transaksi in ['capture', 'settlement']:
        current_app.db.transaksi.update_one(
            {'_id': ObjectId(id_pesanan)},
            {'$set': {'status': 'paid'}}
        )
    elif status_transaksi in ['cancel', 'expire']:
        current_app.db.transaksi.update_one(
            {'_id': ObjectId(id_pesanan)},
            {'$set': {'status': 'canceled'}}
        )

    return jsonify({"status": "success"})
    