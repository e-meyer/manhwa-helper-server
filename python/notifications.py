import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Replace this with the path to your Firebase service account JSON file
service_account_path = 'service-account-credentials.json'

# Initialize the Firebase app
cred = credentials.Certificate(service_account_path)
# firebase_admin.initialize_app(cred)

def send_notification_topic(item):
        message = messaging.Message(
             data={'title': item},
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


