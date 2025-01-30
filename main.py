from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from deep_medical.routes.task_manager import task_router
from deep_medical.exceptions import (
    AppException,
    InvalidDataException,
    NotFoundException
)

app = FastAPI(
    title="Task Manager API",
    version="1.0",
    summary="The APIs to serve the task manager based on the deep medical specification"
)

app.include_router(task_router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    if isinstance(exc, NotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, InvalidDataException):
        status_code = status.HTTP_400_BAD_REQUEST
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse({"detail": str(exc)}, status_code=status_code)