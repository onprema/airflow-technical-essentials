# Airflow Technical Essentials

This repository contains code and examples used alongside the Apache Airflow Technical Essentials live training on O'Reilly.

## Prerequisites
* [Docker](https://docs.docker.com/get-docker/)
* [Astro CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)

## Quickstart
```
astro dev init
astro dev start
```

## dags/example_dag.py
A basic DAG that introduces the concepts of **tasks**, **operators**, **dependencies**, and the **DAG**.

## dags/weather_checker.py
A more robust DAG that uses **variable**, **connection**, **xcom**, **SimpleHTTPOperator**, and **task context**.

## dags/query_dag.py
A dag that queries the Airflow metastore using the `PostgresOperator`.

## Accessing the metastore container
```
docker exec -it $POSTGRES_CONTAINER psql -h postgres -U postgres
```

## Notes
- The **logical date**, formerly known as **execution date**, is the start of the _data interval_, not when the DAG is actually executed.
- Environment variables override `airflow.cfg` (See `.env` for examples)