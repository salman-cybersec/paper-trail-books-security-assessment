
# Paper Trail Books – Application and Attack Surface Map

## 1. Home / Book Listing

**Status:** Implemented

**Inputs:**
- Search text
- Book quantity
- Add-to-cart action

**Outputs:**
- Book title
- Author name
- Category
- Price
- Available stock
- Matching book listings

## 2. Book Details

**Status:** Displayed within the book listing; no separate detail page.

**Inputs:**
- No separate user input

**Outputs:**
- Book title
- Author
- Category
- Price
- Stock availability

## 3. Search

**Status:** Implemented on the home page.

**Inputs:**
- Search keyword

**Outputs:**
- Matching book cards
- Non-matching cards are hidden
- No explicit message when no results are found

## 4. Shopping Cart

**Status:** Implemented on the home page.

**Inputs:**
- Book ID
- Quantity
- Remove-item action

**Outputs:**
- Selected books
- Item quantities
- Subtotals
- Cart total
- Empty-cart message

## 5. Checkout

**Status:** Implemented.

**Inputs:**
- Customer name
- Email address
- Phone number
- Book IDs and quantities

**Outputs:**
- Order confirmation
- Order total
- Validation or error messages

**Backend endpoint:** POST /order

## 6. Login / Authentication

**Status:** Not implemented.

**Inputs:** None.

**Outputs:** None.

## 7. File Upload

**Status:** Not implemented.

No customer-facing file upload functionality is available.

## 8. Attack Surface Summary

The main user interaction points are:
- Book search input
- Quantity input
- Shopping cart actions
- Checkout customer details
- POST /order endpoint

The application currently uses client-side JavaScript for search and cart interactions, and a Python backend for order processing.
