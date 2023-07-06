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
        write_log(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Notification: Success sending {item}")
    except Exception as error:
        print('Error sending notification:', error)
        write_log(
            f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Notification: Error sending {item}: {error}")


def save_notification_to_firestore(data, item):
    doc_ref = db.collection('notifications').document(
        item).collection('notifications')
    doc_ref.add(data)


def get_clean_topic(scanlator_name, topic):
    return scanlator_name.strip().lower() + '_' + topic.strip().replace('`', '').replace('’', '').replace(',', '').replace('\'', '').replace('!', '').replace(' ', '_').lower()


def write_log(log_message):
    with open('scraping_logs.txt', 'a') as file:
        file.write(log_message + '\n')
