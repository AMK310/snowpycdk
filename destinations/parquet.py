import pyarrow as pa
import pyarrow.parquet as pq
from typing import Iterable, Dict

def write_to_parquet(records: Iterable[Dict], output_path: str):
    """
    Writes a list of records (dictionaries) to a Parquet file.

    Args:
        records (Iterable[Dict]): The records to write to the file.
        output_path (str): Path where the Parquet file should be saved.
    """
    # Convert the records to a PyArrow Table
    table = pa.Table.from_pylist(records)

    # Write the table to a Parquet file
    pq.write_table(table, output_path)
