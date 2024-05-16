from example.utils import myRandom


class Calculator:
    random = myRandom()
    def __init__(self, a, opcode, b):
        print(f'utils.py / myRandom() 을 이용하여 자동 랜덤 계산기를 생성합니다')
        print('(ex) 5 + 4 = 9')
        a = self.random(0, 100)
        b = self.random(0, 100)
        
        if(opcode == '+'):
            answer = a + b
            print(f'{a} + {b} = {answer}')
        elif(opcode == '-'):
            answer = a - b
            print(f'{a} - {b} = {answer}')
        elif(opcode == '*'):
            answer = a * b
            print(f'{a} * {b} = {answer}')
        elif(opcode == '/'):
            answer = a / b
            print(f'{a} / {b} = {answer}')
        else:
            print('잘못된 연산자입니다')
            
        return answer