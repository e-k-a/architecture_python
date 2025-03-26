from schemas import UserDB

fake_db = {
    "user1": {
        "id": "admin",
        "email": "admin@example.com",
        "hashed_password": "secret" 
    }
}

def get_user(email: str):
    for user in fake_db.values():
        if user["email"] == email:
            return UserDB(**user)
    return None

def get_user_by_id(user_id: str):
    user = fake_db.get(user_id)
    return UserDB(**user) if user else None