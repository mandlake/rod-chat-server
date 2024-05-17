from example.utils import myRandom


class Dice:

    def __init__(self, sides=6):
        print(f'utils.py myRandom() 를 이용하여 주사위 객체를 생성합니다')
        dice = myRandom(1, sides + 1)
        print(f'주사위를 굴려 {dice}가 나왔습니다')
        