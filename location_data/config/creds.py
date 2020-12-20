'''


'''
from dotenv import load_dotenv, find_dotenv
import os

current_path = os.path.abspath(os.path.dirname(__file__))
env_file = '.env'
env_path = os.path.join(current_path, env_file)


load_dotenv(env_path)


def get_google_key():
    return os.environ['GOOGLE_API_KEY']

def get_wextractor_key():
    return os.environ['WEXTRACTOR_API_KEY']

def get_yelp_key():
    return os.environ['YELP_API_KEY']


print(get_google_key())
