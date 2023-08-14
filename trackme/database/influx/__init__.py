from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from trackme.constants import *

# initialize connection
client = InfluxDBClient(url=f'http://{INFLUX_HOST}:{INFLUX_PORT}',
                        token=INFLUX_TOKEN,
                        org=INFLUX_ORG)

# create API instance
write_api = client.write_api(write_options=ASYNCHRONOUS)
query_api = client.query_api()