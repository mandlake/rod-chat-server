class Contract:
    def __init__(self):
        self.name = ''
        self.phone = ''
        
    def add_contract(self, members) -> object:
        self.name = input('이름 입력: ').title()
        self.phone = input('전화번호 입력: ')
        members[self.name] = self.phone
        print('----------')
        print(f'*****{self.name} 입력 완료*****')
        print(f'{self.name}:', self.phone)
        print('----------')
        return members
    
    def find_contract(self, members) -> object:
        self.name = input('검색할 이름 입력: ').title()
        self.phone = members.get(self.name, '존재하지 않습니다.')
        print('----------')
        print(f'{self.name}:', self.phone)
        print('----------')
        return members
    
    def update_contract(self, members) -> object:
        self.name = input('수정할 이름 입력: ').title()
        if(self.name not in members.keys()):
            print('----------')
            print(f'{self.name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            self.phone = input('새로운 전화번호 입력: ')
            members[self.name] = self.phone
            print('----------')
            print(f'*****{self.name} 수정 완료*****')
            print(f'{self.name}:', self.phone)
            print('----------')
        return members
    
    def delete_contract(self, members) -> object:
        self.name = input('삭제할 이름 입력: ').title()
        if(self.name not in members.keys()):
            print('----------')
            print(f'{self.name} 회원은 존재하지 않습니다.')
            print('----------')
        else:
            ask = input(f"{self.name} 회원을 정말로 삭제할까요?(y): ").lower()
            if ask == 'y':
                del members[self.name]
                print('----------')
                print(f"*****{self.name} 삭제 완료*****")
                print('----------')
            else:
                print('----------')
                print(f'{self.name} 회원을 삭제하지 않았습니다.')
                print('----------')
        return members
    
    def find_all(self, members) -> object:
        print('----------')
        for k, v in members.items():
            print(f'{k}: {v}')
        print('----------')
        return members
    
    def exit_program(self):
        print('----------')
        print('프로그램을 종료합니다.')
        print('----------')

if __name__ == "__main__":
    this = Contract()
    members = {}
    while True:
        menu = input('회원정보 추가(a), 검색(f), 수정(u), 삭제(d), 목록(s), 종료(x): ')
        if menu=='a':
            members = this.add_contract(members)

        elif menu=='f':
            members = this.find_contract(members)

        elif menu=='u':
            members = this.update_contract(members)

        elif menu=='d':
            members = this.delete_contract(members)

        elif menu=='s':
            members = this.find_all(members)

        elif menu=='x':
            this.exit_program()
            break # loop 끝내기