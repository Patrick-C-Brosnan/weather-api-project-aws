from datetime import datetime
from airflow.sdk import dag, task, get_current_context
import os
import sys

# Get the absolute path of the directory containing the current file
#dag_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the folder you want to import from (e.g., go up one level, then into 'sibling_folder')
#src_dir = os.path.join(dag_dir, "..", "src")
# Add it to Python's search path
#sys.path.append(os.path.abspath(src_dir))


from weather_api import extract_weather_for_locations
from transformations import transform_weather_data_locations
from database import insert_into_database



# def get_data_date() -> str:
#     context = get_current_context()
#     dag_run = context["dag_run"]

#     if dag_run.logical_date is None:
#         raise ValueError(
#             "This DAG run has no logical date, so a data date cannot be derived."
#         )

#     return dag_run.logical_date.date().isoformat()
    
#data_date = '2026-09-19' 


@dag(
    dag_id="weather_pipeline",
    description="A pipeline for extracting weather data and inserting into a Postgres DB",
    schedule="@daily",
    start_date=datetime(2026, 9, 17),
    catchup=False,
    tags=["week-3", "learning"],
)

def weather_pipeline():

    @task
    def pipeline_extract():
        return extract_weather_for_locations()

    @task
    def pipeline_transform(extract_result: dict):
        return transform_weather_data_locations(extract_result)

    @task
    def pipeline_load(transform_result: dict):
        return insert_into_database(transform_result)

    extract_result = pipeline_extract()
    transform_result = pipeline_transform(extract_result)
    load_result = pipeline_load(transform_result)

    #extract_result >> transform_result >> load_result


weather_pipeline()