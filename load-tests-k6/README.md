# k6 API Load Testing Suite
Performance testing project using k6 to simulate real-world API traffic, including authenticated and unauthenticated users, with thresholds for automated performance regression detection.
---
## Note
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
│  └─ api_test.js/       # The main k6 test - Initializes user data, setup gets user login tokens, tests fetching data, login with credentials, token login/POST requests
├─ README.md/            # Project Documentation
├─ k6-config.js/         # k6 config file - API Url definition, testing scenarios defined, threshold reporting
├─ requirements.txt/     # Project dependencies
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
k6 run api_test.js
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
- Endpoint: https://quickpizza.grafana.com/api/users/token/login
- Purpose: Simulate users logging in with proper username and password
---
### Example Output Metrics
P95 Latency & HTTP Request Error Rate
```
THRESHOLDS 

http_req_duration
✓ 'p(95)<500' p(95)=328.23ms

http_req_failed
✓ 'rate<0.01' rate=0.00%
```
---
Main Testing Results
```
TOTAL RESULTS 

checks_total.......: 1431    35.079393/s
checks_succeeded...: 100.00% 1431 out of 1431
checks_failed......: 0.00%   0 out of 1431

✓ public status 200
✓ public response not empty
✓ private status 200
✓ login successful
```
---
k6 Testing Metrics
```
HTTP
http_req_duration..............: avg=120.78ms min=13.53ms med=100.42ms max=694.84ms p(90)=258.13ms p(95)=328.23ms
  { expected_response:true }...: avg=120.78ms min=13.53ms med=100.42ms max=694.84ms p(90)=258.13ms p(95)=328.23ms
http_req_failed................: 0.00%  0 out of 1282
http_reqs......................: 1282   31.426822/s

EXECUTION
iteration_duration.............: avg=355.89ms min=30.11ms med=163.35ms max=1.08s    p(90)=1.01s    p(95)=1.01s   
iterations.....................: 1281   31.402308/s
vus............................: 1      min=1         max=15
vus_max........................: 15     min=15        max=15

NETWORK
data_received..................: 1.7 MB 41 kB/s
data_sent......................: 286 kB 7.0 kB/s
```
