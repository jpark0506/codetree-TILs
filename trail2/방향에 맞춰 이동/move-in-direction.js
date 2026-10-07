const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);
const moves = input.slice(1).map(move => {
    return move.split(" ");
}).map(([command, len]) => [command, Number(len)]);

// Please Write your code here.
const com = ['N', 'S', 'E', 'W'];
const dx = [0, 0, 1, -1];
const dy = [1, -1, 0, 0];

let cx = 0;
let cy = 0;

for(let i = 0; i<n; i++){
    const [command, len] = moves[i];
    const index = com.indexOf(command);
    cx += dx[index] * len;
    cy += dy[index] * len;
}

console.log(cx, cy);