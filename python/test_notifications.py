import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from datetime import datetime, timedelta
from firebase_admin import firestore

service_account_path = 'service-account-credentials.json'

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()


def send_notification_topic(item, data):
    message = messaging.Message(
        data=data,
        notification=messaging.Notification(
            title=f"{data['manhwa_title']}",
            body=data['chapter_number'],
        ),
        topic=item,
    )

    try:
        response = messaging.send(message)
        print(f'Sending notification to {item}:', response)
        save_notification_to_firestore(data, item)
    except Exception as error:
        print('Error sending notification:', error)


def save_notification_to_firestore(data, item):
    doc_ref = db.collection('notifications').document(
        item).collection('notifications')
    doc_ref.add(data)