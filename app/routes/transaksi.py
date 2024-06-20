from flask import Blueprint, render_template, current_app, redirect, url_for, request,jsonify
import jwt
from datetime import datetime
from bson import ObjectId
import midtransclient
import uuid

transaksi_ = Blueprint('transaksi', __name__)

@transaksi_.route('/transaksi', methods=['POST'])
def transaksi():
    id_kelas = request.form.get('id_kelas')
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
        "id_kelas": ObjectId(id_kelas),
        "user_id": ObjectId(user_id),
        "kelas_nama": kelas_nama,
        "kelas_harga": int(kelas_harga),
        "order_id": order_id,
        "transaction_token": transaction_token,
        "status": "pending"
    }

    current_app.db.transaksi.insert_one(data_transaksi)

    return jsonify({
        'id' : order_id
    })

@transaksi_.route('/transaksi/<id>')
def payment(id):
    data = current_app.db.transaksi.find_one({'order_id' : id})
    return render_template('admin_panel/payment.html', data=data)
