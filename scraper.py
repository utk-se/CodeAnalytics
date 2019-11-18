import requests
import time

class PythonScraper:

    def __init__(self, keys):
        self.repos = {}
        self.keys = keys

    def getRepos(self):
        return self.repos

    def getTopRepos(self, language, number):
        # See if language is already there
        if language not in self.repos:
            self.repos[language] = {}

        # See how many pages we are going to need; we can only get 100 at most
        # from each request
        num_pages = number // 100
        # Total number of repos we want:
        num_repos = number
        URL = "https://api.github.com/search/repositories?q=language:{}&sort=stars&order=desc&per_page={}&page={}&client_id={}&client_secret={}"
        for i in range(0, num_pages+1):
            while True:
                if num_repos > 100:
                    number = 100
                else:
                    number = num_repos                  
                r = requests.get(URL.format(
                    language,
                    number,
                    i+1,
                    self.keys["client_id"],
                    self.keys["client_secret"]
                ))
                if r.status_code == 200:
                    break
                else:
                    print("Got throttled! Sleeping for 10 seconds... i = {}, language = {}".format(i, language))
                    time.sleep(10)
            for obj in r.json()["items"]:
                self.repos[language][obj["full_name"]] = obj
            
            num_repos = num_repos - 100
