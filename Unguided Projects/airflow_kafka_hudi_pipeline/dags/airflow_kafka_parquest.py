from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

PROJECT_PATH = "/home/hdoop/Downloads/airflow_kafka_hudi_pipeline"
SPARK_JOB = f"{PROJECT_PATH}/spark_jobs/kafka_parquet.py"
SPARK_SUBMIT = "/opt/spark/bin/spark-submit"

default_args = {
    "owner": "airflow",
}

with DAG(
    dag_id="kafka_to_parquet_streaming",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule=None,   
    catchup=False,
    tags=["spark", "kafka", "debezium"],
) as dag:

    start_stream = BashOperator(
        task_id="start_spark_stream",
        bash_command=f"""
        export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
        export SPARK_HOME=/opt/spark
        export PATH=$SPARK_HOME/bin:$PATH

        export PYSPARK_PYTHON=/usr/bin/python3
        export PYSPARK_DRIVER_PYTHON=/usr/bin/python3

        # Run Spark streaming in foreground (Airflow task will stay RUNNING)
        {SPARK_SUBMIT} \
          --master local[*] \
          --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 \
          --conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
          {SPARK_JOB}
        """
    )

