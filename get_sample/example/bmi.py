from example.utils import myRandom, Member


class BMI():
    member = Member()
    def __init__(self) -> None:
        '''utils.py / Members(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''
        height = self.member.height
        weight = self.member.weight
        
        print('BMI 지수를 구하는 계산기입니다')
        height = myRandom(150, 200)
        weight = myRandom(40, 100)
        print(f'당신의 키는 {height}cm 이고 몸무게는 {weight}kg 입니다')
        
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