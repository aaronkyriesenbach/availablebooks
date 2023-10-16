import time
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from constants import libraries, want_to_read_url

if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument("--headless=new")
    d = webdriver.Chrome(options)

    print("Getting want to read titles")

    d.get(want_to_read_url)
    time.sleep(1)

    soup = BeautifulSoup(d.page_source, "html.parser")

    wtr_match_elements = soup.css.select("a.font-semibold.text-lg > span:not(.text-xs)")
    wtr_titles = list(map(lambda e: e.text, wtr_match_elements))

    print(f"Found {len(wtr_titles)} want to read titles")

    all_matches = {}

    for title in wtr_titles:
        print(f"Checking availability for {title}")
        matching_libraries = []

        for library in libraries:
            print(f"Searching {library.name}")
            url = library.base_url + urllib.parse.urlencode({"query": title})
            d.get(url)

            soup = BeautifulSoup(d.page_source, "html.parser")

            search_match_elements = soup.css.select(".TitleInfo > .title-name > a")
            search_matches = list(map(lambda e: e.text.strip(), search_match_elements))

            if title in search_matches:
                print(f"Potential match for {title} found at {library.name}")
                matching_libraries.append(library.name)

        all_matches[title] = matching_libraries

    print("Results:")

    for title in all_matches:
        if len(all_matches[title]) > 0:
            print(f"{title}: {all_matches[title]}")
