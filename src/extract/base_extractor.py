class BaseExtractor:
    
    def extract(self) -> tuple[list[dict], dict]:
        raise NotImplementedError("The extract method must be implemented by subclasses.")
    
