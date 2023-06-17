import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from datetime import datetime

# Replace this with the path to your Firebase service account JSON file
service_account_path = 'service-account-credentials.json'

# Initialize the Firebase app
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

def send_notification_topic(item, data):
        message = messaging.Message(
             data=data,
        notification=messaging.Notification(
            title='Sample Notification',
            body='This is a sample notification for subscribed users',
        ),
        topic=item
        )

        try:
            response = messaging.send(message)
            print('Notification sent successfully to banana:', response)
        except Exception as error:
            print('Error sending notification:', error)


send_notification_topic(item='heavenly_inquisition_sword',
                        data={'title': 'Heavenly Inquisition Sword', 
                         'subtitle': 'Chapter 32', 
                         'cover_link': 'https://www.asurascans.com/wp-content/uploads/2022/10/inquisitionSwordCover02.png', 
                         'chapter_link': 'https://www.asurascans.com/manga/4569947261-heavenly-inquisition-sword/', 
                         'date': datetime.now().isoformat()
                         })