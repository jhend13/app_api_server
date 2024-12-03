import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

# Firebase setup
# should use the recommended way of utilizing the GOOGLE_APPLICATION_CREDENTIALS environvar
cred = credentials.Certificate(
    'C:\\Users\\jhend\\keys\\aadd-be709-firebase-adminsdk-ouy5k-f31c82021f.json')
app = firebase_admin.initialize_app(cred)

print(app.project_id)

token = 'e_3TvKBRSPqqCqT2Aai9hf:APA91bFT7KLcvrafR8OqRclF4X8d846-3H5aMiHiEpKew9MzxrB6l0J3i1lwWACdddeP4fJlZkNI6cWAehQ0La97OAJP5dQPWM_3nYynJUt4NghvYrJJE8U'
message = messaging.Message(
    data={'title': 'server msg', 'body': 'msg sent from server'}, token=token)

credentials
# firebase_admin.messaging.send(firebase_admin.messaging.Message({'' : ''}))
