class Pipeline:
    def __init__(self, extractor, transformers, loader):
        self.extractor = extractor
        self.transformers = transformers
        self.loader = loader

    def run(self):
        data, metadata = self.extractor.extract()
        for transformer in self.transformers:
            data = transformer.transform(data)
        self.loader.load(data, metadata)

