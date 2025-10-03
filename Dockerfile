FROM apache/airflow:2.9.2

USER root
# Install build-essential for compiling some python packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean

USER airflow
# Install python packages
RUN pip install --no-cache-dir \
    "apache-airflow-providers-postgres==5.10.0" \
    "pandas" \
    "requests" \
    "sqlalchemy"
