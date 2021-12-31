from dataclasses import field
import trackme.database.influx as influx_db
from typing import Dict, Union, Generator, Any
from influxdb_client.client.flux_table import FluxRecord
from trackme.contants import *


class BaseRepository:

    def __init__(self) -> None:
        self.write_api = influx_db.write_api
        self.query_api = influx_db.query_api

    def create_one(self, measurement: str, tag_set: Dict, field_set: Dict) -> None:
        record = {
            'measurement': measurement,
            'tags': tag_set,
            'fields': field_set,
        }
        self.write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=record)

    def find_latest_one(
            self,
            measurement: str,
            tag_set: Dict,
            start: str = '-30m',
            field_key: str = None,
            field_value: Union[str, int, float] = None) -> Generator[FluxRecord, Any, None]:
        query = f'from(bucket: "{INFLUX_BUCKET}")'
        query += f'|> range(start: {start})'
        query += f'|> filter(fn: (r) => r._measurement == "{measurement}")'

        for key, value in tag_set.items():
            query += f'|> filter(fn: (r) => r.{key} == "{value}")'

        if field_key is not None and field_value is not None:
            query += f'|> filter(fn: (r) => r._field == "{field_key}" and r._value == "{field_value}")'

        query += '|> last()'
        return self.query_api.query_stream(org=INFLUX_ORG, query=query)