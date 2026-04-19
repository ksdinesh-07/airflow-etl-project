.PHONY: setup install test run-webserver run-scheduler clean

setup:
	@echo "Setting up project..."
	./scripts/setup.sh

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

run-webserver:
	export AIRFLOW_HOME=$(PWD)
	airflow webserver --port 8080

run-scheduler:
	export AIRFLOW_HOME=$(PWD)
	airflow scheduler

clean:
	rm -rf logs/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf venv/
	rm -f airflow.db

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down
