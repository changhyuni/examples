// 공식문서 Demo Code 

import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
    vus: 1,                // 1 Users
    duration: '3000s',        // 
};

// 1. init Code
export function setup() {
    // 2. Setup Code
}


export default function () {
    // 3. VU Code
    http.get('http://grafana.juneman.click/');
    sleep(1);
}