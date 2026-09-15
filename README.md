# etl-platform

A small, config-driven ETL / data integration tool. Inspired by platforms
like Zwiron — pipelines are defined in YAML, not hardcoded, and every run
produces a schema catalog entry and quality check results.

## Why this exists

Most beginner ETL scripts hardcode the source, transform, and target in one
file. This project separates those concerns so adding a new pipeline means
writing a config file, not new code — and every run leaves an audit trail
of what landed and whether it passed basic sanity checks.

## Structure

```
extractors/     pluggable data sources (currently: csv)
loaders/        pluggable data targets (currently: sqlite)
transform.py    column-level transform ops (upper/lower/strip)
catalog.py      records table schema + row count after each load
quality.py      runs post-load checks (not_empty, no_nulls) and logs results
pipeline.py     orchestrates extract -> transform -> load -> catalog -> quality
cli.py          command-line entrypoint
configs/        one YAML file per pipeline
```

## Run it

```bash
pip install -r requirements.txt
python cli.py run configs/customers.yaml
python cli.py catalog data/warehouse.db   # see what's been cataloged
```

## Adding a new pipeline

No code changes needed — copy `configs/customers.yaml`, point `source.path`
at a new CSV, adjust `target.table`, and run it.

## Roadmap

- [ ] Postgres/MySQL extractors and loaders
- [ ] Incremental sync (not just full refresh)
- [ ] More transform ops + row-level filters
- [ ] More quality checks (uniqueness, type checks, custom SQL assertions)
- [ ] Simple web UI to browse the catalog and run history
- [ ] CDC-based sync
- [ ] Outbound-only local agent mode (à la Zwiron) for private DBs
