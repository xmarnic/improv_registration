# This file contains most of the configuration variables
import os

DEBUG=os.environ.get('DEBUG')
SECRET_KEY =os.environ.get('SECRET_KEY')
DATABASE_URL=os.environ.get('DATABASE_URL')
