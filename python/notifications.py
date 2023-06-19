import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from datetime import datetime, timedelta

# Replace this with the path to your Firebase service account JSON file
service_account_path = 'service-account-credentials.json'

# Initialize the Firebase app
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)


def send_notification_topic(item, data):
    message = messaging.Message(
        data=data,
        notification=messaging.Notification(
            title=f"{data['manhwa_title']}",
            body=data['chapter_number'],
        ),
        topic=item
    )

    try:
        response = messaging.send(message)
        print('Notification sent successfully to banana:', response)
    except Exception as error:
        print('Error sending notification:', error)


time = datetime.now() - timedelta(days=5)

# send_notification_topic(item='player_who_returned_10000_years_later',
#                         data={'manhwa_title': 'Player Who Returned 10,000 Years Later',
#                               'chapter_number': 'Chapter 64',
#                               'chapter_url': 'https://www.asurascans.com/player-who-returned-10000-years-later-chapter-63/',
#                               'cover_url': 'https://www.asurascans.com/wp-content/uploads/2022/07/Player10000yearsCover02_copy.png',
#                               'notification_timestamp':  time.isoformat()
#                               })


send_notification_topic(item='heavenly_inquisition_sword',
                        data={'manhwa_title': 'Heavenly Inquisition Sword',
                              'chapter_number': 'Chapter 32',
                              'chapter_url': 'https://www.asurascans.com/manga/4569947261-heavenly-inquisition-sword/',
                              'cover_url': 'https://www.asurascans.com/wp-content/uploads/2022/10/inquisitionSwordCover02.png',
                              'notification_timestamp': datetime.now().isoformat()
                              })
