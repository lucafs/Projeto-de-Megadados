from fastapi import FastAPI
from api.routers import assignment

tags_metadata = [
    {
        "name": "task",
        "description": "Operations related to tasks.",
    },
]

app = FastAPI(
    title="Task list",
    description="Task-list project for the **Megadados** course",
    openapi_tags=tags_metadata,
)

app.include_router(
    assignment.app,
    prefix="/task",
    tags=["task"],
)
