import argparse
import json
import lizard
import logging
import os
import shutil
import stat

from scraper import PythonScraper
from git import Repo

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def parsearg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scrape", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    return parser.parse_args()


def main():

    parser = parsearg()

    # "Constants" that we need
    KEY_FILE = "keys.json"
    DATA_FILE=  "data.json"
    REPOS_DIR = "repos/"
    NUM_TO_SCRAPE = 10

    # Configure the logging
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format='L %(asctime)s %(message)s',
        datefmt='%m/%d/%Y %H:%M:%S'
    )

    # If we want to scrape
    if(parser.scrape):
        with open(KEY_FILE, 'r') as key_file:
            KEYS = json.load(key_file)

        if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
            print("Please add your GitHub Client ID and Client Secret to keys.json")
            return
            
        scraper = PythonScraper(KEYS)

        logging.info("Getting top {} repositories for languages".format(NUM_TO_SCRAPE))
        scraper.getTopRepos("python", NUM_TO_SCRAPE)
        # scraper.getTopRepos("java", NUM_TO_SCRAPE)
        # scraper.getTopRepos("cpp", NUM_TO_SCRAPE)

        repos = scraper.getRepos()

        # let's save what we have
        data = json.dumps(repos, indent=4)
        with open(DATA_FILE, 'w') as data_file:
            data_file.write(data)

    # If we want to analyze
    if(parser.analyze):
        for language in repos:
            for repo in repos[language]:
                repo_name = repo.split('/')[1]
                repo_dest = REPOS_DIR + repo_name
                logging.info("Cloning {}".format(repo))
                Repo.clone_from(repos[language][repo]["html_url"], repo_dest)
                # Run analysis here...
                logging.info("Deleting {}".format(repo))
                shutil.rmtree(repo_dest, onerror=del_rw)

if __name__ == "__main__":
    main()
