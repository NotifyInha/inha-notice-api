from abc import ABC, abstractmethod
from Univutil.InhaUniv import InhaUniv

class UnivFactory(ABC):
    @abstractmethod
    def get_univutil(self):
        pass

class InhaUnivFactory(UnivFactory):
    def get_univutil(self):
        return InhaUniv()