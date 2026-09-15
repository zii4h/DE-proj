import yaml
from extractors import get_extractor
from loaders import get_loader
from transform import apply_transforms
from catalog import update_catalog
from quality import run_checks


class Pipeline:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)

    def run(self):
        name = self.config["pipeline"]
        print(f"=== running pipeline: {name} ===")

        extractor = get_extractor(self.config["source"])
        df = extractor.extract()

        df = apply_transforms(df, self.config.get("transform"))

        loader = get_loader(self.config["target"])
        loader.load(df)

        engine = loader.get_engine()
        table_name = self.config["target"]["table"]

        update_catalog(engine, table_name, df, pipeline_name=name)
        results = run_checks(engine, table_name, df, self.config.get("quality"), pipeline_name=name)

        failed = [r for r in results if not r["passed"]]
        if failed:
            print(f"=== {name} finished with {len(failed)} quality check(s) FAILED ===")
        else:
            print(f"=== {name} finished successfully ===")

        return {"pipeline": name, "rows": len(df), "quality_results": results}
