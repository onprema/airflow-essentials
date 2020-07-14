# Airflow Essentials

## Installing Airflow with Docker

* Build the docker image
```
docker build -t airflow .
```

* Run airflow in a container
```
docker run -d -p 8080:8080 airflow
```

* Run airflow in a container (with mounted volume)
```
docker run -d -p 8080:8080 \
    -v $(pwd)/mnt/dags:/usr/local/airflow/dags \
    -v $(pwd)/mnt/airflow.cfg:/usr/local/airflow/airflow.cfg airflow
```

* Access the airflow UI at [localhost:8080](http://localhost:8080)

## Airflow CLI Commands
```bash
# Check for errors in your DAG
python $DAG

# List DAGS
airflow list_dags

# Lists tasks in a DAG
airflow list_tasks $DAG

# Test a DAG (doesn't modify database)
airflow test $DAG $TASK
```

## Installing Airflow with docker-compose

```
docker-compose up -d
```

## airflow.cfg vs airflow-multinode.cfg

These are the differences between the config files:
* executor = CeleryExecutor
* sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@postgres:5432/airflow

## Ad-Hoc Queries

#### SQLite

Connection = /usr/local/airflow/airflow.db
```sql
select * from sqlite_master;
```

#### Postgres

```sql
select * from pg_catalog.pg_tables;
```