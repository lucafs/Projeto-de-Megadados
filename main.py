from fastapi import FastAPI, HTTPException
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
        data[str(uuid.uuid4())] = ({
            "description": assignment.description,
            "status": assignment.status
        })
    with open('db.json', 'w') as f:
        json.dump(data, f)

    return "Assignment added to database"
    
@app.get("/assignment/active")
def list_all_active_assignment():
    with open("db.json") as f:
        response = []
        data = json.load(f)
        for assignment in data:
            if data[assignment]['status'] == True:
                data[assignment]['id'] = assignment
                response.append(data[assignment])
        return response

@app.get("/assignment/all")
def list_all_assignment():
    with open("db.json") as f:
        response = []
        data = json.load(f)
        for assignment in data:
            data[assignment]['id'] = assignment
            response.append(data[assignment])
        return response

@app.get("/assignment/{assignment_id}")
def get_assignment(assignment_id: str):
    with open("db.json") as f:
        data = json.load(f)
    try:
        return data[assignment_id]
    except:
        raise HTTPException(status_code=404, detail="ID not found on database")

@app.patch("/assignment/activate/{assignment_id}")
def activate_assigment(assignment_id: str):
    with open("db.json") as f:
        data = json.load(f)
    try:
        if data[assignment_id]['status'] == True:
            return "Assigment already activated"
        else:
            data[assignment_id]['status'] = True
            with open('db.json', 'w') as f:
                json.dump(data, f)  
            return (assignment_id + " activated sucessfully")
    except:
        raise HTTPException(status_code=404, detail="ID not found on database")

@app.patch("/assignment/deactivate/{assignment_id}")
def deactivate_assigment(assignment_id: str):
    with open("db.json") as f:
        data = json.load(f)
    try:
        if data[assignment_id]['status'] == False:
            return "Assigment already deactived"
        else:
            data[assignment_id]['status'] = False
            with open('db.json', 'w') as f:
                json.dump(data, f)  
            return (assignment_id + " deactivated sucessfully")
    except:
        raise HTTPException(status_code=404, detail="ID not found on database")

@app.delete("/assignment/{assignment_id}")
def delete_active_assignment(assignment_id: str):
    with open("db.json") as f:
        data = json.load(f)
    try:
        del data[assignment_id]
        with open('db.json', 'w') as f:
            json.dump(data, f)    
        return assignment_id + " deleted sucessfully"
    except:
        raise HTTPException(status_code=404, detail="ID not found on database")

@app.put("/assignment/{assignment_id}")
def modify_assigment(assignment_id: str, assigment: Assignment = None):
    try:
        with open("db.json") as f:
            data = json.load(f)
        if assigment is None:
            return "You didn't send the information to modify the assignment"
        elif assigment.description is not None:
            if assigment.status is not None:
                data[assignment_id]['description'] = assigment.description
                data[assignment_id]['status'] = assigment.status
            else:
                data[assignment_id]['description'] = assigment.description
        elif assigment.status is not None:
            data[assignment_id]['status'] = assigment.status

    except:
        raise HTTPException(status_code=404, detail="ID not found on database")
    
    with open('db.json', 'w') as f:
        json.dump(data, f)

    return (str(assignment_id) + " modified sucessfully")

