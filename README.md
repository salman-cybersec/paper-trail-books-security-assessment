
# Paper Trail Books – Security Assessment Project

## Project Overview
A small independent bookstore web application developed for the Paper Trail Books security assessment project.

The project demonstrates a documented security testing scope, rules of engagement, realistic bookstore inventory, input validation, and basic order processing.

## Technology
- Python 3
- HTML
- CSS
- JavaScript
- JSON

## Project Structure
```text
paper-trail-books-security-assessment/
├── app.py
├── README.md
├── data/
│   ├── books.json
│   └── orders.json
├── docs/
│   ├── scope.md
│   ├── rules-of-engagement.md
│   ├── testing-notes.md
│   └── handover.md
└── static/
    ├── app.js
    └── styles.css
```

## Requirements
- Python 3.9 or later
- No external Python packages required

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project directory.
3. Run:

```bash
python app.py
```

4. Open this address in your browser:

```text
http://127.0.0.1:8000
```

## Application Features
- View bookstore inventory
- Search books by title, author, or category
- Add books to shopping cart
- Calculate order totals
- Submit customer orders
- Validate customer information
- Check available stock
- Save orders in JSON format
- Display clear error messages

## Security Testing Scope

Selected legal practice target:

PortSwigger Web Security Academy

Lab:
SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

Official lab:
https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

The lab selection, authorization boundaries, and testing restrictions are documented in:

- `docs/scope.md`
- `docs/rules-of-engagement.md`

## Testing

The bookstore application was manually tested for:

- Successful order submission
- Empty cart handling
- Invalid email input
- Stock quantity validation

PortSwigger lab completion and evidence are recorded in `docs/testing-notes.md`.

## Limitations
- No real payment gateway integration
- No customer account or authentication system
- JSON files are used for inventory and order storage
- Intended for local demonstration and educational security testing

## Legal Notice
Security testing must only be performed on the selected authorized PortSwigger Academy lab, a personal lab, or systems with written permission.
