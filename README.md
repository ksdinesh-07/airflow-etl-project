# Airflow ETL Pipeline Project

## Project Overview

This project implements an automated ETL (Extract, Transform, Load) pipeline using Apache Airflow to extract data from MySQL database, transform it by filtering records, and load the processed data into CSV files. The pipeline runs on a scheduled basis, eliminating manual data processing and ensuring consistent, timely data delivery.

## Problem Statement

Organizations often need to regularly extract, filter, and export data from databases for reporting, analysis, or integration with other systems. Doing this manually is:
- Time-consuming and error-prone
- Not scalable for large datasets
- Difficult to schedule and monitor
- Lacks proper error handling and logging

## Solution

This project provides an automated ETL solution using Apache Airflow that:
- **Extracts** data from MySQL database tables
- **Transforms** data by applying business rules (e.g., filtering age > 30)
- **Loads** transformed data into CSV files with timestamps
- **Schedules** the entire pipeline to run automatically
- **Monitors** execution with a web-based UI
- **Logs** all activities for debugging and auditing

## Technical Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Orchestration | Apache Airflow 2.10.5 | Schedule and manage ETL workflows |
| Database | MySQL 8.0 | Source data storage |
| Processing | Python 3.12 + Pandas | Data transformation |
| Containerization | Docker | MySQL containerization |
| Version Control | Git & GitHub | Code management |
| CI/CD | GitHub Actions | Automated testing |
| IDE | VS Code | Development environment |


## ETL Pipeline Details

### Extract Phase

**Source:** MySQL Database (`etl_example.sample_data`)

**Operation:**

sql
SELECT * FROM sample_data

id | name      | age | city          | created_at
---|-----------|-----|---------------|-------------------
1  | Alice     | 30  | New York      | 2024-01-01 10:00:00
2  | Bob       | 25  | Los Angeles   | 2024-01-01 10:00:00
3  | Charlie   | 35  | Chicago       | 2024-01-01 10:00:00
4  | David     | 40  | Houston       | 2024-01-01 10:00:00
5  | Eva       | 28  | Phoenix       | 2024-01-01 10:00:00
6  | Frank     | 33  | Miami         | 2024-01-01 10:00:00

### Transform Phase

Business Rule: Filter records where age > 30

## Transformation Logic:

df_transformed = df[df['age'] > 30]

## Transformed Data:

id | name      | age | city          | created_at
---|-----------|-----|---------------|-------------------
3  | Charlie   | 35  | Chicago       | 2024-01-01 10:00:00
4  | David     | 40  | Houston       | 2024-01-01 10:00:00
6  | Frank     | 33  | Miami         | 2024-01-01 10:00:00

### Load Phase

Destination: CSV file with timestamp

### Output Format:
id,name,age,city,created_at
3,Charlie,35,Chicago,2024-01-01 10:00:00
4,David,40,Houston,2024-01-01 10:00:00
6,Frank,33,Miami,2024-01-01 10:00:00

File Naming Convention: etl_output_YYYYMMDD_HHMMSS.csv
### Features
## Core Features

    ✅ Automated ETL pipeline execution

    ✅ Scheduled daily runs (configurable interval)

    ✅ MySQL database connectivity

    ✅ Pandas-based data transformation

    ✅ CSV output with timestamps

    ✅ Error handling and retry logic

    ✅ Execution logging and monitoring

## Airflow Features Used

    DAGs: Directed Acyclic Graphs for workflow definition

    Operators: PythonOperator for custom ETL logic

    XCom: Cross-communication between tasks

    Scheduler: Automated task scheduling

    Web UI: Real-time monitoring interface

    Logging: Detailed execution logs

## DevOps Features

    Docker: Containerized MySQL database

    Git: Version control

    GitHub Actions: CI/CD pipeline

    Makefile: Automated commands

    Environment Variables: Secure configuration

### Installation & Setup
## Prerequisites

# Ubuntu/Debian
sudo apt update
sudo apt install -y python3-pip python3-dev mysql-server git

# Verify installations
python3 --version  # Should be 3.8+
mysql --version    # Should be 8.0+
git --version

## Quick Setup
# Clone repository
git clone https://github.com/ksdinesh-07/airflow-etl-project.git
cd airflow-etl-project

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or use Makefile
make setup

### Manual Setup Steps
  1.Create Virtual Environment
    python3 -m venv venv
    source venv/bin/activate
    
  2.Install Dependencies
    pip install -r requirements.txt
  
  3.Initialize Database
    mysql -uroot -proot < scripts/init.sql
  
  4.Initialize Airflow
    export AIRFLOW_HOME=$(pwd)
    airflow db init
  
  5.Create Admin User
    airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com

  ### Running the Project
    # Start Services

    ## Terminal 1 - Web Server:
        cd ~/airflow_etl_project
        source venv/bin/activate
        export AIRFLOW_HOME=$(pwd)
        airflow webserver --port 8080

    ## Terminal 2 - Scheduler:
        cd ~/airflow_etl_project
        source venv/bin/activate
        export AIRFLOW_HOME=$(pwd)
        airflow scheduler

    ## Terminal 3 - MySQL (if using Docker):
        docker-compose up -d

### Access Airflow UI

    URL: http://localhost:8080

    Username: admin

    Password: admin

### Trigger Pipeline

    Navigate to DAGs list

    Find mysql_to_csv_etl

    Toggle ON

    Click "Trigger DAG" button

### Monitoring & Logs
## Airflow UI Views

    Graph View: Visual representation of task dependencies

    Tree View: Historical runs overview

    Task Duration: Performance metrics

    Logs: Detailed execution logs for each task

### Log Locations
## bash

# Airflow logs
~/airflow_etl_project/logs/

# Task logs
~/airflow_etl_project/logs/mysql_to_csv_etl/

# Application logs
~/airflow_etl_project/data/output/summary_*.txt

Testing
Run Tests
bash

# Run all tests
make test

# Run specific test
pytest tests/test_etl.py -v

# Run with coverage
pytest --cov=dags tests/

### Test Cases

    ✅ Data extraction validation

    ✅ Transformation logic (age > 30 filter)

    ✅ CSV file creation

    ✅ Empty dataset handling

    ✅ Error scenarios

### CI/CD Pipeline (GitHub Actions)

The project includes GitHub Actions for automated testing:
yaml

### Trigger: Push to main/develop or Pull Request
## Jobs:
  - Lint Python code with flake8
  - Run unit tests with pytest
  - Validate DAG structure
  - Check code formatting

### Use Cases
## Business Applications

    Customer Segmentation: Filter customers based on age groups

    Employee Reporting: Generate senior employee reports

    Sales Analysis: Extract and filter sales data by region

    Compliance Reporting: Export filtered data for audits

    Data Integration: Prepare data for external systems

### Industries That Can Benefit

    E-commerce: Customer data processing

    Healthcare: Patient record filtering

    Banking: Transaction data extraction

    HR: Employee database reporting

    Marketing: Campaign data segmentation

### Performance Metrics
## Metric	Value
Execution Time	< 5 seconds for 10,000 records
Memory Usage	~50MB
DAG Load Time	< 2 seconds
Scheduling Interval	Configurable (default: daily)
Retry Attempts	3 attempts with 1-minute delay

### Future Enhancements
## Planned Features

    Email notifications on completion/failure

    Multiple data source support (PostgreSQL, MongoDB)

    Data quality checks and validation

    Dashboard for ETL metrics

    Slack/Teams integration

    Incremental loading (only new records)

    Data encryption for sensitive information

    API endpoint for triggering ETL

### Scalability Improvements

    Parallel task execution

    Distributed processing with Celery

    Cloud storage integration (S3, GCS)

    Data partitioning for large datasets

### Troubleshooting
## Common Issues & Solutions
##Issue	Solution
MySQL connection failed	Check if MySQL is running: sudo systemctl status mysql
DAG not appearing in UI	Check syntax: python3 -m py_compile dags/etl_pipelines/mysql_to_csv_etl.py
Permission denied	Run chmod +x scripts/*.sh
Port 8080 already in use	Use different port: airflow webserver --port 8081
Module not found	Activate venv: source venv/bin/activate
Contributing

    Fork the repository

    Create feature branch (git checkout -b feature/amazing-feature)

    Commit changes (git commit -m 'Add amazing feature')

    Push to branch (git push origin feature/amazing-feature)

    Open Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Apache Airflow Community

    MySQL Developers

    Open Source Contributors

Contact

    Project Maintainer: Dinesh

    GitHub: yourusername

    Email: dinesh@example.com

Version History
Version	Date	Changes
1.0.0	2024-01-15	Initial release
1.1.0	2024-02-01	Added tests and CI/CD
1.2.0	2024-02-15	Docker support added
Quick Commands Reference
bash

# Setup project
make setup

# Run tests
make test

# Start web server
make run-webserver

# Start scheduler
make run-scheduler

# Start MySQL with Docker
make docker-up

# Clean project
make clean

# Push to GitHub
git add .
git commit -m "message"
git push origin main

Conclusion

This Airflow ETL project provides a robust, scalable, and maintainable solution for automated data processing. It demonstrates best practices in data engineering including:

    Orchestration with Apache Airflow

    Modular code structure

    Comprehensive testing

    CI/CD integration

    Detailed documentation

    Easy setup and deployment

The project serves as both a practical ETL solution and a learning resource for understanding modern data pipeline patterns.
