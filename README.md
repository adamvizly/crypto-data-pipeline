Crypto Data ETL Boilerplate

This is a boilerplate project for learning data science and ETL workflows using Apache Airflow and Metabase.
It demonstrates how to fetch cryptocurrency data from the CoinGecko API, store it in PostgreSQL, and visualize it with Metabase.

Tech Stack

- Apache Airflow – workflow orchestration and scheduling
- PostgreSQL – database to store processed data
- Metabase – visualization layer / BI tool
- Python – ETL and API integration
- Docker & Docker Compose – containerized development environment

Features

- ETL pipeline to fetch cryptocurrency data (Bitcoin, Ethereum, Solana)
- Stores historical and hourly data in PostgreSQL
- Airflow DAG automatically backfills 1 day of historical data and continues hourly
- Table creation handled by Airflow (PostgresOperator)
- Data processing and insertion using Pandas and PostgresHook
- Visualization-ready: Metabase connects to PostgreSQL to create dashboards

Project Structure

.
├── dags/
│   └── crypto_dag.py         # Airflow DAG for fetching and storing crypto data
├── Dockerfile                # Custom Airflow image (if needed)
├── docker-compose.yml        # Services: Airflow, PostgreSQL, Metabase
├── .env                      # Environment variables for DB and Airflow
└── README.md

How It Works

1. Airflow DAG (crypto_dag.py)
   - Creates table crypto_prices if it doesn't exist
   - Fetches historical data for last 1 day
   - Runs hourly to fetch the latest prices
   - Inserts processed data into PostgreSQL

2. Data Processing
   - API response transformed into Pandas DataFrame
   - Timestamps standardized
   - Market caps included

3. Visualization
   - Connect Metabase to PostgreSQL
   - Create dashboards for cryptocurrency prices and market cap trends

Notes

- CoinGecko API has rate limits; DAG fetches 1 day of data per run to avoid 429 Too Many Requests.
- For learning purposes, this boilerplate is designed to be modular and easily extendable.
- You can add new coins by updating the DAG’s coins list.

Learning Goals

- Learn how to create ETL pipelines with Airflow
- Practice Python data processing with Pandas
- Understand scheduling and backfilling in Airflow
- Store and query data in PostgreSQL
- Create dashboards using Metabase

Useful Links

- Apache Airflow Docs: https://airflow.apache.org/docs/apache-airflow/stable/
- CoinGecko API Docs: https://www.coingecko.com/en/api/documentation
- Metabase Docs: https://www.metabase.com/docs/latest/
