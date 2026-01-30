from .utils import *
from TodoApp.routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_getdb
app.dependency_overrides[get_current_user] = overide_get_current_user

def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'codewithrobytest'
    assert response.json()['email'] == 'codewithrobytest@gmail.com'
    assert response.json()['first_name'] == 'Eric'
    assert response.json()['last_name'] == 'Roby'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(111)-111-1111'

def test_change_password(test_user):
    response = client.put('/user/user/', json={'current_password':'testpassword', 'new_password':'new password'})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid(test_user):
    response = client.put('/user/user/', json={'current_password':'wrong password', 'new_password':'new password'})
    assert response.status_code == 401
    assert response.json() == {'detail':'error on password change'}

def test_change_phone_number(test_user):
    response = client.put('/user/phone_number/(111)-111-1111')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # db = TestsessionLocal()
    # model = db.query(Users).filter(Users.id == 1).first()
    # assert model.phone_number == '(111)-111-1111'