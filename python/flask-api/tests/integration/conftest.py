import pytest
from src.app import create_app,db,User,Role

@pytest.fixture()
def app():
    app = create_app(
        {
            # Aumente estas chaves para pelo menos 32 caracteres
            "SECRET_KEY": "uma_chave_muito_longa_e_segura_com_32_chars", 
            "SQLALCHEMY_DATABASE_URI": "sqlite://", 
            "JWT_SECRET_KEY": "uma_chave_jwt_com_pelo_menos_32_bytes_aqui",
            "JWT_VERIFY_SUB": False,
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def access_token(client):
    role = Role(name = "admin")
    db.session.add(role)
    db.session.commit()

    user = User(username = "john", password = "john1", role_id = role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post("/auth/login", json = {"username": user.username, "password": user.password})
    return response.json["access_token"]

    