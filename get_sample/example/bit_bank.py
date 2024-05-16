from example.utils import memberlist, myRandom


class Account:
    random = myRandom()
    member = memberlist()

    def __init__(self) -> None:
        '''
        [요구사항(RFP)]
        은행이름은 비트은행이다.
        입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다.
        계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다.
        예를들면 123-12-123456 이다.
        금액은 100 ~ 999 사이로 랜덤하게 입금된다. (단위는 만단위로 암묵적으로 판단한다)
        '''
        self.BANK_NAME = '비트은행'
        self.name = ''
        self.account_number = ''
        self.money = 0

    def to_string(self):
        self.name = self.member[self.random(0, len(self.member))]
        self.account_number = self.creat_account_number()
        return f'은행 : {self.BANK_NAME}, ' \
               f'입금자: {self.name},' \
               f'계좌번호: {self.account_number},' \
               f'금액: {self.money} 만원'


    def creat_account_number(self):
        return f'{self.random(100, 1000)}-{self.random(10, 100)}-{self.random(100000, 1000000)}'

    def deposit(self):
        self.money += self.random(100, 1000)
        print(f'입금액: {self.money} 만원')

    @staticmethod
    def find_account(ls, account_number):
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                return i

    @staticmethod
    def del_account(ls, account_number):
        idx = Account.find_account(ls, account_number)
        ls.pop(idx)

    @staticmethod
    def main():
        ls = []
        while 1 :
            menu = input('0.종료 1.계좌개설 2.계좌목록 3.입금 4.출금 5.계좌해지 6.계좌조회')
            if menu == '0':
                break
            if menu == '1':
                acc = Account(None, None, None)
                print(f'{acc.to_string()} ... 개설되었습니다.')
                ls.append(acc)
            elif menu == '2':
                a = '\n'.join(i.to_string() for i in ls)
                print(a)
            elif menu == '3':
                account_number = input('입금할 계좌번호')
                deposit = int(input('입금액')) # string -> int
                # 힌트 a.money + deposit
                for i, j in enumerate(ls):
                    if j.account_number == account_number:
                        ls[i].money += deposit
            elif menu == '4':
                account_number = input('출금할 계좌번호')
                money = input('출금액')
                # 추가코드 완성
                ls[Account.find_account(ls, account_number)].money -= int(money)
            elif menu == '5':
                Account.del_account(ls, input('탈퇴할 계좌번호'))
            elif menu == '6':
                print(Account.find_account(ls, input('검색할 계좌번호') ))
            else:
                print('Wrong Number.. Try Again')
                continue