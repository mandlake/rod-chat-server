
from app.api.titanic.model.titanic_model import TitanicModel


class TitanicService:
    model = TitanicModel()
    
    def preprocess(self):
        print('프로세스 시작')
        this = self.model
        this.preprocess('train.csv', 'test.csv')
    
    def modeling(self):
        print('모델링 시작')
        this = self.model
        result = this.learning(this, 'train.csv', 'test.csv')
        print(f'모델링 결과: {result}')
        
        return result
    
    def learning(self):
        print('러닝 시작')
        this = self.model
        result = self.modeling()
        print(f'결정트리를 활용한 검증 정확도: {this}')
        print(f'랜덤포레스트를 활용한 검증 정확도: {this}')
        print(f'나이브베이즈를 활용한 검증 정확도: {this}')
        print(f'KNN을 활용한 검증 정확도: {this}')
        print(f'SVM을 활용한 검증 정확도: {this}')
        
        return this
    
    def postprocessing(self):
        print('후처리 시작')
        this = self.model
        print(f'후처리 결과: {this}')
        
        return this
    
    def submit(self):
        print('제출 시작')
        this = self.model
        print(f'제출 결과: {this}')
        
        return this