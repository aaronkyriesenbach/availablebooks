from urllib.parse import urlencode

from bs4 import BeautifulSoup
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

from time import time

import multiprocessing

from constants import libraries
from models.Book import Book
from search_library import search_library

# Hardcover API key goes in secrets.py, format:
# auth_header={"authorization": "token_here"}
from secrets import auth_header

if __name__ == "__main__":
    start_time = time()

    options = ChromeOptions()
    options.add_argument("--headless=new")
    d = webdriver.Chrome(options)

    print("Getting want to read titles")

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

    requests = []
    for b in wtr_books:
        for l in libraries:
            requests.append((b, l))

    pool = multiprocessing.Pool()
    outputs = pool.starmap(search_library, requests)

    for val in outputs:
        if val:
            book_title = val[0]
            library = val[1]

            all_matches[book_title] = [library] + all_matches[book_title] if book_title in all_matches else [library]

    print("Results:")
    for title in all_matches:
        print(f"{title}: {all_matches[title]}")

    end_time = time()
    print(f"Total time: {end_time - start_time}")
