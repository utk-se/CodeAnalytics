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

def printfiles(lfiles):
        for lfile in lfiles:
            print("File: {}".format(lfile.filename))
            for func in lfile.function_list:
                print("     Function Name: {}".format(func.long_name))
                print("         Length: {}".format(func.length))
                print("         Start: {}".format(func.start_line))
                print("         Ends: {}".format(func.start_line + func.length - 1))

def main():

    parser = parsearg()

    # "Constants" that we need
    KEY_FILE = "keys.json"
    DATA_FILE=  "data.json"
    REPOS_DIR = "repos/"
    NUM_TO_SCRAPE = 10
    LANGUAGES = ["python"]

    # Configure the logging
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format='L %(asctime)s %(message)s',
        datefmt='%Y-%m-%d-%H-%M-%S'
    )

    # If we want to scrape
    if(parser.scrape):
        with open(KEY_FILE, 'r') as key_file:
            KEYS = json.load(key_file)

        if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
            print("Please add your GitHub Client ID and Client Secret to keys.json")
            return
            
        scraper = PythonScraper(KEYS)

        for language in LANGUAGES:
            scraper.getTopRepos(language, NUM_TO_SCRAPE)

        repos = scraper.getRepos()

        for language in repos:
            for repo in repos[language]:
                logging.info("{} {}".format(
                    language,
                    repos[language][repo]["html_url"]
                    ))

        # let's save what we have
        data = json.dumps(repos, indent=4)
        with open(DATA_FILE, 'w') as data_file:
            data_file.write(data)

    # If we want to analyze
    if(parser.analyze):
        lfiles = []
        extensions = ["py"]
        for language in repos:
            for repo in repos[language]:
                repo_name = repo.split('/')[1]
                repo_dest = REPOS_DIR + repo_name
                logging.info("Cloning {}".format(repo))
                Repo.clone_from(repos[language][repo]["html_url"], repo_dest)
                print("Analyzing {}".format(repo_dest))
                for (root, subdir, files) in os.walk(repo_dest):
                    for file in files:
                        fullpath = os.path.join(root, file)
                        if extensions:
                            for extension in extensions:
                                if fullpath.endswith(extension):
                                    lfile = lizard.analyze_file(fullpath)
                                    lfiles.append(lfile)
                        else:
                            lfile = lizard.analyze_file(fullpath)
                            lfiles.append(lfile)
                
                logging.info("Deleting {}".format(repo))
                shutil.rmtree(repo_dest, onerror=del_rw)
        printfiles(lfiles)

if __name__ == "__main__":
    main()
