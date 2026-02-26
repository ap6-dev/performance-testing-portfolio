# Programming Portfolio: API Testing & Performance
This portfolio demonstrates expertise in API functional testing and API performance/load testing, showcasing:
- Automated functional tests with Python/pytest
- Parameterized, real-world API testing
- Load testing with k6, including public and authenticated endpoints
- Performance regression detection with thresholds
- Realistic traffic simulation and scenario design

# Portfolio Projects
## 1. API Function Tests (```api-functional-test```)
Purpose: validate REST API endpoints for correctness, readability, and expected responses.

**Key Features**
- Functional tests for multiple endpoints
- Parameterized input and expected output using JSON
- Automated checks for response codes, payload validation, and schema compliance
- Fast execution for CI integration

**Tools/Tech:** Python, pytest, JSON, CI-friendly

### Example of Test Cases:
| Endpoint      | Test              | Result   |
| ------------- | ----------------- | -------- |
| `/users`      | GET list of users | ✅ Passed |
| `/users/{user_id}` | GET single user   | ✅ Passed |
| `/posts`      | POST new post     | ✅ Passed |

**Portfolio Value:** \
Demonstrate ability to build a robust automated API testing framework capable of verifying correctness and supporting regression testing.

# 2. Load Tests with k6 (```load-tests-k6```)
Purpose: Simulate real-world API traffic to validate system performance, latency, and throughput.

**Key Features**
- Public (unauthenticated) and private (authenticated) scenarios
- Token generation via setup() and reuse for multiple virtual users
- Performance thresholds and automated regression gates
- Parameterized users from JSON file
- Scenario-based traffic: constant VUs and optional ramping profiles

**Tools/Tech:** Python, pytest, JSON, CI-friendly

### Results Snapshot:
| **Scenario** | **Endpoint** | **Requests** | **Success** | **Avg Latency (TTFB)** | **Avg Duration** |
| :--- | :---: | :--- | :---: | :--- | :---: |
| Public Users | GET https://quickpizza.grafana.com | 300 | 300 out of 300 | 16.76ms | 16.88ms |
| Authenticated Users | POST https://quickpizza.grafana.com/api/pizza | 1032 | 1032 out of 1032 | 145.16ms | 145.25ms |
| Login | POST https://quickpizza.grafana.com/api/users/token/login | 100 | 100 out of 100 | 16.02ms | 16.12ms |

**Performance Regression Gate:**
- p95 latency < 500ms
- Error rate < 1%

**Portfolio Value:** \
Demonstrates realistic load testing, performance monitoring, and the ability to implement automated performance regression testing.

---

# Skills Demonstrated Across Projcets
- Automated API testing (functional correctness, data validation, regression)
- Performance testing (load, latency, tokenized endpoints, public/private traffic)
- Scenario-based testing (VU profiles, ramping, constant load)
- Parameterization (user data, randomized payloads)
- CI/CD readiness (thresholds, regression gates, reusable configuration)
- Tools: Python, pytest, requests, k6, JSON

---

# How to Run
### API Functional Tests
```
cd api-functional-test
pytest
```
### k6 Load Tests
```
cd load-tests-k6
k6 run --summary-mode=full tests/api-test.js
```
