from bson.objectid import ObjectId

from pymongo import MongoClient

import config
from config import *

client = MongoClient("localhost", 27017)

scat_db = client[config.DB_NAME]
session_collection = scat_db[config.SESSION_COLLECTION_NAME]
category_collection = scat_db[config.CATEGORY_COLLECTION_NAME]


def add_category(category):
    return category_collection.insert_one({"category": category})


def get_twelve_categories():
    pipeline = [
        {"$sample": {"size": 12}}
    ]
    categories = [cat["category"] for cat in list(category_collection.aggregate(pipeline))]
    return categories


def insert_session_categories(session_code, categories):
    session_collection.update(
        {"session_code": session_code},
        {"$unset": {"categories": ""}}
        )

    session_collection.update(
        {"session_code": session_code},
        {
            "$push": {
                "categories": categories
            }
        })


def get_session_round(session_code):
    return session_collection.find_one({"session_code": session_code}, {"round": 1})["round"]


def update_round(session_code):
    new_round = get_session_round(session_code) + 1
    session_collection.update({"session_code": session_code},
                              {"$set": {"round": int(new_round)}}
                              )


def get_session_categories(session_code):
    session_data = session_collection.find_one({"session_code": session_code}, {"categories": 1, "round": 1})
    return session_data



def get_session(session_code):
    return session_collection.find_one({"session_code": session_code})


def create_session(session_code):
    session_collection.insert_one({"session_code": session_code, "players": [], "round": 0})


def get_player(session_code, player):
    player = session_collection.aggregate([
        {"$unwind": "$players"},
        {"$match": {"session_code": session_code, "players.name": player}},
    ])
    try:
        return player.next()
    except StopIteration:
        return None


def create_player(session_code, player):
    session_collection.update(
        {"session_code": session_code},
        {"$addToSet": {"players": {"name": player}}}
    )


def insert_session_letter(session_code, letter):
    session_collection.update(
        {"session_code": session_code},
        {"$unset": {"letter": ""}}
    )

    session_collection.update(
        {"session_code": session_code},
        {
            "$push": {
                "letter": letter
            }
        })


def get_session_letter(session_code):
    return session_collection.find_one({"session_code": session_code}, {"letter": 1, "_id": 0})


def get_all_categories():
    return list(category_collection.find())


def update_category(category_id, category):
    category_collection.update({"_id": ObjectId(category_id)}, {"category": category})


def delete_category(category_id):
    category_collection.remove({"_id": ObjectId(category_id)})
