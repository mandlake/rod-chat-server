from example.utils import myRandom


class RPS:
    random = myRandom()

    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')
        rand = self.random(0, 3)
        if(rand == 0):
            print('가위')
        elif(rand == 1):
            print('바위')
        else:
            print('보')