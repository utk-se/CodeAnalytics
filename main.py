import json
from scraper import PythonScraper

def main():


    KEY_FILE = "keys.json"
    NUM_TO_SCRAPE = 500

    with open(KEY_FILE, 'r') as key_file:
        KEYS = json.load(key_file)


    if KEYS["client_id"] is "" or KEYS["client_secret"] is "":
        print("Please add your GitHub Client ID and Client Secret to keys.json")
        return

    scraper = PythonScraper(KEYS)

    scraper.getTopRepos("python", NUM_TO_SCRAPE)
    scraper.getTopRepos("java", NUM_TO_SCRAPE)
    scraper.getTopRepos("cpp", NUM_TO_SCRAPE)

    repos = scraper.getRepos()

if __name__ == "__main__":
    main()
