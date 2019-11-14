import json
import requests
import time

class PythonScraper:

    def __init__(self, keys):
        self.links = {}
        self.keys = keys

    def getLinks(self):
        return self.links

    def getTopRepos(self, language, number):
        num_pages = number // 100
        URL = "https://api.github.com/search/repositories?q=language:{}&sort=stars&order=desc&per_page={}&page={}&client_id={}&client_secret={}"
        for i in range(0, num_pages):
            while True:
                r = requests.get(URL.format(
                    language,
                    number,
                    i,
                    self.keys["client_id"],
                    self.keys["client_secret"]
                ))
                if r.status_code == 200:
                    break
                else:
                    print("Got throttled! Sleeping for 10 seconds... i = {}, language = {}".format(i, language))
                    time.sleep(10)
            for obj in r.json()["items"]:
                self.links[obj["full_name"]] = obj

def main():


    KEY_FILE = "keys.json"
    NUM_TO_SCRAPE = 500

    with open(KEY_FILE, 'r') as key_file:
        KEYS = json.load(key_file)


    if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
        print("Please add your GitHub Client ID and Client Secret to keys.json")

    scraper = PythonScraper(KEYS)

    try:
        scraper.getTopRepos("python", NUM_TO_SCRAPE)
    except Exception as error:
        print(error)
        return

    try:
        scraper.getTopRepos("cpp", NUM_TO_SCRAPE)
    except Exception as error:
        print(error)
        return

    try:
        scraper.getTopRepos("java", NUM_TO_SCRAPE)
    except Exception as error:
        print(error)
        return

    try:
        scraper.getTopRepos("javascript", NUM_TO_SCRAPE)
    except Exception as error:
        print(error)
        return

    repos = scraper.getLinks()

    for repo in repos:
        print("Language: {}, Repo: {}".format(repos[repo]["language"], repo))

if __name__ == "__main__":
    main()
