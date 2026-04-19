# Airflow ETL Project

## Project Overview
This project implements ETL pipelines using Apache Airflow to extract data from MySQL, transform it, and load to CSV files.

## Tech Stack
- Apache Airflow 2.10.5
- Python 3.12
- MySQL 8.0
- Pandas
- PyMySQL

## Project Structure EOF

airflow_etl_project/
├── dags/ # Airflow DAG files
│ ├── etl_pipelines/ # ETL pipeline DAGs
│ └── common/ # Common DAG utilities
├── plugins/ # Custom plugins
│ ├── operators/ # Custom operators
│ └── hooks/ # Custom hooks
├── include/ # Helper scripts
├── scripts/ # Shell scripts
├── config/ # Configuration files
├── tests/ # Unit tests
├── data/ # Data storage
└── logs/ # Airflow logs


## Setup Instructions

### Prerequisites
```bash
sudo apt update
sudo apt install -y python3-pip python3-dev mysql-server

# Clone repository
git clone <your-repo-url>
cd airflow_etl_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize Airflow
export AIRFLOW_HOME=$(pwd)
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

# Start Airflow webserver
airflow webserver --port 8080

# Start Airflow scheduler (new terminal)
airflow scheduler

# Access UI at http://localhost:8080

## ETL Pipelines
# MySQL to CSV ETL

    Extracts data from MySQL sample_data table

    Transforms: Filters records with age > 30

    Loads: Saves to CSV in data/output/

Environment Variables

Create .env file:

MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=etl_example

pytest tests/


#### **requirements.txt**
```bash
cat > requirements.txt << 'EOF'
apache-airflow==2.10.5
pandas==2.2.0
pymysql==1.1.0
sqlalchemy==2.0.25
mysqlclient==2.2.0
pytest==7.4.3
black==23.12.0
flake8==7.0.0
python-dotenv==1.0.0
