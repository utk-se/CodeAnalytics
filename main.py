import json
import os
import shutil

from scraper import PythonScraper
from git import Repo

def main():


    KEY_FILE = "keys.json"
    REPOS_DIR = "repos/"
    NUM_TO_SCRAPE = 10

    with open(KEY_FILE, 'r') as key_file:
        KEYS = json.load(key_file)


    if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
        print("Please add your GitHub Client ID and Client Secret to keys.json")
        return

    scraper = PythonScraper(KEYS)

    scraper.getTopRepos("python", NUM_TO_SCRAPE)
    # scraper.getTopRepos("java", NUM_TO_SCRAPE)
    # scraper.getTopRepos("cpp", NUM_TO_SCRAPE)

    repos = scraper.getRepos()

    for language in repos:
        for repo in repos[language]:
            repo_name = repo.split('/')[1]
            repo_dest = REPOS_DIR + repo_name
            print("Cloning {}".format(repo))
            Repo.clone_from(repos[language][repo]["html_url"], repo_dest)
            # Run analysis here...
            print("Deleting {}".format(repo))
            shutil.rmtree(repo_dest)

if __name__ == "__main__":
    main()
