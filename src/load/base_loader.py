class BaseLoader:
   
   def load(self, data: list[dict], metadata: dict) -> None:
        raise NotImplementedError("The load method must be implemented by subclasses.")
    
