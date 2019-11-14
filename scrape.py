import requests


class PythonScraper:

    def __init__(self):
        self.links = []

    def getLinks(self):
        return self.links

    def getTopRepos(self, language, number):
        num_pages = int(number / 100)
        for i in range(0, num_pages):
            r = requests.get("https://api.github.com/search/repositories?q=language:{}&sort=stars&order=desc&per_page={}&page={}".format(language, number, i))
            if r.status_code != 200:
                raise Exception("WARNING: Please slow down your requests!")
            for obj in r.json()["items"]:
                self.links.append(obj["html_url"])

def main():

    scraper = PythonScraper()

    try:
        scraper.getTopRepos("python", 1000)
    except Exception as error:
        print(error)
        return
        
    links = scraper.getLinks()

    if links is None:
        return

    for link in links:
        print(link)

if __name__ == "__main__":
    main()