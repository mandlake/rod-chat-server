from example.utils import myRandom


class Dice:
    random = myRandom()

    def __init__(self, sides=6):
        print(f'utils.py myRandom() 를 이용하여 주사위 객체를 생성합니다')
        self.random(1, sides + 1)
        