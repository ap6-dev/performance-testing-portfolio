# k6 API Load Testing Suite
Performance testing project using k6 to simulate real-world API traffic, including authenticated and unauthenticated users, with thresholds for automated performance regression detection.
---
## Project Note
This project uses the [official k6 testing api](https://quickpizza.grafana.com) as an example of integration with an API. Some responses are specific to this API, so respones from a real,
in profuction API may require more thorough validation.
- All API calls are made to mock endpoints.
- No real user data is used or affected.
- This project is for educational and portfolio purposes only.
- Do not use this test suite against live production APIs without permission.
---
### File Structure
```
load-tests-k6/
├─ data/                    
│  └─ users.json         # Mock user login data (more users can be added for parametrized testing)
├─ tests/                
│  └─ api_test.js        # The main k6 test - Initializes user data, setup gets user login tokens, tests fetching data, login with credentials, token login/POST requests
├─ README.md             # Project Documentation
├─ k6-config.js          # k6 config file - API Url definition, testing scenarios defined, threshold reporting
├─ requirements.txt      # Project dependencies
```
---
### Features
- API load testing with k6
- Parameterized test users via JSON
- Auth token generation in setup()
- Multiple traffic scenarios (public vs authenticated)
- Performance thresholds (p95 latency & error rate)
- Clean lifecycle usage (init → setup → VU → teardown)
---
### Installation
```
git clone https://github.com/ap6-dev/performance-testing-portfolio.git
cd performance-testing-portfolio/load-tests-k6/tests
```
### Running Tests
```
k6 run --summary-mode=full api_test.js
```
---
### Test Scenarios
1. Public Users (Unauthenticated) - ```public_flow()```
- Endpoint: GET https://quickpizza.grafana.com
- Purpose: Simulate anonymous browsing traffic
2. Authenticated Users - ```private_flow()```
- Login performed in ```setup()```
- Token reused by VUs
- Endpoint: POST https://quickpizza.grafana.com/api/pizza
- Purpose: Simulate logged-in user activity
3. Login - ```login()```
- Endpoint: POST https://quickpizza.grafana.com/api/users/token/login
- Purpose: Simulate users logging in with proper username and password
---
## Example Results
The following results were obtained from a 30-second load test using:
- 5 VUs (public users - constant load profile)
- 5 VUs (authenticated users - constant load profile)
- 0→5→0 VUs (login - ramping load profile)
- Token reuse from ```setup()```
### Request Metrics

| **Metric** | **Value** |
| :--- | :---: |
| Total Requests | 1231 |
| Requests/sec (RPS) | ~40/s |
| Iterations | 1230 |
| Checks passed | 1380 |
### Latency
| **Metric** | **Value** |
| :--- | :---: |
| Average | 125.1ms |
| Median (p50) | 105.18ms |
| p(90) | 259.6ms |
| p(95) | 330.91ms |
| Max | 711.03ms |

Threshold: p95 < 500ms
### Error Rate
| **Metric** | **Value** |
| :--- | :---: |
| hhtp_req_failed | 0 out of 1231 |

### Scenario Breakdown
| **Scenario** | **Endpoint** | **Requests** | **Success** | **Avg Latency (TTFB)** | **Avg Duration** |
| :--- | :---: | :--- | :---: | :--- | :---: |
| Public Users | GET https://quickpizza.grafana.com | 300 | 300 out of 300 | 16.76ms | 16.88ms |
| Authenticated Users | POST https://quickpizza.grafana.com/api/pizza | 1032 | 1032 out of 1032 | 145.16ms | 145.25ms |
| Login | POST https://quickpizza.grafana.com/api/users/token/login | 100 | 100 out of 100 | 16.02ms | 16.12ms |

### Observations
- Public GET requests were very fast (avg. 16.88ms) with no failures.
- Authenticated POST requests had higher latency (~145ms) due to auth and server processing, but all requests succeeded.
- Login requests were fast (~16ms) and all succeeded, showing token generation is performant under load.
- Overall, all requests stayed within acceptable thresholds, making this test suitable as a performance regression gate.

### Performance Regression Gate
This test is designed to fail automatically if:
- p95 latency exceeds 500ms
- Error rate exceeds 1%
> This enables use in CI/CD as a performance regression test.

