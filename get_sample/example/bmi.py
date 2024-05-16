from example.utils import Member, myRandom


class BMI():
    member = Member()
    random = myRandom()
    def __init__(self) -> None:
        '''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''
        self.height = self.random(150, 200)
        self.weight = self.random(40, 100)
        
    def get_bmi(self):
        print('BMI 지수를 구하는 계산기입니다')
        print('키와 몸무게를 입력하세요')
        height = self.random(150, 200)
        weight = self.random(40, 100)
        bmi = weight / (height / 100) ** 2
        print(f'당신의 BMI 지수는 {bmi:.2f} 입니다')
        if bmi < 18.5:
            print('저체중입니다')
        elif bmi < 23:
            print('정상입니다')
        elif bmi < 25:
            print('과체중입니다')
        elif bmi < 30:
            print('비만입니다')
        else:
            print('고도비만입니다')
        