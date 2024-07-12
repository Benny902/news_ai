from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import ReturnDocument

def create_user(db, username, password, **additional_fields):
    hashed_password = generate_password_hash(password)
    user = {
        'username': username,
        'password': hashed_password,
    }
    user.update(additional_fields)
    result = db.users.insert_one(user)
    return result.inserted_id

def find_user_by_username(db, username):
    return db.users.find_one({'username': username})

def update_user_profile(db, user_id, updates):
    result = db.users.update_one({'_id': user_id}, {'$set': updates})
    return result

def check_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)
