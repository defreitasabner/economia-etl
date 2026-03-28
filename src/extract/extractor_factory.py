from src.config.models.dataset_config import ExtractConfig
from src.extract.composed_extractor import ComposedExtractor
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


class ExtractorFactory:

    @staticmethod
    def create(extract_config: ExtractConfig) -> Extractor:
        if len(extract_config.extractors) == 0:
            raise ValueError("No extractors defined in the configuration.")
        extractors_classes = []
        extractors_configs = []
        for extractor_cfg in extract_config.extractors:
            extractor_cls = ExtractorRegistry.get(extractor_cfg.type)
            extractors_classes.append(extractor_cls)
            extractors_configs.append(extractor_cfg)
        return ComposedExtractor(extractors_classes, extractors_configs)
    
