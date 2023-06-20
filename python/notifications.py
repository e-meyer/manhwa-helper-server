import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from datetime import datetime, timedelta
from firebase_admin import firestore


# Replace this with the path to your Firebase service account JSON file
service_account_path = 'service-account-credentials.json'

# Initialize the Firebase app
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


time = datetime.now() - timedelta(days=5)


def notify_player_who_returned_10000_years_later():
    send_notification_topic(item='player_who_returned_10000_years_later',
                            data={'manhwa_title': 'Player Who Returned 10,000 Years Later',
                                  'chapter_number': 'Chapter 64',
                                  'chapter_url': 'https://www.asurascans.com/player-who-returned-10000-years-later-chapter-63/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2022/07/Player10000yearsCover02_copy.png',
                                  'notification_timestamp':  time.isoformat()
                                  })


def notify_heavenly_inquisition_sword():
    send_notification_topic(item='heavenly_inquisition_sword',
                            data={'manhwa_title': 'Heavenly Inquisition Sword',
                                  'chapter_number': 'Chapter 32',
                                  'chapter_url': 'https://www.asurascans.com/manga/4569947261-heavenly-inquisition-sword/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2022/10/inquisitionSwordCover02.png',
                                  'notification_timestamp': datetime.now().isoformat()
                                  })


def notify_i_obtained_a_mythic_item():
    send_notification_topic(item='i_obtained_a_mythic_item',
                            data={'manhwa_title': 'I Obtained a Mythic Item',
                                  'chapter_number': 'Chapter 59',
                                  'chapter_url': 'https://www.asurascans.com/i-obtained-a-mythic-item-chapter-59/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2022/06/IObtainedaMythicItemCover04.png',
                                  'notification_timestamp': datetime.now().isoformat()
                                  })


def notify_the_max_level_hero_has_returned():
    send_notification_topic(item='the_max_level_hero_has_returned',
                            data={'manhwa_title': 'The Max Level Hero has Returned',
                                  'chapter_number': 'Chapter 133',
                                  'chapter_url': 'https://www.asurascans.com/the-max-level-hero-has-returned-chapter-133/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2020/10/maxlevelheroCover01.png',
                                  'notification_timestamp': (datetime.now() - timedelta(days=3)).isoformat()
                                  })


def notify_the_s_classes_that_i_raised():
    send_notification_topic(item='the_s_classes_that_i_raised',
                            data={'manhwa_title': 'The S-Classes That I Raised',
                                  'chapter_number': 'Chapter 91',
                                  'chapter_url': 'https://www.asurascans.com/the-s-classes-that-i-raised-chapter-91/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2021/11/thesclassesthatiraisedcover.jpg',
                                  'notification_timestamp': (datetime.now() - timedelta(days=1, hours=6)).isoformat()
                                  })


def notify_i_reincarnated_as_the_crazed_heir():
    send_notification_topic(item='i_reincarnated_as_the_crazed_heir',
                            data={'manhwa_title': 'I Reincarnated As The Crazed Heir',
                                  'chapter_number': 'Chapter 132',
                                  'chapter_url': 'https://www.asurascans.com/i-reincarnated-as-the-crazed-heir-master-of-the-heavenly-palace-1/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2021/07/Title-Cover-kopya.png',
                                  'notification_timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
                                  })


def notify_demonic_evolution():
    send_notification_topic(item='demonic_evolution',
                            data={'manhwa_title': 'Demonic Evolution',
                                  'chapter_number': 'Chapter 16',
                                  'chapter_url': 'https://www.asurascans.com/demonic-evolution-chapter-16/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2023/02/tIEELUSJN.webp-t.w640-vert-copyCUnetauto_scaleLevel3width-1000.jpg',
                                  'notification_timestamp': (datetime.now() - timedelta(days=2, hours=4)).isoformat()
                                  })


def notify_chronicles_of_the_demon_faction():
    send_notification_topic(item='chronicles_of_the_demon_faction',
                            data={'manhwa_title': 'Chronicles of the Demon Faction',
                                  'chapter_number': 'Chapter 21',
                                  'chapter_url': 'https://www.asurascans.com/chronicles-of-the-demon-faction-chapter-21/',
                                  'cover_url': 'https://www.asurascans.com/wp-content/uploads/2023/03/DemonFactionCover02.png',
                                  'notification_timestamp': (datetime.now() - timedelta(days=4)).isoformat()
                                  })


# Check the command-line arguments and call the appropriate function
if len(sys.argv) == 2:
    parameter = sys.argv[1]
    if parameter == 'player':
        notify_player_who_returned_10000_years_later()
    elif parameter == 'heavenly':
        notify_heavenly_inquisition_sword()
    elif parameter == 'mythic':
        notify_i_obtained_a_mythic_item()
    elif parameter == 'maxlevel':
        notify_the_max_level_hero_has_returned()
    elif parameter == 'raised':
        notify_the_s_classes_that_i_raised()
    elif parameter == 'crazed':
        notify_i_reincarnated_as_the_crazed_heir()
    elif parameter == 'demonic':
        notify_demonic_evolution()
    elif parameter == 'demonfaction':
        notify_chronicles_of_the_demon_faction()
    else:
        print("Invalid parameter.")
else:
    print("Usage: python3 notifications.py <parameter>")
