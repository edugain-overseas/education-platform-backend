import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.group_chat_router import router as group_chat_router
from app.routers.group_router import router as group_router
from app.routers.lecture_router import router as lecture_router
from app.routers.lesson_router import router as lesson_router
from app.routers.module_router import router as module_router
from app.routers.specialization_router import router as specialization_router
from app.routers.student_router import router as student_router
from app.routers.subject_router import router as subject_router
from app.routers.user_router import router as user_router


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(user_router, prefix='/api/v1', tags=['User'])
app.include_router(specialization_router, prefix='/api/v1', tags=['Specialization'])
app.include_router(group_router, prefix='/api/v1', tags=['Group'])
app.include_router(subject_router, prefix='/api/v1', tags=['Subject'])
app.include_router(module_router, prefix='/api/v1', tags=['Module'])
app.include_router(lesson_router, prefix='/api/v1', tags=['Lesson'])
app.include_router(student_router, prefix='/api/v1', tags=['Student'])
app.include_router(group_chat_router, prefix='/api/v1', tags=['GroupChat'])
app.include_router(lecture_router, prefix='/api/v1', tags=['Lecture'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Server working"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
