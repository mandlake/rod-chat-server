from example.utils import myRandom


class LeapYear:
    random = myRandom()

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 윤년계산기 객체를 생성합니다')
        print ('(ex) 2020년은 윤년입니다. 단 컴프리헨션을 사용합니다')
        num = self.random(0, 3000)
        print(f'{num}년은 윤년입니다' if (num % 4 == 0 and num % 100 != 0) or num % 400 == 0 else f'{num}년은 윤년이 아닙니다')