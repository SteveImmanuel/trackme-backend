from dotenv import load_dotenv

load_dotenv()

import os

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_EXPIRY_TIME = int(os.getenv('JWT_EXPIRY_TIME'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DEFAULT_EXPIRY_TIME = int(os.getenv('REDIS_DEFAULT_EXPIRY_TIME'))

INFLUX_HOST = os.getenv('INFLUX_HOST')
INFLUX_PORT = int(os.getenv('INFLUX_PORT'))
INFLUX_USERNAME = os.getenv('INFLUX_USERNAME')
INFLUX_PASSWORD = os.getenv('INFLUX_PASSWORD')
INFLUX_TOKEN = os.getenv('INFLUX_TOKEN')
INFLUX_BUCKET = os.getenv('INFLUX_BUCKET')
INFLUX_ORG = os.getenv('INFLUX_ORG')