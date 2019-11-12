import requests


class PythonScraper:

    def getTopRepos(language, number):
        r = requests.get("https://api.github.com/search/repositories?q=language:{}&sort=stars&order=desc&per_page={}".format(language, number))
        return r.json()


obj = PythonScraper.getTopRepos("python", 100)
