
import json
import html
import re
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "books.json"
HOST = "127.0.0.1"
PORT = 8000


def load_books():
    if not DATA_FILE.exists():
        raise FileNotFoundError("Book inventory file is missing.")

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        books = json.load(file)

    if not isinstance(books, list):
        raise ValueError("Inventory must contain a list of books.")

    required = ["id", "title", "author", "category", "price", "stock"]

    for book in books:
        if not isinstance(book, dict):
            raise ValueError("Invalid book record found.")

        for field in required:
            if field not in book:
                raise ValueError(f"Book record is missing: {field}")

        if (
            isinstance(book["price"], bool)
            or not isinstance(book["price"], (int, float))
            or book["price"] <= 0
        ):
            raise ValueError("Book price must be greater than zero.")

        if (
            type(book["stock"]) is not int
            or book["stock"] < 0
        ):
            raise ValueError("Book stock cannot be negative.")

    return books


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


class BookstoreHandler(BaseHTTPRequestHandler):

    def send_response_body(
        self,
        content,
        status=200,
        content_type="text/html; charset=utf-8"
    ):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self'; script-src 'self'"
        )
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            try:
                books = load_books()
                cards = ""

                for book in books:
                    cards += f"""
                    <article class="book-card">
                        <h3>{html.escape(str(book['title']))}</h3>
                        <p>Author: {html.escape(str(book['author']))}</p>
                        <p>Category: {html.escape(str(book['category']))}</p>
                        <p>Price: PKR {book['price']}</p>
                        <p>Available: {book['stock']}</p>
                        <label>Quantity</label>
                        <input class="quantity" type="number" min="1"
                               max="{book['stock']}" value="1"
                               id="qty-{html.escape(str(book['id']))}">
                        <button class="add-cart"
                                data-id="{html.escape(str(book['id']))}">
                            Add to Cart
                        </button>
                    </article>
                    """

                page = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Paper Trail Books</title>
                    <link rel="stylesheet" href="/static/styles.css">
                    <script src="/static/app.js" defer></script>
                </head>
                <body>
                    <header>
                        <h1>Paper Trail Books</h1>
                        <p>Your independent bookstore</p>
                    </header>

                    <main>
                        <section>
                            <h2>Our Book Collection</h2>
                            <input id="search" type="search"
                                   placeholder="Search books, authors or categories">
                            <div class="book-grid">{cards}</div>
                        </section>

                        <section id="cart-section">
                            <h2>Shopping Cart</h2>
                            <div id="cart-items">Your cart is empty.</div>
                            <p id="cart-total">Total: PKR 0</p>
                        </section>

                        <section id="checkout-section">
                            <h2>Checkout</h2>
                            <form id="checkout-form">
                                <label for="customer-name">Full Name</label>
                                <input id="customer-name" name="name"
                                       type="text" maxlength="80" required>

                                <label for="customer-email">Email Address</label>
                                <input id="customer-email" name="email"
                                       type="email" maxlength="120" required>

                                <label for="customer-phone">Phone Number</label>
                                <input id="customer-phone" name="phone"
                                       type="tel" maxlength="20" required>

                                <button type="submit">Place Order</button>
                            </form>
                            <p id="checkout-message" role="status"></p>
                        </section>
                    </main>

                    <footer>
                        <p>Paper Trail Books - Independent Bookstore</p>
                    </footer>
                </body>
                </html>"""

                self.send_response_body(page)

            except (OSError, ValueError, KeyError, TypeError) as error:
                self.send_response_body(
                    f"<h1>Inventory Error</h1><p>{html.escape(str(error))}</p>",
                    500
                )

        elif path.startswith("/static/"):
            filename = path.removeprefix("/static/")
            allowed = {"styles.css", "app.js"}

            if filename not in allowed:
                self.send_response_body("File not found.", 404)
                return

            file_path = BASE_DIR / "static" / filename

            try:
                content = file_path.read_text(encoding="utf-8")
                content_type = (
                    "text/css; charset=utf-8"
                    if filename.endswith(".css")
                    else "application/javascript; charset=utf-8"
                )
                self.send_response_body(content, 200, content_type)

            except OSError:
                self.send_response_body("Static file not found.", 404)

        else:
            self.send_response_body("Page not found.", 404)

    def do_POST(self):
        if urlparse(self.path).path != "/order":
            self.send_response_body("Endpoint not found.", 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))

            if length <= 0 or length > 10000:
                raise ValueError("Invalid request size.")

            form = parse_qs(
                self.rfile.read(length).decode("utf-8"),
                keep_blank_values=True
            )

            def get_field(name):
                return form.get(name, [""])[0].strip()

            name = get_field("name")
            email = get_field("email")
            phone = get_field("phone")
            items = json.loads(get_field("items"))

            if not name or len(name) > 80:
                raise ValueError("Enter a valid customer name.")

            if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]{1,79}", name):
                raise ValueError("Name contains invalid characters.")

            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValueError("Enter a valid email address.")

            if not re.fullmatch(r"[0-9+() -]{7,20}", phone):
                raise ValueError("Enter a valid phone number.")

            if not isinstance(items, list) or not items or len(items) > 20:
                raise ValueError("Your cart is empty or invalid.")

            books = load_books()

            # Combine repeated entries for the same book.
            requested_quantities = {}

            for item in items:
                if not isinstance(item, dict):
                    raise ValueError("Invalid cart item.")

                book_id = item.get("id")
                quantity = item.get("quantity")

                if type(quantity) is not int or quantity < 1 or quantity > 20:
                    raise ValueError("Book quantity must be between 1 and 20.")

                book = next(
                    (b for b in books if str(b["id"]) == str(book_id)),
                    None
                )

                if book is None:
                    raise ValueError("Selected book was not found.")

                normalized_id = str(book["id"])
                requested_quantities[normalized_id] = (
                    requested_quantities.get(normalized_id, 0) + quantity
                )

                if requested_quantities[normalized_id] > 20:
                    raise ValueError(
                        "Total quantity for one book cannot exceed 20."
                    )

            order_items = []
            total = 0

            # Validate combined quantities against actual stock.
            for book_id, quantity in requested_quantities.items():
                book = next(
                    b for b in books if str(b["id"]) == book_id
                )

                if quantity > book["stock"]:
                    raise ValueError(
                        f"Not enough stock for {book['title']}."
                    )

                subtotal = book["price"] * quantity
                total += subtotal

                order_items.append({
                    "id": book["id"],
                    "title": book["title"],
                    "quantity": quantity,
                    "unit_price": book["price"],
                    "subtotal": subtotal
                })

            # Prepare the updated inventory.
            updated_books = [dict(book) for book in books]

            for item in order_items:
                book = next(
                    b for b in updated_books if b["id"] == item["id"]
                )
                book["stock"] -= item["quantity"]

            order = {
                "customer": {
                    "name": name,
                    "email": email,
                    "phone": phone
                },
                "items": order_items,
                "total": total,
                "created_at": datetime.now().isoformat(timespec="seconds")
            }

            orders_file = BASE_DIR / "data" / "orders.json"

            if orders_file.exists():
                with open(orders_file, "r", encoding="utf-8") as file:
                    orders = json.load(file)
            else:
                orders = []

            if not isinstance(orders, list):
                raise ValueError("Order storage must contain a list.")

            orders.append(order)

            # Save inventory and order records.
            with open(orders_file, "w", encoding="utf-8") as file:
                json.dump(orders, file, indent=4, ensure_ascii=False)

            save_books(updated_books)

            self.send_response_body(
                json.dumps({
                    "success": True,
                    "message": "Your order has been placed successfully.",
                    "total": total
                }),
                200,
                "application/json"
            )

        except (
            ValueError,
            TypeError,
            KeyError,
            OSError,
            json.JSONDecodeError
        ) as error:
            self.send_response_body(
                json.dumps({
                    "success": False,
                    "message": str(error)
                }),
                400,
                "application/json"
            )

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), BookstoreHandler)
    print(f"Paper Trail Books running at http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
