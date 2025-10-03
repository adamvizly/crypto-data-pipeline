from __future__ import annotations

from datetime import datetime, timedelta
import requests
import pandas as pd
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator


@dag(
    dag_id="crypto_data_pipeline",
    schedule_interval="@hourly",
    start_date=datetime.now() - timedelta(days=1),
    tags=["crypto", "api"],
)
def crypto_etl_dag():
    create_crypto_table_task = PostgresOperator(
        task_id="create_crypto_table",
        postgres_conn_id="postgres_default",
        sql="""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id VARCHAR(50) NOT NULL,
                symbol VARCHAR(20) NOT NULL,
                name VARCHAR(50) NOT NULL,
                price_usd FLOAT NOT NULL,
                market_cap_usd BIGINT,
                timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
                PRIMARY KEY (id, timestamp)
            );
        """,
    )

    @task()
    def fetch_last_day_data() -> dict:
        coins = ["bitcoin", "ethereum", "solana"]

        # fetch data for last 24 hours only
        end = int(datetime.utcnow().timestamp())
        start = end - 24 * 60 * 60  # 24 hours ago

        all_data = {}
        for coin in coins:
            url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range"
            params = {
                "vs_currency": "usd",
                "from": start,
                "to": end
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            all_data[coin] = data
        return all_data

    @task()
    def process_and_load_data(crypto_data: dict):
        if not crypto_data:
            print("No data received.")
            return

        id_to_meta = {
            'bitcoin': {'symbol': 'btc', 'name': 'Bitcoin'},
            'ethereum': {'symbol': 'eth', 'name': 'Ethereum'},
            'solana': {'symbol': 'sol', 'name': 'Solana'}
        }

        records = []

        for crypto_id, data in crypto_data.items():
            prices = data.get("prices", [])
            market_caps = dict(data.get("market_caps", []))

            for ts_ms, price in prices:
                ts = datetime.utcfromtimestamp(ts_ms / 1000)
                market_cap = market_caps.get(ts_ms)

                records.append({
                    "id": crypto_id,
                    "symbol": id_to_meta[crypto_id]["symbol"],
                    "name": id_to_meta[crypto_id]["name"],
                    "price_usd": price,
                    "market_cap_usd": market_cap,
                    "timestamp": ts,
                })

        df = pd.DataFrame(records)
        print("Processed DataFrame:", df.head())

        if not df.empty:
            hook = PostgresHook(postgres_conn_id="postgres_default")
            engine = hook.get_sqlalchemy_engine()
            df.to_sql('crypto_prices', engine, if_exists='append', index=False)
            print(f"✅ Loaded {len(df)} rows into DB.")

    # DAG dependencies
    fetched_data = fetch_last_day_data()
    load_task = process_and_load_data(fetched_data)

    create_crypto_table_task >> fetched_data >> load_task


crypto_etl_dag()
