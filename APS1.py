from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import uuid
import json

app = FastAPI()

class Assignment(BaseModel):
    description: str
    status: bool

@app.post("/assignment")
def insert_assignment(assignment: Assignment):
    with open("db.json") as f:
        data = json.load(f)
        _id = str(uuid.uuid4())
        data[_id] = ({
            "description": assignment.description,
            "status": assignment.status
        })
    with open('db.json', 'w') as f:
        json.dump(data, f)

    return _id
    
@app.get("/assignment/active")
def list_all_active_assignment():
    with open("db.json") as f:
        response = []
        data = json.load(f)
        print(data)
        for assignment in data:
            print(assignment)
            if data[assignment]['status'] == True:
                response.append(data[assignment])
        return response



@app.delete("/assignment/delete/{U_id}")
def delete_active_assignment(U_id: str):
    with open("db.json") as f:
        data = json.load(f)

        for assignment in data:
            if assignment == U_id:
                print('entrou')
                del data[assignment]
                with open('db.json', 'w') as f:
                    json.dump(data, f)                
                return "Delete completed"
        return "Id not found"

@app.patch("/assignment/{assignment_id}")
def modify_assigment(assignment_id: str, assigment: Assignment = None):
    try:
        with open("db.json") as f:
            data = json.load(f)
        if assigment is None:
            return "Você não enviou os atributos necessários para modificar a tarefa"
        elif assigment.description is not None:
            if assigment.status is not None:
                data[assignment_id]['description'] = assigment.description
                data[assignment_id]['status'] = assigment.status
            else:
                data[assignment_id]['description'] = assigment.description
        elif assigment.status is not None:
            data[assignment_id]['status'] = assigment.status

    except:
        return "O ID não foi encontrado no banco de dados"
    
    with open('db.json', 'w') as f:
        json.dump(data, f)

    return assignment_id

