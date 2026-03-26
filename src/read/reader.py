from abc import ABC, abstractmethod

class Reader(ABC):
    
    @abstractmethod
    def read(self, filepath: str):
        pass

    @abstractmethod
    def get_path(self) -> str:
        pass

