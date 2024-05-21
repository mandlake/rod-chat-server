from abc import *

class EditorBase(metaclass=ABCMeta):
    @abstractmethod
    def dropNaN(self):
        pass

class PrinterBase(metaclass=ABCMeta):
    @abstractmethod
    def print(self):
        pass
    

class ReaderBase(metaclass=ABCMeta):
    @abstractmethod
    def print(self):
        pass
    
    @abstractmethod
    def xls(self):
        pass
    
    @abstractmethod
    def json(self):
        pass
    
    @abstractmethod
    def gmaps(self):
        pass
    
    
class ScraperBase(metaclass=ABCMeta):
    @abstractmethod
    def driver(self):
        pass