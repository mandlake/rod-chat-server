from fastapi import APIRouter
from pydantic import BaseModel
from app.api.titanic.service.titanic_service import TitanicService

router = APIRouter()
service = TitanicService()

class Request(BaseModel):
    question: str
    
class Response(BaseModel):
    answer: str

@router.post("/titanic")
async def titanic(req: Request):
    print("타이타닉 딕셔너리 내용")
    service.preprocess()
    print(req)
    return Response(answer="생존자는 100명입니다.")

