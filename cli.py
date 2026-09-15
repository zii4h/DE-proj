import argparse
from pipeline import Pipeline
from catalog import show_catalog


def main():
    parser = argparse.ArgumentParser(prog="etl-platform")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a pipeline from a config file")
    run_parser.add_argument("config", help="Path to pipeline YAML config, e.g. configs/customers.yaml")

    catalog_parser = subparsers.add_parser("catalog", help="Show what's been cataloged in a warehouse db")
    catalog_parser.add_argument("db", help="Path to the SQLite warehouse file, e.g. data/warehouse.db")

    args = parser.parse_args()

    if args.command == "run":
        pipeline = Pipeline(args.config)
        pipeline.run()
    elif args.command == "catalog":
        print(show_catalog(args.db))


if __name__ == "__main__":
    main()
