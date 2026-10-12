const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);
const arr = Array.from({length: n}, (_, i) => input[i + 1].split(' ').map(Number));

// Please Write your code here.

const dist = (x1, y1, x2, y2) => {
    return Math.abs(x1 - x2) + Math.abs(y1- y2); 
}

const cal = (index) => {
    let sum = 0;

    for(let i = 1; i < n; i++){
        if(i === index)
            continue;

        if(i === index + 1){
            sum += dist(...[...arr[i], ...arr[i - 2]]);
        }else{
            sum += dist(...[...arr[i], ...arr[i - 1]])
        }
    }

    return sum;
}

let min = 100000000;

for(let i = 1; i < n - 1; i++){
    let r = cal(i);

    if(min > r){
        min = r;
    }
}

console.log(min);