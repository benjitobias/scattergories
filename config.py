import os

DB_NAME = "scat"
WORD_COLLECTION_NAME = "words"
CATEGORY_COLLECTION_NAME = "categories"
SESSION_COLLECTION_NAME = "sessions"


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
