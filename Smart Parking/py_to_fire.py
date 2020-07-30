import firebase_admin
from firebase_admin import credentials, firestore
import google.cloud
import pytz
from datetime import datetime , timedelta

cred = credentials.Certificate('parkingapp-key.json')
firebase_admin.initialize_app(cred)

store = firestore.client()
#doc_ref = store.collection(u'users').limit(2)

#try:
 #   docs = doc_ref.get()
 #   for doc in docs:
  #      print(u'Doc Data:{}'.format(doc.to_dict()))
#except google.cloud.exceptions.NotFound:
 #   print(u'Missing data')
count = 0
while True:
    if(count == 0):
        entry = input("Enter vehicle no : ")

        user_ref = store.collection('Users').where('vechile' , '==' , entry).stream()
        for doc in user_ref:
            user = doc.id
        count = 1


    if(count == 1):
        place_ref = store.collection('Places').stream()
        placeList = []
        for place in place_ref:
            placeList.append(place.id)
        
            slot_ref = store.collection('Places').document(place.id).collection('slots').stream()
            slotList = []
            for slot in slot_ref:
                slotList.append(slot.id)

                history_ref = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').stream()
                historyList = []
                for history in history_ref:
                    historyList.append(history.id)

                    docs = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').where('user','==',user).stream()

                    for doc in docs:
                        print(doc.id)
                        store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).update(
                            {
                                'arraivaltime': datetime.now(pytz.utc)
                            }
                        )
                        print("arraivaltime updated")
    
                        time = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).get().get('starttime')
                        duration = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).get().get('duration')
                        endTime = time+timedelta(minutes = duration)
                        arraivaltime = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).get().get('arraivaltime')
                        if(endTime > arraivaltime > time):
                            store.collection('Places').document(place.id).collection('slots').document(slot.id).update(
                                {
                                    'availability':False
                                }
                            )
                            print("availability updated to false" )

                            store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).update(
                                {
                                    'exittime': endTime,
                                    'comparetime':endTime
                                }
                            )
                            print("exittime updated")
                    
                        enders = store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').where('comparetime','<', arraivaltime).stream()
                    
                        for end in enders:

                            store.collection('Places').document(place.id).collection('slots').document(slot.id).update(
                                {
                                    'availability':True
                                }
                            )
                            print("availability updated to True")

                            store.collection('Places').document(place.id).collection('slots').document(slot.id).collection('history').document(history.id).update({
                                'comparetime':None
                            })
                            
                            store.collection('Users').document(user).collection('notifications').document().set({
                                'title':"Time's Up",
                                'Message':"Your slot time is up. Please vacate",
                                'Time': endTime
                            })
                            print('notification posted')
                            user = None
                            count == 0
                            break

#doc_ref.document("Malavika").update(
#    {
#        u'Slot0':u'booked',
        
        
#    },
#)

#docs = doc_ref.where('availability','==',False).stream()

#for doc in docs:
#    store.collection(u'Places').document("IyTyYJZCfpRDm1nj7iz8YwbSt5p1").collection("slots").document(doc.id).update(
#        {
#            u'availability' : True
#        }
#    )

#datetime.now(pytz.utc)