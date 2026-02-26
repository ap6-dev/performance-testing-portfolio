//Official k6 testing api
export const BASE_URL = 'https://quickpizza.grafana.com';

//Init context: define k6 options
export const options = {
    scenarios: {
        public_users_scenario: {
                executor: 'constant-vus',
                vus: 5,
                duration: '30s',
                exec: 'public_flow'
            },
        authenticated_users_scenario: {
            executor: 'constant-vus',
            vus: 5,
            duration: '30s',
            exec: 'private_flow'
        },
        login_scenario: {
            startVUs: 0,
            executor: 'ramping-vus',
            stages: [
                {duration: '10s', target: 5}, //ramp up to 5
                {duration: '10s', target: 5},
                {duration: '10s', target: 0} //ramp down
            ],
            exec: 'login',
        },
    },
    thresholds: {
            http_req_duration: ['p(95)<500'],
            http_req_failed: ['rate<0.01'],
    },
};