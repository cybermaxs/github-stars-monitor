.PHONY: install ingest transform clean refresh dashboard run

install:
	uv sync
	cd transform && uv run dbt deps
	cd dashboard && npm install

ingest:
	uv run ingestion/github.py

transform:
	cd transform && uv run dbt build

dashboard:
	cd dashboard && npm run sources && npm run build

clean:
	rm data/github.duckdb

refresh: clean ingest transform dashboard

run: ingest transform dashboard
