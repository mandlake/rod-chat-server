from example.utils import myRandom, memberlist


class Account:
    memberlist = memberlist()

    def __init__(self) -> None:
        '''
        [요구사항(RFP)]
        은행이름은 비트은행이다.
        입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
        계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
        예를들면 123-12-123456 이다.
        금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
        '''
        self.creat_account_number()
        print(self.to_string())
        self.deposit()
        print(self.to_string())

    def to_string(self):
        return f'은행 : {self.BANK_NAME}, ' \
               f'입금자: {self.name},' \
               f'계좌번호: {self.account_number},' \
               f'금액: {self.money} 만원'


    def creat_account_number(self) -> object:
        self.BANK_NAME = '비트은행'
        self.name = self.memberlist[myRandom(0, len(memberlist()))]
        self.account_number = f'{myRandom(100, 1000)}-{myRandom(10, 100)}-{myRandom(100000, 1000000)}'
        self.money = myRandom(100, 1000)
        return self

    def deposit(self):
        self.money += myRandom(100, 1000)
        print(f'계좌번호: {self.account_number} 입금액: {self.money} ')

    @staticmethod
    def find_account(ls, account_number) -> object:
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                return i

    @staticmethod
    def del_account(ls, account_number) -> list:
        idx = Account.find_account(ls, account_number)
        del ls[idx]
        return ls

    @staticmethod
    def main():
        ls = []
        while 1 :
            menu = input('0.종료 1.계좌개설 2.계좌목록 3.입금 4.출금 5.계좌해지 6.계좌조회')
            
            if menu == '0':
                break
            elif menu == '1':
                ls.append(Account())
            elif menu == '2':
                for i in ls:
                    print(i.to_string())
            elif menu == '3':
                account_number = input('입금할 계좌번호')
                idx = Account.find_account(ls, account_number)
                ls[idx].deposit()
            elif menu == '4':
                pass
            elif menu == '5':
                account_number = input('해지할 계좌번호')
                ls = Account.del_account(ls, account_number)
            elif menu == '6':
                account_number = input('조회할 계좌번호')
                print(ls[Account.find_account(ls, account_number)].to_string())
            else:
                print('잘못된 메뉴입니다.')
                continue