import uuid as uuidf
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
from api.models import Assignment
from api.database import get_db, DBSession

app = APIRouter()

@app.get(
    '',
    summary='Reads task list',
    description='Reads the whole task list.',
    response_model=Dict[uuidf.UUID, Assignment],
)
async def read_assignments(completed: bool = None, dB: DBSession = Depends(get_db)):
    return dB.read_assignments(completed)


@app.post(
    '',
    summary='Creates a new task',
    description='Creates a new task and returns its UUID.',
    response_model=uuidf.UUID,
)
async def create_assignment(item: Assignment, dB: DBSession = Depends(get_db)):
    return dB.create_assignment(item)


@app.get(
    '/{uuid_}',
    summary='Reads task',
    description='Reads task from UUID.',
    response_model=Assignment,
)
async def read_assignment(uuid_: uuidf.UUID, db: DBSession = Depends(get_db)):
    try:
        return db.read_assignment(uuid_)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@app.put(
    '/{uuid_}',
    summary='Replaces a task',
    description='Replaces a task identified by its UUID.',
)
async def replace_assignment(uuid_: uuidf.UUID, item: Assignment, dB: DBSession = Depends(get_db)):
    try:
        if dB.replace_assignment(uuid_, item) == "UUID not found":
            raise HTTPException(status_code=404,detail='UUID not found')
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@app.patch(
    '/{uuid_}',
    summary='Alters task',
    description='Alters a task identified by its UUID',
)
async def alter_assignment(uuid_: uuidf.UUID, item: Assignment, dB: DBSession = Depends(get_db)):
    try:
        dB.alter_assignment(uuid_, item)
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception


@app.delete(
    '/{uuid_}',
    summary='Deletes task',
    description='Deletes a task identified by its UUID',
)
async def remove_assignment(uuid_: uuidf.UUID, dB: DBSession = Depends(get_db)):
    try:
        if dB.remove_assignment(uuid_) == "Task not found":
            raise HTTPException(status_code=404,detail='Task not found')
    except KeyError as exception:
        raise HTTPException(
            status_code=404,
            detail='Task not found',
        ) from exception 