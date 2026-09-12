import os

class Config:
    PROJECT_NAME = 'Cloudburst Warning Backend'
    VERSION = '1.0.0'
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./cloudburst.db')
    LORA_PORT = os.getenv('LORA_PORT', '/dev/ttyUSB0')

config = Config()
