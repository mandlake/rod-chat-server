import numpy as np
import pandas as pd
import icecream as ic
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from app.api.domain.data_sets import DataSets
from app.api.domain.models import models

class TitanicModel(object) :
    model = models()
    dataset = DataSets()
    
    def preprocess(self, train_fname, test_fname) -> object:
        this = self.dataset
        that = self.model
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        # 데이터셋은 Train, Test, Validation 3종류로 분류
        this.train = that.new_dataframe_no_index(train_fname)
        print(f'트레인셋: {this.train.columns}')
        this.test = that.new_dataframe_no_index(test_fname)
        print(f'테스트셋: {this.test.columns}')
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        this = self.drop_feature(this, 'Survived')
        
        this = self.drop_feature(this, 'SlbSp', 'Parch', 'Cabin', 'Ticket')
        
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate_title(this)
        this = self.name_nominal(this, title_mapping)
        this = self.drop_feature(this, 'Name')
        
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')
        
        this = self.pclass_ordinal(this)
        
        this = self.age_ratio(this)
        this = self.drop_feature(this, 'Age')
        
        this = self.fare_ratio(this)
        this = self.drop_feature(this, 'Fare')
        
        this = self.embarked_nominal(this)
        self.df_info(this)
        
        return this
    
    def df_info(self, this):
        print('='*50)
        print(f'1. Train 의 type 은 {type(this.train)} 이다.')
        print(f'2. Train 의 column 은 {this.train.columns} 이다.')
        print(f'3. Train 의 상위 1개의 데이터는 {this.train.head()} 이다.')
        print(f'4. Train 의 null 의 갯수는 {this.train.isnull().sum()} 이다.')
        print(f'5. Test 의 type 은 {type(this.test)} 이다.')
        print(f'6. Test 의 column 은 {this.test.columns} 이다.')
        print(f'7. Test 의 상위 1개의 데이터는 {this.test.head()} 이다.')
        print(f'8. Test 의 null 의 갯수는 {this.test.isnull().sum()} 이다.')
        print('='*50)
        
    
    @staticmethod
    def drop_feature(this, *feature) -> object:
        [(i.drop(j, axis=1, inplace=True)) for j in feature for i in [this.train, this.test] if j in i.columns]
        
        return this
    
    @staticmethod
    def extract_title_from_name(this) -> pd.DataFrame:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i.Name.str.extract('([A-Za-z]+)\.', expand=False)
        return this
    
    @staticmethod
    def remove_duplicate_title(this) -> pd.DataFrame:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        
        print(a)
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        
        title_mapping = {'Mr': 1, 'Ms': 2, 'Mrs': 3, 'Master': 4, 'Royal': 5, 'Rare': 6}
        
        return title_mapping
    
    @staticmethod
    def name_nominal(this, title_mapping) -> pd.DataFrame:
        for i in [this.train, this.test]:
            i['Title'] = i['Title'].replace(['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme'], 'Rare')
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            i['Title'] = i['Title'].replace(['Mlle'], 'Mr')
            i['Title'] = i['Title'].replace(['Miss'], 'Ms')
            i['Title'] = i['Title'].fillna(-0.5)
            i['Title'] = i['Title'].map(title_mapping)
        
        return this
    
    @staticmethod
    def sex_nominal(this) -> pd.DataFrame:
        for i in [this.train, this.test]:
            i['Sex'] = i['Sex'].fillna(-0.5)
            i['Gender'] = i['Sex'].map({'male': 0, 'female': 1})
        
        return this
    
    @staticmethod
    def pclass_ordinal(this) -> pd.DataFrame:
        for i in [this.train, this.test]:
            i['Pclass'] = i['Pclass'].fillna(-0.5)
        
        return this

    @staticmethod
    def age_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        age_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4,
                       'Young Adult': 5, 'Adult': 6, 'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior']
        
        for i in [train, test]:
            i['Age'] = pd.cut(i['Age'], bins=bins, labels=labels)
            i['AgeGroup'] = i['Age'].map(age_mapping)
        
        return this
    
    @staticmethod
    def fare_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        fare_mapping = {'Unknown': 0, '1_quartile': 1, '2_quartile': 2, '3_quartile': 3, '4_quartile': 4}
        train['Fare'] = train['Fare'].fillna(-0.5)
        test['Fare'] = test['Fare'].fillna(-0.5)
        bins = [-1, 0, 8, 15, 31, np.inf]
        labels = ['Unknown', '1_quartile', '2_quartile', '3_quartile', '4_quartile']
        
        for i in [train, test]:
            i['Fare'] = pd.cut(i['Fare'], bins=bins, labels=labels)
            i['FareBand'] = i['Fare'].map(fare_mapping)
        
        return this
    
    @staticmethod
    def embarked_nominal(this) -> pd.DataFrame:
        this.train['Embarked'] = this.train['Embarked'].fillna('S')
        this.test['Embarked'] = this.test['Embarked'].fillna('S')
        this.train['Embarked'] = this.train['Embarked'].map({'S':1, 'C':2, 'Q':3})
        this.test['Embarked'] = this.test['Embarked'].map({'S':1, 'C':2, 'Q':3})
        return this
    
    @staticmethod
    def create_k_fold() -> object:
        return KFold(n_splits=10, shuffle=True, random_state=0)
    
    @staticmethod
    def get_accurancy(this, k_fold) -> object:
        score = cross_val_score(RandomForestClassifier(), this.train, this.label, cv=k_fold, n_jobs=-1, scoring='accuracy')
        return score

    @staticmethod
    def learning(self, train_fname, test_fname) -> pd.DataFrame:
        this = self.preprocess(train_fname, test_fname)
        print(f'학습 시작')
        k_fold = self.create_k_fold()
        accuracy = self.get_accurancy(this, k_fold)
        print(f'사이킷런 알고리즘 정확도 : {accuracy}') 
        return accuracy