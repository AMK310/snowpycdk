from sources.snowflake import SourceSnowflake
from destinations.parquet import write_to_parquet
from destinations.bigquery import write_to_bigquery
from airbyte_cdk.models import SyncMode
from config import config
def main():
    # Initialize the Snowflake source
    source = SourceSnowflake()

    # Check connection to the Snowflake database
    check_result, check_message = source.check_connection(None, config)
    print(f"Check result: {check_result}, Message: {check_message}")

    # Fetch streams (tables) from Snowflake source
    streams = source.streams(config)

    # Iterate over each stream (table)
    for stream in streams:
        # Read records from the stream with a full refresh
        records = list(stream.read_records(SyncMode.full_refresh))

        # Write the records to Parquet file
        write_to_parquet(records, "output.parquet")

        # Write the records to BigQuery (Uncomment the following line for BigQuery integration)
        # write_to_bigquery(records, "test_amine", "your_table")

# Ensure the script is executed as the main program
if __name__ == "__main__":
    main()
