from fastapi.testclient import TestClient
from main import app

import uuid as uuidf
from random import randrange


client = TestClient(app)

# Got from stackoverflow https://stackoverflow.com/questions/19989481/how-to-determine-if-a-string-is-a-valid-v4-uuid
def is_valid_uuid(val):
    try:
        uuidf.UUID(str(val))
        return True
    except ValueError:
        return False

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_get_task_that_does_not_exist():
    uuid = uuidf.uuid4()
    response = client.get("/task/" + str(uuid))
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_task():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    assert is_valid_uuid(response.json()) == True

def test_create_task_and_get_task_created():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    assert is_valid_uuid(response.json()) == True

    response = client.get("/task/" + str(response.json()))
    assert response.status_code == 200
    assert response.json() == {'description': 'This is a test task', 'completed': True}

def test_create_task_and_change_task_status_and_check_task_status():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    assert is_valid_uuid(response.json()) == True

    task_uuid = response.json()

    response = client.patch('/task/' + str(task_uuid) , json={"completed": "False"})
    assert response.status_code == 200
    assert response.json() == None

    response = client.get("/task/" + str(task_uuid))
    assert response.status_code == 200
    assert response.json() == {'description': 'This is a test task', 'completed': False}

def test_create_task_and_change_task_description_and_check_description():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    assert is_valid_uuid(response.json()) == True

    task_uuid = response.json()

    response = client.patch('/task/' + str(task_uuid) , json={"description": "Modified description"})
    assert response.status_code == 200
    assert response.json() == None

    response = client.get("/task/" + str(task_uuid))
    assert response.status_code == 200
    assert response.json() == {'description': 'Modified description', 'completed': True}

def test_list_task_randomly_get_one_if_does_not_exists_creates_and_replace_task_checking_status_and_description():
    response = client.get('/task')
    assert response.status_code == 200
    if len(response.json()) < 0:
        random = randrange(len(response.json()) - 1)
        task = list(response.json().items())[random]
        response = client.put('/task/' + task[0], json={'description': 'Replace description', 'completed': True})
        assert response.status_code == 200
        assert response.json() == None

        response = client.get("/task/" + str(task[0]))
        assert response.status_code == 200
        assert response.json() == {'description': 'Replace description', 'completed': True}
    else:
        response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
        assert response.status_code == 200
        assert is_valid_uuid(response.json()) == True

        task_uuid = str(response.json())

        response = client.put('/task/' + task_uuid, json={'description': 'Replace description', 'completed': True})
        assert response.status_code == 200
        assert response.json() == None

        response = client.get("/task/" + task_uuid)
        assert response.status_code == 200
        assert response.json() == {'description': 'Replace description', 'completed': True}

def test_create_task_and_delete_task():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    assert is_valid_uuid(response.json()) == True

    task_uuid = str(response.json())

    response = client.delete('/task/' + task_uuid)
    assert response.status_code == 200
    assert response.json() == None

    assert task_uuid not in client.get('/task')

def 