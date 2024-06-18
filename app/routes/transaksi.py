from flask import Blueprint, render_template, current_app, redirect, url_for, request
import jwt
from datetime import datetime
from bson import ObjectId
from midtransclient import Snap

transaksi_ = Blueprint('transaksi', __name__)

@transaksi_.route('/transaksi', methods=['POST'])
def create_transaction():
    data = request.json
    user_id = data['user_id']
    kelas_id = data['kelas_id']
    kelas_harga = data['kelas_harga']
    kelas_nama = data['kelas_nama']
    email = data['email']
    phone = data['phone']

    snap = Snap(
        is_production=False,
        server_key='SB-Mid-client-EUKPwnA2TMKkqkoq',
        client_key='SB-Mid-server-FMMkLWM6rj2RGC2XiHMevXfH'
    )

    transaction = {
        "transaction_details": {
            "order_id": f"order-{user_id}-{kelas_id}",
            "gross_amount": kelas_harga
        },
        "item_details": [
            {
                "id": kelas_id,
                "price": kelas_harga,
                "quantity": 1,
                "name": kelas_nama
            }
        ],
        "customer_details": {
            "email": email,
            "phone": phone
        }
    }
    try:
        snap_response = snap.create_transaction(transaction)
        return jsonify({
            'redirect_url': snap_response['redirect_url'],
            'token': snap_response['token']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@transaksi_.route('/midtrans-notifikasi', methods=['POST'])
def midtrans_notifikasi():
    notification_json = request.json
    order_id = notification_json.get('order_id')
    transaction_status = notification_json.get('transaction_status')
    fraud_status = notification_json.get('fraud_status')
    
    try:
        order_parts = order_id.split('-')
        user_id = order_parts[1]
        kelas_id = order_parts[2]

        if transaction_status == 'capture':
            if fraud_status == 'accept':
                update_kelas_diambil(user_id, kelas_id, status='success')
            elif fraud_status == 'challenge':
                update_kelas_diambil(user_id, kelas_id, status='challenge')
            else:
                update_kelas_diambil(user_id, kelas_id, status='deny')

        elif transaction_status == 'settlement':
            update_kelas_diambil(user_id, kelas_id, status='success')

        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            update_kelas_diambil(user_id, kelas_id, status='failed')

        elif transaction_status == 'pending':
            update_kelas_diambil(user_id, kelas_id, status='pending')

        return jsonify({'status': 'ok'})
    except Exception as e:
        logging.error(f"Error processing Midtrans notification: {str(e)}")
        return jsonify({'error': str(e)}), 500

def update_kelas_diambil(user_id, kelas_id, status):
    db = current_app.db
    user_oid = ObjectId(user_id)
    kelas_oid = ObjectId(kelas_id)
    
    if status == 'success':
        db.user.update_one(
            {'_id': user_oid},
            {'$addToSet': {'kelas_diambil': kelas_oid}}
        )
    else:
        db.user.update_one(
            {'_id': user_oid},
            {'$set': {f'kelas_status.{kelas_oid}': status}}
        )