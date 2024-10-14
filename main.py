import os
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from constants import libraries
from models.Book import Book

if __name__ == "__main__":
    load_dotenv()

    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options)

    print("Getting want to read titles")

    auth_header = {
        "authorization": os.environ["HARDCOVER_AUTH_TOKEN"]
    }

    transport = AIOHTTPTransport(url="https://hardcover-production.hasura.app/v1/graphql", headers=auth_header)
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql(
        """
        query GetWantToReadBooks {
            me {
                user_books(where: {status_id: {_eq: 1}}) {
                    book {
                        title
                        contributions {
                            author {
                                name
                            }
                        }
                    }
                }
            }
        }
    """
    )

    result = client.execute(query)

    wtr_books = []
    for item in result["me"][0]["user_books"]:
        title = item["book"]["title"]

        book = Book(title)

        if len(item["book"]["contributions"]) > 0:
            author = item["book"]["contributions"][0]["author"]["name"]
            book.author = author

        wtr_books.append(book)

    print(f"Found {len(wtr_books)} want to read titles")

    all_matches = {}

    for book in wtr_books:
        print(f"Checking availability for {book.title}")
        matching_libraries = []

        for library in libraries:
            print(f"Searching {library.name}")
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
                matching_libraries.append(library.name)

        if len(matching_libraries) > 0:
            all_matches[book.title] = matching_libraries

    print("Results:")
    for title in all_matches:
        print(f"{title}: {all_matches[title]}")
