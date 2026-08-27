# pythonProject1

Playwright + pytest UI/API test automation for the Ualand auction platform (QA environment).

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

Test environment URLs, credentials, and shared payloads (e.g. `BASE_URL`, `USER_NAME_*`, `CSP_PAYLOAD`) live in `config.py`.

## Running tests

```bash
pytest
```

`pytest.ini` runs headed against Chromium by default. Uncomment the `addopts` line for screenshots/video/trace capture and an HTML report on failure.

## Structure

- `pages/` — page objects (login, base page/bid, CSP creation, admin bid approval)
- `api/` — API helpers (e.g. auth)
- `tests/` — test suites; `tests/csp/` covers the CSP auction flow (create → bid → two bids → admin approve), ordered via `conftest.py`
- `utils/` — shared test utilities (e.g. date generation)
- `test_data/` — fixture files used by tests
- `specs/` — test plans
- `conftest.py` — shared fixtures and pytest hooks, including a fixture that neutralizes promo dialogs/toasts that can intercept clicks during tests
