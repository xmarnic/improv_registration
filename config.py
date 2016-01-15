# This file contains most of the configuration variables
import os

DEBUG=False
SECRET_KEY =os.environ.get('SECRET_KEY')
DATABASE_URL=os.environ.get('DATABASE_URL')
