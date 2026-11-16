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

### Runtime Test Execution

The following runtime tests were performed:

| Test Case | Result |
|---|---|
| Empty cart submission | Pass |
| Invalid customer email | Pass |
| Invalid phone number | Pass |
| Zero quantity | Pass |
| Quantity exceeding available stock | Pass |
| Valid order submission | Pass |
| Long search input | Pass – Application did not crash |

### Testing Notes

The application handled the tested invalid inputs without crashing. Search functionality recovered after unusual input, and a valid order was successfully submitted.

Repeated book IDs exceeding available stock were reviewed in source code but were not separately verified through runtime testing.

### Limitations

Authentication, file uploads, and payment integration are not implemented in the current application and were not tested.
