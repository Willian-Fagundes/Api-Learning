from src.app import User, db, Role
from sqlalchemy import func

def test_get_user_success(client):
    role = Role(name = "admin")
    db.session.add(role)
    db.session.commit()

    user = User(username = "john", password = "jane1", role_id = role.id)
    db.session.add(user)
    db.session.commit()
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json == {"id": user.id,"username" : user.username,}

def test_get_user_404(client):
    role = Role(name = "admin")
    db.session.add(role)
    db.session.commit()

    user_id =1 
   
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_create_user(client, access_token):
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username" : "jane", "password": "jane1", "role_id" : role_id}

    response = client.post("/users/", json = payload, headers = {"Authorization" : f"Bearer {access_token}"})

    assert response.status_code == 201
    assert response.json == ({"message" : "user created"})
    
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2


def test_list_users(client, access_token):
    user = db.session.execute(db.select(User).where(User.username == "john")).scalar()
    response = client.get(f"/users/", headers = {"Authorization" : f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json == ({"user" : [
            {
            "id": user.id, 
            "username" : user.username,
            "role" : {
                "id" : user.role.id,
                "name" : user.role.name
            }}]})