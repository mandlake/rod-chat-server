from fastapi import FastAPI
import uvicorn

from example.bit_bank import Account
from example.bmi import BMI
from example.calculator import Calculator
from example.dice import Dice
from example.grade import Grade
from example.leap_year import LeapYear

app = FastAPI()


@app.get("/")
async def root():
    print('=====================')
    BMI()
    print('=====================')
    LeapYear()
    print('=====================')
    Dice()
    print('=====================')
    Grade()
    print('=====================')
    Calculator()
    print('=====================')
    Account()
    print('=====================')
    
    return {"message": "Hello World 3"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)