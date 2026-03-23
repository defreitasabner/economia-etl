from abc import ABC, abstractmethod

class BaseLoader(ABC):
   
   @abstractmethod
   def load(self, data: list[dict], metadata: dict) -> None:
      pass
    
