## Testing

After starting the application, use the following steps to check its functionality:

1. Open http://127.0.0.1:8000 in your browser.
2. Confirm that the bookstore inventory is displayed.
3. Use the search box to search for a book by title or author.
4. Add a book to the shopping cart.
5. Try an invalid quantity, such as 0.
6. Try submitting an order with an empty cart.
7. Submit a valid order using customer name, email, and phone.
8. Confirm that a successful order message is displayed.
9. Check `data/orders.json` to verify that the order was saved.

The application should display clear error messages for invalid input and should not crash.
