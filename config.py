import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    API = os.environ.get('API')
    PROJECT = os.environ.get('PROJECT')
    URL_LIST_JOBS = os.environ.get('URL_LIST_JOBS')
    URL_GET_ELEM = os.environ.get('URL_GET_ELEM')
    URL_RUN_JOB = os.environ.get('URL_RUN_JOB')
    spiders = {
        'mdtech1': {'mdtech': 'mdtech'},
        'dinaton': {

            'dinatonpart1': 'dinatonpart1',
            'dinatonpart2': 'dinatonpart2',
            'dinatonpart3': 'dinatonpart3',
            'dinatonpart4': 'dinatonpart4',

        }

    }
    SHOP_TRANSLATE = {
        'dinaton': 'Динатон'
    }
    PART_OF_IMAGE_LIST = 8
    BRAND_NO_CHANGE_PRICE = ["yamaha", "casio", "roland", "boss", "korg"]
    IMG_PATH = os.environ.get('IMG_PATH')
    CATEGORY_FILE_PATH = os.environ.get('CATEGORY_FILE_PATH')
    OUTPUT_PATH = os.environ.get('OUTPUT_PATH')
    SCHED_EXPORT_PATH = os.environ.get('SCHED_EXPORT_PATH')
    SCHED_IMPORT_PATH = os.environ.get('SCHED_IMPORT_PATH')
    NAME_MODEL_FILE = os.environ.get('NAME_MODEL_FILE')
    RAW_PATH = os.environ.get('RAW_PATH')
    CSV_PRO_URL = os.environ.get('CSV_PRO_URL')
    SHEDULERS = {

        'dinaton': {

            'gitar': {
                'del': {
                    'export': '1545038027',
                    'import': '1545380365'
                    },
                'add': {
                    'import': '1545222565'
                    }
                },
            'duhovye': {
                'del': {
                    'export': '',
                    'import': '',
                },
                'add': {
                    'import': ''
                }

                },
            'udarnie': {
                'del': {
                    'export': '',
                    'import': '',
                    },
                'add': {
                    'import': ''
                    }

                },
            'all': {
                'update': {
                    'export': '1545038827',
                    'import': '1545380543'
                }
            }
        }
    }
