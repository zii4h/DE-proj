from extractors.csv_extractor import CSVExtractor

EXTRACTOR_REGISTRY = {
    "csv": CSVExtractor,
}


def get_extractor(config: dict):
    extractor_cls = EXTRACTOR_REGISTRY.get(config["type"])
    if extractor_cls is None:
        raise ValueError(f"Unknown extractor type: {config['type']}")
    return extractor_cls(config)
