from example.utils import myRandom, memberlist


class Account:
    BANK_NAME = '비트은행'
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
        self.bit_bank()

    def to_string(self):
        return f'은행 : {self.BANK_NAME}, ' \
               f'입금자: {self.name},' \
               f'계좌번호: {self.account_number},' \
               f'금액: {self.money} 만원'


    def create_account_number(self) -> object:
        self.name = self.memberlist[myRandom(0, len(memberlist()))]
        self.account_number = f'{myRandom(100, 1000)}-{myRandom(10, 100)}-{myRandom(100000, 1000000)}'
        self.money = myRandom(100, 1000)
        return self

    def deposit(self):
        deposit_money = myRandom(100, 1000)
        self.money += deposit_money
        print(f'계좌번호: {self.account_number} 입금액: {deposit_money} 남은 금액: {self.money}')
    
    def withdraw(self):
        withdraw_money = myRandom(100, 1000)
        self.money -= withdraw_money
        print(f'계좌번호: {self.account_number} 출금액: {withdraw_money} 남은 금액: {self.money} ')

    @staticmethod
    def find_account(ls, account_number) -> object:
        for i, account in enumerate(ls):
            if account.account_number == account_number:
                return i
        return -1

    @staticmethod
    def del_account(ls, account_number) -> list:
        idx = Account.find_account(ls, account_number)
        if idx != -1:
            del ls[idx]
        return ls

    def bit_bank(self):
        ls = []
        while 1 :
            menu = input('0.종료 1.계좌개설 2.계좌목록 3.입금 4.출금 5.계좌해지 6.계좌조회')
            if menu == '0':
                break
            elif menu == '1':
                acc = self.create_account_number()
                print(f'{self.to_string()} ... 개설되었습니다.')
                ls.append(acc)
            elif menu == '2':
                if not ls:
                    print('계좌 목록이 없습니다.')
                else:
                    for account in ls:
                        print(account.to_string())
            elif menu == '3':
                account_number = input('입금할 계좌번호: ')
                idx = self.find_account(ls, account_number)
                if idx != -1:
                    ls[idx].deposit()
                else:
                    print('계좌를 찾을 수 없습니다.')
            elif menu == '4':
                account_number = input('출금할 계좌번호: ')
                idx = self.find_account(ls, account_number)
                if idx != -1:
                    ls[idx].withdraw()
                else:
                    print('계좌를 찾을 수 없습니다.')
            elif menu == '5':
                account_number = input('해지할 계좌번호: ')
                ls = self.del_account(ls, account_number)
            elif menu == '6':
                account_number = input('조회할 계좌번호: ')
                idx = self.find_account(ls, account_number)
                if idx != -1:
                    print(ls[idx].to_string())
                else:
                    print('계좌를 찾을 수 없습니다.')
            else:
                print('잘못된 메뉴입니다.')
                continue