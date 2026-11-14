import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "books.json"

def load_books():
    with open(DATA_FILE, encoding="utf-8") as file:
        return json.load(file)

class BookstoreHandler(BaseHTTPRequestHandler):

    def send_page(self, content, status=200):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path)

        if path.path != "/":
            return self.send_page("<h1>404 - Page not found</h1>", 404)

        try:
            books = load_books()
            search = parse_qs(path.query).get("search", [""])[0]
            search = search.strip().lower()

            if len(search) > 100:
                return self.send_page("<h1>Search must be under 100 characters.</h1>", 400)

            filtered = [
                book for book in books
                if search in book["title"].lower()
                or search in book["author"].lower()
                or search in book["category"].lower()
            ]

            cards = ""
            for book in filtered:
                cards += f"""
                <article>
                    <h2>{book['title']}</h2>
                    <p>Author: {book['author']}</p>
                    <p>Category: {book['category']}</p>
                    <p>Price: Rs. {book['price']}</p>
                    <p>Stock: {book['stock']}</p>
                </article>
                """

            if not cards:
                cards = "<p>No matching books found.</p>"

            page = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Paper Trail Books</title>
                <link rel="stylesheet" href="/static/styles.css">
            </head>
            <body>
                <header><h1>Paper Trail Books</h1></header>
                <main>
                    <h2>Our Book Collection</h2>
                    <form method="GET">
                        <input name="search" maxlength="100"
                               placeholder="Search books or authors"
                               value="{search}">
                        <button type="submit">Search</button>
                    </form>
                    <section>{cards}</section>
                </main>
            </body>
            </html>
            """
            self.send_page(page)

        except (OSError, ValueError, KeyError, TypeError):
            self.send_page("<h1>Unable to load bookstore inventory.</h1>", 500)

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), BookstoreHandler)
    print("Paper Trail Books running at http://127.0.0.1:8000")
    server.serve_forever()
