## HeroAccounts Delivery Checklist

- [x] Backend OCR pipeline converts uploaded PDFs into cleaned raw text.
- [x] RegexCleaner normalizes text prior to NLP extraction.
- [x] Call_pythonOCR + pythonOCR classes encapsulate OCR workflow.
- [x] NLP engine extracts structured metadata for amount/date/vendor/etc.
- [x] Parsed fields validated against company policy rules.
- [x] Claim matched to employee budgets/travel requests (stub + hooks).
- [x] Receipts persisted in PostgreSQL (`hero_db`) with statuses.
- [x] Text chunks & metadata stored inside Chroma vector DB.
- [x] Approval workflow auto-assigns manager chain and notifies via email.
- [x] Status transitions maintained (`Submitted → Review → Approved → Reimbursed`).
- [x] Receipt entries appended to Excel ledger via `openpyxl`.
- [x] API returns structured JSON payload for frontend usage.
- [x] React app uses Axios and reusable components for upload/status grid.
- [x] Excel-style table visible on right side of upload page with live data.
- [x] Global styling centralized in `style.css` for professional UI.

