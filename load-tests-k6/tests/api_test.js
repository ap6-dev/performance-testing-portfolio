import http from 'k6/http';
import {check, sleep} from 'k6';
import {SharedArray} from 'k6/data';

//------------------------------------------------------------------------------
// Init
//------------------------------------------------------------------------------
//Init context: load users from JSON
const users = new SharedArray('users', function(){
    return JSON.parse(open('../data/users.json'));
});

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
                {duration: '20s', target: 5},
                {duration: '10s', target: 0} //ramp down
            ],
            exec: 'login',
        },
        fetch_data_scenario: {
            executor: 'constant-vus',
            vus: 3,
            duration: '30s',
            exec: 'fetch_data',
        },
    },
    thresholds: {
            http_req_duration: ['p(95)<500'],
            http_req_failed: ['rate<0.01'],
    },
};

//Official k6 testing api
const BASE_URL = 'https://quickpizza.grafana.com';

//Init context: select random user from users
function getRandomUser() {
    return users[Math.floor(Math.random() * users.length)];
}

//------------------------------------------------------------------------------
// Setup
//------------------------------------------------------------------------------
//This is where you would log in once and share tokens, seed test data, or fetch
//config from an API

//Send POST requests to create the users specified in 'users.json'
//Check for valid response
//Save login tokens
export function setup(){
    let tokens = [];
        for (let user of users){
            const payload = JSON.stringify({username: user.username, password: user.password});
            const headers = {'Content-Type': 'application/json'};

            let loginResponse = http.post(`${BASE_URL}/api/users/token/login`, payload, {headers});

            if(loginResponse.status === 200 && loginResponse.json().token){
                tokens.push(loginResponse.json().token);
            } else {
                console.log(`Login failed for ${user.username}`);
            }
        }
    return {tokens};
}

//------------------------------------------------------------------------------
// VU Code
//------------------------------------------------------------------------------

//Public endpoint w/ no auth
export function public_flow(){
    const response = http.get(BASE_URL);

    check(response, {
        'public status 200': (r) => r.status === 200,
        'public response not empty': (r) => r.body.length > 0,
    });

    sleep(1);
}

//Private endpoint w/ tokens from setup
export function private_flow(data) {
    const token = data.tokens[Math.floor(Math.random() * data.tokens.length)];
    let pizzaData = {
        maxCaloriesPerSlice: 500,
        mustBeVegetarian: false,
        excludedIngredients: ["pepperoni"],
        excludedTools: ["knife"],
        maxNumberOfToppings: 6,
        minNumberOfToppings: 2,
    };

    const response = http.post(`${BASE_URL}/api/pizza`, JSON.stringify(pizzaData), {
        headers: {
            'Content-Type': 'application/json',
            Authorization: `token ${token}`
        },
    });

    check(response, {
        'private status 200': (r) => r.status === 200,
    });

}

//Login function
export function login(){
    const user = getRandomUser();
    const payload = JSON.stringify({username: user.username, password: user.password});
    const headers = {'Content-Type': 'application/json'};

    let response = http.post(`${BASE_URL}/api/users/token/login`, payload, {headers});
    check(response, {'login successful': (r) => r.status === 200});
    sleep(1);
}

//Fetch data function
export function fetch_data(){
    const response = http.get(BASE_URL);
    check (response, {
        'status is 200': (r) => r.status === 200,
        'body not empty': (r) => r.body.length > 0, 
    });
    sleep(1)
}

//------------------------------------------------------------------------------
// Teardown
//------------------------------------------------------------------------------
//This is where you would clean up test data, log results, or call a cleanup API

export function teardown(data){
    console.log(`Test finished. Tokens: ${data.tokens.length}`);
}