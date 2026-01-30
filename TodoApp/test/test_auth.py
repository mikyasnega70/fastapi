from .utils import *
from TodoApp.routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user, bycrpt_context
from fastapi import status, HTTPException
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_getdb

def test_authenticate_user(test_user):
    db = TestsessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existance_user = authenticate_user('wrongusername', 'testpassword', db)
    assert non_existance_user is False

    wrong_password = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password is False

def test_create_token():
    username = 'testuser'
    id = 1
    role = 'user'
    expiresdelta = timedelta(days=1)

    token = create_access_token(username, id, role, expiresdelta)

    decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decode_token['sub'] == username
    assert decode_token['id'] == id
    assert decode_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub':'testuser', 'id':1, 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username':'testuser', 'id':1, 'user_role':'admin'}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)
    
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'can not validate user'

def test_create_user(test_user):
    request_test = {
        'email':'testuser@gmail.com',
        'username':'testuser',
        'first_name':'Test',
        'last_name':'User',
        'password':'testpassword',
        'role':'user',
        'phone_number':'(222)-222-2222'
    }
    response = client.post('/auth', json=request_test)
    response.status_code == status.HTTP_201_CREATED

    db = TestsessionLocal()
    model = db.query(Users).filter(Users.id == 2).first()
    assert model.email == request_test.get('email')
    assert model.username == request_test.get('username')
    
def test_login_access(test_user):
    response = client.post('/auth/token', data={"username":"codewithrobytest", "password":"testpassword"})
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'

def test_login_access_invalid(test_user):
    response = client.post('/auth/token', data={'username':'wronguser', 'password':'wrongpassword'})
    assert response.status_code == 401
    assert response.json() == {'detail':'can not validate user'}
