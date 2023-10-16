import time
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from constants import want_to_read_url, libraries
from models.Book import Book

if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument("--headless=new")
    d = webdriver.Chrome(options)

    print("Getting want to read titles")

    d.get(want_to_read_url)
    time.sleep(1)

    soup = BeautifulSoup(d.page_source, "html.parser")

    wtr_books = []
    book_container_elements = soup.css.select("div.flex.flex-col.justify-center")
    for book_container_element in book_container_elements:
        title_element = book_container_element.css.select_one("a.font-semibold.text-lg > span:not(.text-xs)")
        author_element = book_container_element.css.select_one("span > span > a.items-center > span")

        book = Book(title_element.text)

        if author_element is not None:
            book.author = author_element.text

        wtr_books.append(book)

    print(f"Found {len(wtr_books)} want to read titles")

    all_matches = {}

    for book in wtr_books:
        print(f"Checking availability for {book.title}")
        matching_libraries = []

        for library in libraries:
            print(f"Searching {library.name}")
            url = library.base_url + urllib.parse.urlencode(
                {"query": (book.title + " " + book.author) if book.author is not None else book.title})
            d.get(url)

            soup = BeautifulSoup(d.page_source, "html.parser")

            search_match_elements = soup.css.select(".TitleInfo > .title-name > a")
            search_matches = list(map(lambda e: e.text.strip(), search_match_elements))

            if book.title in search_matches:
                print(f"Potential match for {book.title} found at {library.name}")
                matching_libraries.append(library.name)

        all_matches[book.title] = matching_libraries

    print("Results:")

    for title in all_matches:
        if len(all_matches[title]) > 0:
            print(f"{title}: {all_matches[title]}")
