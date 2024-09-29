import os

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, UploadFile
from starlette.responses import JSONResponse

from app.config import settings
from app.containers import Container
from app.schemas.qa import QAQuery
from app.services.qa_service import QAService
from app.worker.tasks import generate_chat_task, update_retrievers_task

router = APIRouter()


@router.get("/upload-file-check")
@inject
async def upload_file_check(
    qa_service: QAService = Depends(Provide[Container.qa_service]),
):
    qa_service.exist_file(settings.UPLOAD_FILE_DIR)


@router.post("/upload")
@inject
async def upload_pdf(
    file: UploadFile = File(...),
    qa_service: QAService = Depends(Provide[Container.qa_service]),
):
    file_path = os.path.join(settings.UPLOAD_FILE_DIR, file.filename)
    qa_service.check_file(file.filename, file_path)
    await qa_service.save_file(file, file_path)

    qa_service.pdf_to_vectorstore(file_path)
    task = update_retrievers_task.delay()
    return JSONResponse(
        {
            "task_id": str(task.id),
            "filename": file.filename,
        }
    )


@router.get("/result/retriever/{task_id}")
@inject
async def check_update_retrievers(
    task_id: str,
):
    task = generate_chat_task.AsyncResult(task_id)
    if task.ready():
        return JSONResponse({"status": "completed"})
    else:
        return JSONResponse({"status": "processing"})


@router.post("/query")
@inject
async def qa_endpoint(
    query: QAQuery,
):
    task = generate_chat_task.delay(query.question)
    return JSONResponse({"task_id": str(task.id)})


@router.get("/result/{task_id}")
@inject
async def get_result(
    task_id: str,
    user_id: str = "user",
    qa_service: QAService = Depends(Provide[Container.qa_service]),
):
    task = generate_chat_task.AsyncResult(task_id)
    if task.ready():
        chat_history = qa_service.get_chat_history(user_id)
        return JSONResponse(
            {
                "status": "completed",
                "result": task.result,
                "chat_history": chat_history,
            }
        )
    else:
        return JSONResponse({"status": "processing"})
