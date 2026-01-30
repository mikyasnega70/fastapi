from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..models import Todo
from ..database import session_local
from typing import Annotated, Optional
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Todorequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)
    complete: bool 

templates = Jinja2Templates(directory='TodoApp/templates')

def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

## pages ##
@router.get('/todo-page')
async def render_todos_page(request:Request, db:db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todo).filter(Todo.owner_id == user.get('id')).all()
        return templates.TemplateResponse('todo.html', {'request':request, 'todos':todos, 'user':user})
    except:
        return redirect_to_login()
    
@router.get('/add-todo-page')
async def render_add_todo(request:Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        
        return templates.TemplateResponse('add-todo.html', {'request':request, 'user':user})
    except:
        return redirect_to_login()

@router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo(request:Request, todo_id:int, db:db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()
        
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        return templates.TemplateResponse('edit-todo.html', {'request':request, 'todo':todo, 'user':user})
    except:
        return redirect_to_login()

## endpoints ##
@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency ,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()

@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency ,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='todo not found')

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency ,db: db_dependency, todorequest: Todorequest):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    todo_model = Todo(**todorequest.model_dump(), owner_id= user.get('id'))
    
    db.add(todo_model)
    db.commit()

@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency ,db: db_dependency, todorequest: Todorequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    
    todo_model.title = todorequest.title
    todo_model.description = todorequest.description
    todo_model.priority = todorequest.priority
    todo_model.complete = todorequest.complete

    db.add(todo_model)
    db.commit()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency ,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    
    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    
    db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user.get('id')).delete()
    db.commit()
