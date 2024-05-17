from example.utils import my100


class Grade:

    def __init__(self) -> None:
        # 아래 주석된 부분을 완성합니다.
        kor = my100()
        eng = my100()
        math = my100()
        print(f'국어: {kor}, 영어: {eng}, 수학: {math}')
        
        sum = self.sum(kor, eng, math)
        avg = self.avg(kor, eng, math)
        grade = self.grade(kor, eng, math)
        print(f'총점: {sum}, 평균: {avg}, 학점: {grade}')
        
        passChk = self.passChk(kor, eng, math)
        print(f'결과: {passChk}')
    
    def sum(self, kor, eng, math):
        return kor + eng + math
    
    def avg(self, kor, eng, math):
        sum = self.sum(kor, eng, math)
        return sum / 3
    
    def grade(self, kor, eng, math):
        avg = self.avg(kor, eng, math)
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
        
    def passChk(self, kor, eng, math):
        grade = self.grade(kor, eng, math)
        if grade != 'F':
            return '합격'
        else:
            return '불합격'