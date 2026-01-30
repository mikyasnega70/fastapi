from TodoApp.routers.todos import get_db, get_current_user
from fastapi import status
from TodoApp.models import Todo
from .utils import *


app.dependency_overrides[get_db] = override_getdb
app.dependency_overrides[get_current_user] = overide_get_current_user



def test_read_all_authenticate(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id':test_todo.id,
        'title':'test todo',
        'description':'test todo description',
        'priority':3,
        'complete':False,
        'owner_id':1,
    }]

def test_read_one_authenticate(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id':test_todo.id,
        'title':'test todo',
        'description':'test todo description',
        'priority':3,
        'complete':False,
        'owner_id':1,
    }

def test_read_one_authenticate_not_found(): 
    response = client.get('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail':'todo not found'}



def test_create_todo(test_todo):
    request_test = {
    'title':'new todo',
    'description':'new todo description',
    'priority':2,
    'complete':False,
  }
    
    response = client.post('/todos/todo', json=request_test)
    assert response.status_code == 201

    db = TestsessionLocal()
    model = db.query(Todo).filter(Todo.id == 2).first()
    assert model.complete == request_test.get('complete')
    assert model.description == request_test.get('description')
    assert model.priority == request_test.get('priority')
    assert model.title == request_test.get('title')

def test_update_todo(test_todo):
    request_test = {
        'title':'updated todo',
        'description':'test todo description',
        'priority':3,
        'complete':False,
    }

    response = client.put('/todos/todo/1/', json=request_test)
    assert response.status_code == 204

    db = TestsessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model.title == 'updated todo'

def test_update_todo_not_found(test_todo):
    request_test = {
        'title':'updated todo',
        'description':'test todo description',
        'priority':3,
        'complete':False,
    }

    response = client.put('/todos/todo/999/', json=request_test)
    assert response.status_code == 404
    assert response.json() == {'detail': 'todo not found'}

def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db = TestsessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model is None

def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'todo not found'}

