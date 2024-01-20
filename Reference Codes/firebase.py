import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from getlocation import *
import time

#print("It Works!")

#credentials for firebase
cred = credentials.Certificate("/home/pi/Downloads/squid-3349a-firebase-adminsdk-4lbn4-5afa229c69.json")
'''firebase_admin.initialize_app(cred)'''

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://squid-3349a.firebaseio.com/'
})

#sending to firebase
while True:
    ref = db.reference() #creating a reference
    time.sleep(20)
    (lat,long, timestamp) = getloc() #getting the location from a function called getloc()

    #Sending the GPS data to the firebase
    snapshot = ref.child('GPS').child("Lat").push(lat)
    snapshot = ref.child('GPS').child("Long").push(long)
    snapshot = ref.child('GPS').child("Timestamp").push(timestamp)
