from src.utils import square, requires_roles
import pytest
from http import HTTPStatus



def test_requires_roles(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value = mock_user)
    
    decorated_funtion = requires_roles("admin")(lambda: "Success")

    resultado = decorated_funtion()

    assert resultado == "Success"

     
def test_requires_roles_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"
    
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value = mock_user)

    decorated_funtion = requires_roles("admin")(lambda: "Success")
   
    resultado = decorated_funtion()

    assert resultado == ({"msg": "Not Allowed"}, 403)
