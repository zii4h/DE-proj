from loaders.sqlite_loader import SQLiteLoader

LOADER_REGISTRY = {
    "sqlite": SQLiteLoader,
}


def get_loader(config: dict):
    loader_cls = LOADER_REGISTRY.get(config["type"])
    if loader_cls is None:
        raise ValueError(f"Unknown loader type: {config['type']}")
    return loader_cls(config)
