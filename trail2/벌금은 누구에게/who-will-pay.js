const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split("\n");

const [n, m, k] = input[0].split(" ").map(Number);
const p = input.slice(1, m + 1).map(Number);

// Please Write your code here.

const s = Array(n+1).fill(0);

for(let b of p){
    s[b]++;
    if(s[b] === k){
        console.log(b);
    }
}
