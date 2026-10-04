const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);
const commands = input.slice(1).map(line => line.split(' '));

// Please Write your code here.

const arr = Array(1000 * 100 * 2 + 1).fill(0);
const color = Array(1000 * 100 * 2 + 1).fill('');

let coord = 1000 * 100 + 1;

// 표시하고 이동.
for(let [move, cmd] of commands){
    
    move = Number(move);
    if(cmd === 'R'){
        for(let i = 0; i < move; i++){
            arr[coord + i] = arr[coord + i] + 1;
            color[coord + i] = 'B';
        }
        coord = coord + move - 1;
    }
    if(cmd === 'L'){
        for(let i = 0; i < move; i++){
            arr[coord - i] = arr[coord - i] + 1;
            color[coord - i] = 'W';
        }
        coord = coord - move + 1;
    }
}



const gray = arr.filter((v) => {
    return v >= 4;
}).length;

const white = arr.filter((v, index) => {
    return v < 4 && color[index] === 'W';
}).length;

const black = arr.filter((v, index) => {
    return v < 4 && color[index] === 'B';
}).length;

console.log(white, black, gray)