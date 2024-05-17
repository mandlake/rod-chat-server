from example.utils import my100, myRandom


class Calculator:
    def __init__(self):
        print(f'utils.py / myRandom() 을 이용하여 자동 랜덤 계산기를 생성합니다')
        print('(ex) 5 + 4 = 9')
        a = my100()
        b = my100()
        opcodes = ['+', '-', '*', '/']
        opcode = opcodes[myRandom(0, 4)]
        
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