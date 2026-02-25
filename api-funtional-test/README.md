# API Functional Tests

A Python-based API functional and performance testing suite for REST endpoints, with integrated performance measurement and reporting. Designed to be CI/CD-ready.
---
## Disclaimer
This project uses JSONPlaceholder - a free fake online REST API - for testing purposes.
- All API calls are made to mock endpoints.
- No real user data is used or affected.
- This project is for educational and portfolio purposes only.
- Do not use this test suite against live production APIs without permission.
---
### File Structure
```
api-functional-tests/
├─ data/                    
│  └─ posts_test_data.json  # Data used for specific /posts tests
│  └─ users_test_data.json  # Data used for specific /users tests
├─ src/                     # Main source code (test helpers, utils, etc.)
│  └─ clients/
│     └─ api_client.py      # Main api client
│  └─ utils/
│     └─ performance.log    # Performance metrics printed here
│     └─ performance.py     # Performance measurement and summary printing
│     └─ validation.py      # Utility methods for tests, logging, and performance
├─ tests/                   # Test cases for your APIs
│     └─ test_framework.py  # Test cases for the api framework
│     └─ test_posts.py      # Test cases for /posts
│     └─ test_users.py      # Test cases for /users
├─ requirements.txt         # Python dependencies
└─ README.md                # Project documentation
```
---
### Features
- Functional testing of REST APIs using pytest
- Performance measurement of endpoints (avg, max, min timings)
- Color-coded summary highlighting slow endpoints
- CI/CD ready with GitHub Actions
- Optional log file saving for detailed performance reports
---
### Installation
```
git clone https://github.com/ap6-dev/performance-testing-portfolio.git
cd performance-testing-portfolio/api-functional-tests
```
### Running Tests
```
pytest --color=yes --capture=no
```
---
### Performance Summary
- Shows average, max, and min response times per endpoint.
- Can be configured to highlight endpoints exceeding a threshold (e.g., 50 ms).
Example
```
GET /users → avg: 23.2 ms | max: 26.0 ms | min: 20.0 ms
POST /users → avg: 57.7 ms | max: 60.0 ms | min: 54.8 ms  <-- slow, highlighted red
```
---
### CI/CD Integration
- The workflow is defined in ```.github/workflows/ci.yml```
- Automatically runs tests on push or pull requests
- Optionally saves performance logs as artifacts for later review
