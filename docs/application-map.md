
# Paper Trail Books – Application and Attack Surface Map

## 1. Application Overview

Paper Trail Books is a small independent bookstore web application.

Customers can:
- View the book collection.
- Search for books, authors and categories.
- Select book quantities.
- Add books to a shopping cart.
- Remove books from the cart.
- Submit an order through checkout.

The application uses:
- Python standard library HTTP server for the backend.
- HTML and CSS for the interface.
- JavaScript for search, cart and checkout interactions.
- JSON files for inventory and order storage.

## 2. Application Pages and Sections

### 2.1 Home / Book Listing

**Status:** Implemented

**Route:** GET /

**Inputs:**
- Search keyword.
- Book quantity.
- Add-to-cart action.

**Outputs:**
- Book title.
- Author.
- Category.
- Price.
- Available stock.
- Book quantity controls.

### 2.2 Book Details

**Status:** Not implemented as a separate page.

Book information is displayed directly inside the book listing cards.

### 2.3 Search

**Status:** Implemented on the home page.

**Inputs:**
- Search keyword.

**Processing:**
- JavaScript reads the search input.
- It compares the keyword against the text of each book card.
- Non-matching cards are hidden.

**Outputs:**
- Matching book cards.
- No explicit message when no results are found.

### 2.4 Shopping Cart

**Status:** Implemented on the home page.

**Inputs:**
- Book ID from the selected book card.
- Quantity.
- Add-to-cart action.
- Remove-item action.

**Processing:**
- JavaScript stores cart items in a Map.
- It calculates item subtotals and the cart total.

**Outputs:**
- Selected books.
- Item quantities.
- Subtotals.
- Cart total.
- Empty-cart message.

### 2.5 Checkout

**Status:** Implemented.

**Inputs:**
- Customer name.
- Email address.
- Phone number.
- Book IDs and quantities from the cart.

**Processing:**
- JavaScript collects the checkout details.
- It sends the order to the backend using POST /order.

**Outputs:**
- Order confirmation.
- Order total.
- Validation or error messages.

## 3. Backend Routes and Endpoints

### GET /

- Loads the bookstore home page.
- Reads book inventory from data/books.json.
- Generates book listing cards.
- Returns the HTML page.

### GET /static/styles.css

- Serves the application stylesheet.

### GET /static/app.js

- Serves the application JavaScript.

### POST /order

**Purpose:** Receives and processes customer orders.

**Inputs:**
- name
- email
- phone
- items

**Backend processing:**
- Checks request size.
- Validates customer information.
- Checks the cart structure.
- Validates book IDs and quantities.
- Checks available stock.
- Calculates order totals on the server.
- Updates inventory.
- Saves the order.

**Outputs:**
- JSON success response.
- Order confirmation and total.
- JSON error response when validation fails.

Unknown routes return a 404 response.

## 4. Entry Points and Attack Surface

The main user-controlled entry points are:

| Entry Point | Input | Location |
|---|---|---|
| Search box | Search keyword | Frontend |
| Quantity input | Book quantity | Frontend |
| Add to Cart | Book ID and quantity | Frontend |
| Remove from Cart | Selected book ID | Frontend |
| Checkout form | Name, email, phone | Frontend |
| POST /order | Customer details and cart items | Backend |

The backend also receives HTTP request data and URL paths.

## 5. Data Storage

### data/books.json

Stores:
- Book ID.
- Title.
- Author.
- Category.
- Price.
- Stock.

### data/orders.json

Stores:
- Customer information.
- Ordered book details.
- Quantities.
- Unit prices.
- Subtotals.
- Order total.
- Order creation time.

## 6. Security Controls Observed in the Code

- HTML escaping is used when displaying book titles, authors and categories.
- JavaScript validates selected quantities before adding them to the cart.
- Backend validates customer information and order items.
- Backend checks book IDs and available stock.
- Order totals are calculated by the backend.
- Request size is limited to 10,000 bytes.
- Static file access is restricted to an allowlist.
- X-Content-Type-Options and Content-Security-Policy headers are set.

These are observed security controls, not proof that the application is completely secure.

## 7. Features Not Implemented

- Login and authentication.
- Separate book detail pages.
- File upload functionality.
- Customer account management.
- Public API documentation.

## 8. Application Data Flow

1. Customer opens the home page.
2. Backend loads inventory from books.json.
3. Customer searches for books and selects quantities.
4. JavaScript manages the shopping cart.
5. Customer enters checkout information.
6. JavaScript sends an order request to POST /order.
7. Backend validates the request and calculates the total.
8. Backend updates books.json and saves the order in orders.json.
9. Backend returns a success or error response.

## 9. Security Assessment Focus

The following areas should be reviewed during authorized security testing:

- Input validation.
- Client-side and server-side validation differences.
- Book ID and quantity handling.
- Order total calculation.
- Stock management.
- Request size handling.
- Error handling.
- Data storage and output handling.

Further testing is required before confirming any vulnerability.
