#!/bin/bash

# Setup script for Airflow ETL project

echo "Setting up Airflow ETL Project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
mysql -uroot -proot < scripts/init.sql

# Set Airflow home
export AIRFLOW_HOME=$(pwd)

# Initialize Airflow
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

echo "Setup complete!"
echo "Run 'airflow webserver --port 8080' to start"
