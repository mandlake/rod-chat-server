from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Request(BaseModel):
    question: str
    
class Response(BaseModel):
    answer: str

@router.post("/titanic")
async def titanic(req: Request):
    print("타이타닉 딕셔너리 내용")
    print(req)
    return Response(answer="titanic predict")

