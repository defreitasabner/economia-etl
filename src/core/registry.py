from abc import ABC
import importlib
import pkgutil


class Registry(ABC):

    _registry = {}

    @classmethod
    def auto_discover(cls):
        base_package = cls.__module__.rsplit(".", 1)[0]
        package = importlib.import_module(base_package)

        for module_info in pkgutil.walk_packages(
            package.__path__,
            prefix = f"{base_package}."
        ):
            module_name = module_info.name
            if module_name.endswith(".__init__"):
                continue

            importlib.import_module(module_name)

    @classmethod
    def register(cls, name: str):
        def decorator(item_cls):
            if name in cls._registry:
                raise ValueError(f'Item com o nome \'{name}\' já está registrado pelo {cls.__name__}.')
            cls._registry[name] = item_cls
            return item_cls
        return decorator
    
    @classmethod
    def get(cls, name: str):
        if name not in cls._registry:
            raise ValueError(f"Item com o nome '{name}' não está registrado.")
        return cls._registry[name]
    
