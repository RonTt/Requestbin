from os import environ, path
from dotenv import find_dotenv, load_dotenv


filename = '.env'
if "ENV" not in environ:
    filename = 'local.env'
else:
    filename = f'{environ.get("ENV")}.env'


basedir = path.abspath(path.dirname(__file__))
dotenv_file = path.join(basedir, filename)
if find_dotenv(dotenv_file):
    load_dotenv(dotenv_file)


class Configuration(object):
    def __init__(self):
        self.test_data_path = './data'
        self.reqres_api_url = environ.get('REQRES_URL')
        self.reqres_api_version = environ.get('REQRES_API_VERSION')
