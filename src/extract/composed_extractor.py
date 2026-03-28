from src.extract.extractor import Extractor


class ComposedExtractor(Extractor):
    
    def __init__(self, extractor_classes, extractors_configs) -> None:
        self.__extractor_classes = extractor_classes
        self.__extractors_configs = extractors_configs

    def extract(self) -> tuple[list[dict], dict]:
        metadata = {
            'extractors': [],
        }
        extracted_data = None
        for extractor_cls, extractor_config in zip(self.__extractor_classes, self.__extractors_configs):
            if extracted_data is None:
                extractor = extractor_cls(extractor_config)
            else:
                extractor = extractor_cls(extractor_config, extracted_data)
            extracted_data, extractor_metadata = extractor.extract()
            extracted_data = extracted_data

            metadata['extractors'].append({
                'type': extractor_config.type,
                'metadata': extractor_metadata,
            })

        return extracted_data, metadata