from pymongo import MongoClient

import config
from config import *

client = MongoClient("localhost", 27017)

scat_db = client[config.DB_NAME]
word_collection = scat_db[config.WORD_COLLECTION_NAME]
session_collection = scat_db[config.SESSION_COLLECTION_NAME]
category_collection = scat_db[config.CATEGORY_COLLECTION_NAME]


def add_word(word):
    word_collection.insert_one({"word": word})


def add_category(category):
    category_collection.insert_one({"category": category})


def get_twelve_categories():
    pipeline = [
        {"$match": {"used": False}},
        {"$sample": {"size": 12}}
    ]
    categories = [cat["category"] for cat in list(category_collection.aggregate(pipeline))]
    return categories


def get_session(session_code):
    return session_collection.find_one({"session_code": session_code})


def create_session(session_code):
    session_collection.insert_one({"session_code": session_code, "players": []})


def get_player(session_code, player):
    return session_collection.find_one({"session_code": session_code, "player": player})


def create_player(session_code, player):
    session_collection.update(
        {"session_code": session_code},
        {"$addToSet": {"players": {"name": player}}}
    )

