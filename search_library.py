from urllib.parse import urlencode

from bs4 import BeautifulSoup

from models.Book import Book
from models.Library import Library

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

options = ChromeOptions()
options.add_argument("--headless=new")


def search_library(book: Book, library: Library):
    d = webdriver.Chrome(options)

    print(f"Searching {library.name} for {str(book)}")
    url = library.base_url + urlencode(
        {
            "query": (book.title + " " + book.author)
            if book.author is not None
            else book.title
        }
    )
    d.get(url)

    soup = BeautifulSoup(d.page_source, "html.parser")

    search_match_elements = soup.css.select(".TitleInfo > .title-name > a")
    search_matches = list(map(lambda e: e.text.strip(), search_match_elements))

    if book.title in search_matches:
        print(f"Potential match for {book.title} found at {library.name}")
        return book.title, library.name

    return False
