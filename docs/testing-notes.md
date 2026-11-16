## Task 2 – Application Security Review

### Static Code Review

The application source code was reviewed to identify user inputs, backend routes, validation controls, and data storage.

The following controls were identified:

- Customer name, email, and phone validation.
- Empty and invalid cart rejection.
- Book ID validation.
- Quantity and stock validation.
- Server-side order total calculation.
- Request body size limit.
- HTML escaping for book information.
- Allowlisted static file access.
- Duplicate book entries are combined before stock validation.

### Test Execution Status

The above controls have been reviewed in source code. Runtime testing of these cases is still pending.

Planned test cases:

1. Empty cart submission.
2. Invalid customer email.
3. Invalid phone number.
4. Zero or negative quantity.
5. Quantity exceeding available stock.
6. Repeated book IDs exceeding available stock.
7. Valid order submission.
