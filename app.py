import json
import html
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "books.json"
STATIC_DIR = BASE_DIR / "static"


def load_books():
    with open(DATA_FILE, encoding="utf-8") as file:
        books = json.load(file)

    if not isinstance(books, list):
        raise ValueError("Invalid inventory format")

    for book in books:
        if not all(key in book for key in (
            "id", "title", "author", "category", "price", "stock"
        )):
            raise ValueError("Invalid book record")

        if not isinstance(book["price"], (int, float)) or book["price"] < 0:
            raise ValueError("Invalid book price")

        if not isinstance(book["stock"], int) or book["stock"] < 0:
            raise ValueError("Invalid stock value")

    return books


class BookstoreHandler(BaseHTTPRequestHandler):

    def send_page(self, content, status=200):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path)

        if path.path.startswith("/static/"):
            filename = path.path.removeprefix("/static/")
            if filename not in {"styles.css", "app.js"}:
                return self.send_page("Not found", 404)

            file_path = STATIC_DIR / filename

            if not file_path.is_file():
                return self.send_page("Static file not found", 404)

            content_type = mimetypes.guess_type(filename)[0]
            data = file_path.read_bytes()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)
            return

        if path.path != "/":
            return self.send_page("<h1>404 - Page not found</h1>", 404)

        try:
            books = load_books()
            search = parse_qs(path.query).get("search", [""])[0].strip()

            if len(search) > 100:
                return self.send_page(
                    "<h1>Search must be under 100 characters.</h1>", 400
                )

            filtered = [
                book for book in books
                if search.casefold() in book["title"].casefold()
                or search.casefold() in book["author"].casefold()
                or search.casefold() in book["category"].casefold()
            ]

            cards = ""

            for book in filtered:
                title = html.escape(str(book["title"]))
                author = html.escape(str(book["author"]))
                category = html.escape(str(book["category"]))

                cards += f"""
                <article>
                    <h2>{title}</h2>
                    <p>Author: {author}</p>
                    <p>Category: {category}</p>
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
                               value="{html.escape(search, quote=True)}">
                        <button type="submit">Search</button>
                    </form>
                    <section>{cards}</section>
                </main>
            </body>
            </html>
            """

            self.send_page(page)

        except (OSError, ValueError, KeyError, TypeError):
            self.send_page(
                "<h1>Unable to load bookstore inventory.</h1>", 500
            )

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), BookstoreHandler)
    print("Paper Trail Books running at http://127.0.0.1:8000")
    server.serve_forever()
