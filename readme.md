# Data Pipeline: Snowflake to Parquet & BigQuery

This project defines an ETL pipeline that extracts data from a Snowflake data warehouse, transforms it as necessary, and writes the results to both Parquet and BigQuery destinations. The pipeline utilizes the Airbyte platform to orchestrate the data flow, with Python connectors for Snowflake, Parquet, and BigQuery.

## Project Structure

- **`sources/`**: Contains the Snowflake data source connector.
  - `snowflake.py`: Defines the Snowflake connection and data extraction logic.
  
- **`destinations/`**: Contains the destination connectors for Parquet and BigQuery.
  - `parquet.py`: Defines the logic for writing data to a Parquet file.
  - `bigquery.py`: Defines the logic for writing data to a BigQuery table.

- **`main.py`**: The main execution script that runs the entire pipeline.

## Requirements

This project requires the following Python packages:

- **airbyte-cdk**: Used for building Airbyte connectors.
- **snowflake-connector-python**: Snowflake connector to interact with the Snowflake data warehouse.
- **pyarrow**: Library for writing data to Parquet format.
- **google-cloud-bigquery**: Google Cloud client for interacting with BigQuery.

### Installation

To get started, clone this repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/data-pipeline.git
cd data-pipeline
devbox enter

## Usage

To run the pipeline, execute the `main.py` script:

```bash
python main.py

## Pipeline Execution Steps

When running `main.py`, the following steps are performed:

1. **Check Connection to Snowflake**  
   - Ensures the Snowflake credentials are valid and the connection is successful.

2. **Extract Data from Snowflake**  
   - Retrieves data from the specified Snowflake tables using SQL queries.

3. **Write Data to Parquet**  
   - Converts the extracted data into a Parquet file for efficient storage and further processing.

4. **Write Data to BigQuery (Optional)**  
   - Transfers the processed data to a BigQuery dataset and table (requires Google Cloud authentication).

## Configuration

Update the `config` dictionary in `main.py` with your Snowflake and BigQuery credentials:

```python
config = {
    "username": "your_snowflake_username",
    "password": "your_snowflake_password",
    "account": "your_snowflake_account",
    "database": "your_database",
    "schema": "your_schema",
    "warehouse": "your_warehouse",
    "parquet_output": "output.parquet",
    "bigquery_dataset": "your_dataset",
    "bigquery_table": "your_table"
}
## Authentication for BigQuery

To enable writing to BigQuery, set up authentication using Google Cloud SDK:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"

## Error Handling

If any issue occurs, errors will be displayed in the console log. Common troubleshooting steps:

- Ensure your Snowflake credentials and connection details are correct.
- Verify your Google Cloud authentication for BigQuery.
- Check that dependencies are correctly installed using `devbox enter`.

## Contributing

If you wish to contribute to this project:

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with detailed changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any inquiries or collaboration opportunities, feel free to reach out:

📧 **Email:** amine.amarzouk@servier.com  
👤 **Author:** Amine Amarzouk
