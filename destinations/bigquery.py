from google.cloud import bigquery
from typing import Iterable, Dict

def write_to_bigquery(records: Iterable[Dict], dataset_id: str, table_id: str):
    """
    Writes records to a specified BigQuery table.

    Args:
        records (Iterable[Dict]): The records to insert.
        dataset_id (str): The dataset ID in BigQuery.
        table_id (str): The table ID where the data will be written.
    """
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    # Prepare rows for insertion
    rows_to_insert = [tuple(record.values()) for record in records]
    errors = client.insert_rows(table, rows_to_insert)

    if errors:
        print(f"Errors occurred while inserting rows: {errors}")
    else:
        print(f"Data successfully written to BigQuery table {dataset_id}.{table_id}")
