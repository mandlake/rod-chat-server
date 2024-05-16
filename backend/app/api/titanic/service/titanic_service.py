from app.api.titanic.model.titanic_model import TitanicModel

class TitanicService:
    model = TitanicModel()
    
    def process(self):
        print('프로세스 시작')
        this = self.model
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        this.train = self.new_titanic('train.csv')
        this.test = self.new_titanic('test.csv')
        
        self.df_info(this)
        
        this = self.title_nominal(this)
        
        self.df_info(this)
        
        this = self.drop_feature(this, 'Name', 'SlbSp', 'Parch', 'Cabin', 'Ticket')
        this = self.pclass_ordinal(this)
        this = self.sex_nominal(this)
        this = self.age_ratio(this)
        this = self.fare_ratio(this)
        this = self.embarked_nominal(this)
        
        this.id = this.test['PassengerId']                          # 승객ID
        
        self.df_info(this)
        
        this = self.create_train(this)
    
    @staticmethod
    def df_info(this):
        [print(i.head()) for i in [this.train, this.test]]
        
    @staticmethod
    def create_train(this) -> str:
        return this.train.drop('Survived', axis=1)
    
    @staticmethod
    def create_label(this) -> str:
        return this.train['Survived']
    
    @staticmethod
    def title_nominal(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i.Name.str.extract('([A-Za-z]+)\.', expand=False)
        for i in combine:
            i['Title'] = i['Title'].replace(['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona'], 'Rare')
            i['Title'] = i['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            i['Title'] = i['Title'].replace('Mlle', 'Miss')
            i['Title'] = i['Title'].replace('Ms', 'Miss')
            i['Title'] = i['Title'].replace('Mme', 'Mrs')
        return this
    
    @staticmethod
    def extract_title_from_name(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i['Name'].str.extract('([A-Za-z]+)\.', expand=False)
        return this
    
    @staticmethod
    def sex_nominal(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Sex'] = i['Sex'].map({})
        return this
    
    @staticmethod
    def age_ratio(this) -> object:
        return this
    
    @staticmethod
    def fare_ratio(this) -> object:
        return this
    
    @staticmethod
    def embarked_nominal(this) -> object:
        return this
  