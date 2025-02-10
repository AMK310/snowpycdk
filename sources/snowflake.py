from airbyte_cdk.sources.abstract_source import AbstractSource
from airbyte_cdk.models import SyncMode, AirbyteCatalog, AirbyteStream
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.utils.schema_helpers import ResourceSchemaLoader
from snowflake.connector import connect
from typing import Dict, Iterable, Optional, List, Union

class SnowflakeStream(Stream):
    def __init__(self, config: Dict, table_name: str, cursor_field: Optional[str] = None):
        """Initializes Snowflake stream for a given table."""
        self.config = config
        self.table_name = table_name
        self.cursor_field = cursor_field
    
    def primary_key(self) -> Optional[Union[str, List[str]]]:
        """Returns the primary key of the table (or None if not applicable)."""
        return "id"  # Replace with actual primary key of your table

    def read_records(self, sync_mode: SyncMode, cursor_field: Optional[str] = None, stream_slice: Optional[Dict] = None, stream_state: Optional[Dict] = None) -> Iterable[Dict]:
        """Fetches records from Snowflake."""
        connection = connect(
            user=self.config['username'],
            password=self.config['password'],
            account=self.config['account'],
            host=self.config['host'],
            protocol=self.config['protocol'],
            port=self.config['port'],
            warehouse=self.config['warehouse'],
            database=self.config['database'],
            schema=self.config['schema']
        )
        cursor = connection.cursor()

        # Query to fetch data from the table
        query = f"SELECT * FROM {self.table_name}"
        if sync_mode == SyncMode.incremental and self.cursor_field and stream_state:
            query += f" WHERE {self.cursor_field} > '{stream_state.get(self.cursor_field)}'"

        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        for record in cursor:
            yield dict(zip(columns, record))
        
        cursor.close()
        connection.close()

    def get_updated_state(self, current_stream_state: Dict, latest_record: Dict) -> Dict:
        """Updates stream state based on the latest record."""
        if self.cursor_field:
            current_stream_state[self.cursor_field] = max(
                latest_record.get(self.cursor_field, ""),
                current_stream_state.get(self.cursor_field, "")
            )
        return current_stream_state

    def supports_incremental(self) -> bool:
        """Indicates whether the stream supports incremental sync."""
        return self.cursor_field is not None
    
    def cursor_field(self) -> Union[str, List[str]]:
        """Returns the cursor field for tracking changes."""
        return "updated_at"  # Set the field used for tracking updates

class SourceSnowflake(AbstractSource):
    def check_connection(self, logger, config: Dict) -> tuple:
        """Checks the connection to Snowflake."""
        try:
            connection = connect(
                username=config['username'],
                password=config['password'],
                host=config['host'],
                protocol=config['protocol'],
                port=config['port'],
                account=config['account'],
                warehouse=config['warehouse'],
                database=config['database'],
                schema=config['schema']
            )
            connection.close()
            return True, None
        except Exception as e:
            return False, str(e)

    def discover(self, logger, config: Dict) -> AirbyteCatalog:
        """Discovers available streams (tables) in Snowflake."""
        streams = []
        for table in ["your_table", "another_table"]:
            # Replace with dynamic schema discovery if required
            json_schema = ResourceSchemaLoader(table).get_schema("snowflake")
            streams.append(AirbyteStream(name=table, json_schema=json_schema))
        return AirbyteCatalog(streams=streams)

    def read(self, logger, config: Dict, catalog: AirbyteCatalog, state: Dict = None) -> Iterable[Dict]:
        """Reads records from the streams in the catalog."""
        for stream in self.streams(config):
            yield from stream.read_records(SyncMode.full_refresh)

    def streams(self, config: Dict) -> List[Stream]:
        """Returns a list of streams (tables) configured for extraction."""
        return [
            SnowflakeStream(config, "your_table", cursor_field="updated_at"),
            SnowflakeStream(config, "another_table")
        ]
