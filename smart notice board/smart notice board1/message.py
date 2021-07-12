# Import database module.
from firebase_admin import db
from firebase import firebase
firebase = firebase.FirebaseApplication('https://notice-64ce2.firebaseio.com/', None)

# Get a database reference to our blog.

result = firebase.patch('/notice-64ce2/notic/', {'Message': 'someday'})
print(result)

'''
ref = db.reference('/notice-64ce2')
users_ref = ref.child('/notice-64ce2')
users_ref.set('/notice-64ce2', {'Message':'notice' })

users_ref.set({
    'alanisawesome': {
        'date_of_birth': 'June 23, 1912',
        'full_name': 'Alan Turing'
    },
    'gracehop': {
        'date_of_birth': 'December 9, 1906',
        'full_name': 'Grace Hopper'
    }
})
'''
