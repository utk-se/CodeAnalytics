import requests


class PythonScraper:
    def getTopRepos(language, number):
        links = []
        num_pages = int(number / 100)
        for i in range(0, num_pages):
            r = requests.get("https://api.github.com/search/repositories?q=language:{}&sort=stars&order=desc&per_page={}&page={}".format(language, number, i))
            if r.status_code != 200:
                print("WARNING: Slow down your requests!!")
                return None
            for obj in r.json()["items"]:
                links.append(obj["html_url"])
        return links

def main():
    arr = PythonScraper.getTopRepos("python", 1000)

    if arr is None:
        return

    for link in arr:
        print(link)

if __name__ == "__main__":
    main()