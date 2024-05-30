from abc import ABC, abstractmethod

class UnivUtilFunction(ABC):
    @abstractmethod
    def deserializesource(self, data):
        pass