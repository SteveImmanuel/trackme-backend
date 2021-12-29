from dotenv import load_dotenv

load_dotenv()

import os

DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_EXPIRY_TIME = int(os.getenv('JWT_EXPIRY_TIME'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_DEFAULT_EXPIRY_TIME = int(os.getenv('REDIS_DEFAULT_EXPIRY_TIME'))
