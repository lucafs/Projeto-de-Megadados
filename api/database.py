import uuid
from api.models import Assignment

class DBSession:
    tasks = {}
    def __init__(self):
        self.tasks = DBSession.tasks
    
    def read_assignments(self, completed: bool):
        return {
            uuid_: item
            for uuid_, item in self.tasks.items()
            if item.completed == completed
        }

    def create_assignment(self, item: Assignment):
        uuid_ = uuid.uuid4()
        self.tasks[uuid_] = item
        return uuid_ 
    
    def read_assignment(self, uuid_: uuid.UUID):
        return self.tasks[uuid_]
    
    def replace_assignment(self, uuid_: uuid.UUID, item: Assignment):
        if uuid_ in self.tasks:
            self.tasks[uuid_] = item
        else:
            return "Task not found"
            
    def alter_assignment(self, uuid_: uuid.UUID, item: Assignment):
        update_data = item.dict(exclude_unset=True)
        self.tasks[uuid_] = self.tasks[uuid_].copy(update=update_data)
    
    def remove_assignment(self, uuid_: uuid.UUID):
        if uuid_ in self.tasks:
            del self.tasks[uuid_]
            return "Task removida com sucesso"
        return "Task not found"

def get_db():
    return DBSession()
