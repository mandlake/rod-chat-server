from example.utils import myRandom


class Grade:

    def __init__(self) -> None:
        # 아래 주석된 부분을 완성합니다.
        kor = myRandom(0,100)
        eng = myRandom(0, 100)
        math = myRandom(0, 100)
        sum = self.sum(kor, eng, math)
        avg = self.agv(kor, eng, math)
        grade = self.getGrade()
        passChk = self.passChk()
        return [sum, avg, grade, passChk]
    
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
        if kor >= 60 and eng >= 60 and math >= 60:
            return '합격'
        else:
            return '불합격'