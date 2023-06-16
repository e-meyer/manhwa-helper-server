import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Replace this with the path to your Firebase service account JSON file
service_account_path = 'service-account-credentials.json'

# Initialize the Firebase app
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)


def send_notification_token():
    device_token = "f836y-Y8RtKcS6lHkOanFH:APA91bGRnWp8aHoIGRYzdThDycWpRhErA12Q2jK9-FEI-Kb_K7P0zFKFsw5chO6sZ893kfmTETtOrYRP_vmwVwBSYMQYyOe6lWJSy9KHC1BtzY76Hnhb8KKnORyF_AGUom5WpY2-4ce1"
    message = messaging.Message(
        notification=messaging.Notification(
            title="Notification Title",
            body="Notification Body"
        ),
        token=device_token,
    )

    try:
        response = messaging.send(message)
        print('Notification sent successfully to token:', response)
    except Exception as error:
        print('Error sending notification:', error)


def send_notification_topic():
    message = messaging.Message(
        notification=messaging.Notification(
            title='Sample Notification',
            body='This is a sample notification for subscribed users',
        ),
        topic='banana'
    )

    message2 = messaging.Message(
        notification=messaging.Notification(
            title='Sample Notification',
            body='This is a sample notification for subscribed users',
        ),
        topic='french_fries'
    )

    try:
        response = messaging.send(message)
        response2 = messaging.send(message2)
        print('Notification sent successfully to banana:', response)
        print('Notification sent successfully to french_fries:', response2)
    except Exception as error:
        print('Error sending notification:', error)


send_notification_topic()
