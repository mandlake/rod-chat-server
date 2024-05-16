from fastapi import FastAPI
from langchain.chat_models.openai import ChatOpenAI
import os
from dotenv import load_dotenv
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from pydantic import BaseModel

from starlette.middleware.cors import CORSMiddleware
from app.main_router import router as m_router

class Request(BaseModel):
    question: str

class Response(BaseModel):
    answer: str

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(m_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chatting(req:Request):
    print('딕셔너리 내용')
    print(req)
 
    chat = ChatOpenAI(
        openai_api_key=os.environ["api_key"],
        temperature=0.1,                    # 창의성 (0.0 ~ 2.0) 
        max_tokens=2048,                    # 최대 토큰수
        model_name='gpt-3.5-turbo-0613',    # 모델명
        )

    print(f'{chat.predict(req.question)}')

    return Response(answer=chat.predict(req.question))

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
