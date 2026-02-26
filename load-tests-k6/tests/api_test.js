import http from 'k6/http';
import {check, sleep} from 'k6';
import {SharedArray} from 'k6/data';
import { BASE_URL, options } from '../k6-config.js';
export {options}

//------------------------------------------------------------------------------
// Init
//------------------------------------------------------------------------------
//Init context: load users from JSON
const users = new SharedArray('users', function(){
    return JSON.parse(open('../data/users.json'));
});

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

//------------------------------------------------------------------------------
// Teardown
//------------------------------------------------------------------------------
//This is where you would clean up test data, log results, or call a cleanup API

export function teardown(data){
    console.log(`Test finished. Tokens: ${data.tokens.length}`);
}