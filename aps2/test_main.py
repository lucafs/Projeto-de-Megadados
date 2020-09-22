from fastapi.testclient import TestClient
from main import app

import uuid as uuidf

client = TestClient(app)
uuid = uuidf.uuid4()

# Got from stackoverflow https://stackoverflow.com/questions/19989481/how-to-determine-if-a-string-is-a-valid-v4-uuid
def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False

def test_get_task_that_does_not_exist():
    response = client.get("/task/" + str(uuid))
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_task():
    response = client.post('/task', json={"completed": "True", "description": "This is a test task"})
    assert response.status_code == 200
    if (is_valid_uuid(response.json()))

