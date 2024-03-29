import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers.group_chat_router import router as group_chat_router
from app.routers.group_router import router as group_router
from app.routers.lecture_router import router as lecture_router
from app.routers.lesson_router import router as lesson_router
from app.routers.module_router import router as module_router
from app.routers.specialization_router import router as specialization_router
from app.routers.student_router import router as student_router
from app.routers.student_test_router import router as student_test_router
from app.routers.subject_chat_router import router as subject_chat_router
from app.routers.subject_instruction_router import router as subject_instruction_router
from app.routers.subject_router import router as subject_router
from app.routers.teacher_router import router as teacher_router
from app.routers.test_lesson_router import router as test_router
from app.routers.user_router import router as user_router
from app.setting import API_PREFIX

# from redis import asyncio as aioredis
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend


app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(user_router, prefix=API_PREFIX, tags=['User'])
app.include_router(student_router, prefix=API_PREFIX, tags=['Student'])
app.include_router(student_test_router, prefix=API_PREFIX, tags=['Student Test'])
app.include_router(teacher_router, prefix=API_PREFIX, tags=['Teacher'])

app.include_router(specialization_router, prefix=API_PREFIX, tags=['Specialization'])
app.include_router(group_router, prefix=API_PREFIX, tags=['Group'])
app.include_router(subject_router, prefix=API_PREFIX, tags=['Subject'])
app.include_router(subject_instruction_router, prefix=API_PREFIX, tags=['Subject Instruction'])
app.include_router(module_router, prefix=API_PREFIX, tags=['Module'])
app.include_router(lesson_router, prefix=API_PREFIX, tags=['Lesson'])
app.include_router(lecture_router, prefix=API_PREFIX, tags=['Lecture'])
app.include_router(test_router, prefix=API_PREFIX, tags=['Test'])

app.include_router(group_chat_router, prefix=API_PREFIX, tags=['GroupChat'])
app.include_router(subject_chat_router, prefix=API_PREFIX, tags=['SubjectChat'])


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


@app.get("/get_image")
async def get_image(file_path: str):
    return FileResponse(file_path)


# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis=redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
