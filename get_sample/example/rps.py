from example.utils import myRandom


class RPS:
    def __init__(self) -> None:
        print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')
        rps = ['가위', '바위', '보']
        rand = myRandom(0, 3)
        
        print(f'가위바위보 중 하나를 선택하세요')
        user = input('0.가위 1.바위 2.보')
        
        print(f'사용자: {rps[int(user)]} vs 컴퓨터: {rps[rand]}')
        
        if user == '0' and rand == 1 or user == '1' and rand == 2 or user == '2' and rand == 0:
            print('컴퓨터 승')
        elif user == '0' and rand == 2 or user == '1' and rand == 0 or user == '2' and rand == 1:
            print('사용자 승')
        else:
            print('비김')
