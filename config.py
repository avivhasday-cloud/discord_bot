import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    ADMIN_USER = os.environ.get('ADMIN_USER')
    TOKEN = os.environ.get('TOKEN')
