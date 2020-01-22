import argparse
import json
import logging
import os
import shutil
import stat
import copy

from scraper import PythonScraper
from git import Repo

from pymongo.mongo_client import MongoClient

itemtemplate = {
    "url" : None,
    "name" : None,
    "target_commit" : None,
    "target_commit_date" : None,
    "status" : "unclaimed",
    "worker" : None,
    "source" : "popular"
    # "search_result_item": {}
}

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def parsearg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language", "-l",
        required=True,
        type=str
    )
    parser.add_argument(
        "--count", "-c",
        required=True,
        type=int
    )
    return parser.parse_args()


def main():

    args = parsearg()
    dbclient = MongoClient()
    db = dbclient.get_database(name='ca-repo-list-test-a')
    collection = db.get_collection('big-repo-list')

    # "Constants" that we need
    KEY_FILE = "keys.json"
    LANGUAGES = ["python"]

    # Configure the logging
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format='L %(asctime)s %(message)s',
        datefmt='%Y-%m-%d-%H-%M-%S'
    )

    with open(KEY_FILE, 'r') as key_file:
        KEYS = json.load(key_file)

    if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
        print("Please add your GitHub Client ID and Client Secret to keys.json")
        return

    def handle_repo_item(repo_obj):
        logging.info(
            "URL: {}\nNAME: {}".format(
                repo_obj["clone_url"],
                repo_obj["name"]
            )
        )
        print("Got repo:", repo_obj["name"])
        new_item = copy.deepcopy(itemtemplate)
        new_item["name"] = repo_obj["name"]
        new_item["url"] = repo_obj["clone_url"]
        new_item["search_result_item"] = repo_obj

        # push to mongo
        collection.insert_one(new_item)

    scraper = PythonScraper(KEYS)

    scraper.getTopRepos(args.language, args.count, handle_repo_item)


if __name__ == "__main__":
    main()
