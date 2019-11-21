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


def printfilescsv(language, repo, lfiles):
    repo = repo.replace('/', '_')
    PATH = "./data/{}/{}.csv".format(language, repo)
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    with open(PATH, "w+") as csv_file:
        csv_file.write("File, Function, Length\n")
        for lfile in lfiles:
            for func in lfile.function_list:
                csv_file.write("{},\"{}\",{}\n".format(
                    lfile.filename, 
                    func.long_name.replace("\"", "\'"), 
                    func.length))
    

def main():

    parser = parsearg()

    # "Constants" that we need
    KEY_FILE = "keys.json"
    DATA_FILE=  "data.json"
    REPOS_DIR = "repos/"
    NUM_TO_SCRAPE = 1000
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
                    repos[language][repo]["html_url"]))

        # let's save what we have
        data = json.dumps(repos, indent=4)
        with open(DATA_FILE, 'w') as data_file:
            data_file.write(data)

    # If we want to analyze
    if parser.analyze:
        # If we are only analyzing
        if not parser.scrape:
            with open(DATA_FILE) as data_file:
                repos = json.load(data_file)
        extensions = ["py"]
        for language in repos:
            for repo in repos[language]:
                lfiles = []
                repo_name = repo.split('/')[1]
                repo_dest = REPOS_DIR + repo_name
                logging.info("Cloning {}".format(repo))
                r = Repo.clone_from(repos[language][repo]["html_url"], repo_dest)
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

                r.close()
                printfilescsv(language, repo, lfiles)
                logging.info("Deleting {}".format(repo))
                shutil.rmtree(repo_dest, onerror=del_rw)

if __name__ == "__main__":
    main()
