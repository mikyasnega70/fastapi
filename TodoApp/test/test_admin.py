from .utils import *
from TodoApp.routers.admin import get_db, get_current_user
from fastapi import status
from TodoApp.models import Todo

app.dependency_overrides[get_db] = override_getdb
app.dependency_overrides[get_current_user] = overide_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id':test_todo.id,
            'title':'test todo',
            'description':'test todo description',
            'priority':3,
            'complete':False,
            'owner_id':1,
        }
    ]

def test_admin_delete_todo(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == 204

    db = TestsessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model is None

def test_admin_delete_todo_notfound():
    response = client.delete('/admin/todo/2')
    assert response.status_code == 404
    assert response.json() == {'detail':'todo not found'}

