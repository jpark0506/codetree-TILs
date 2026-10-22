const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const [n, m] = input[0].split(' ').map(Number);
const grid = input.slice(1, n + 1).map(row => row.split(' ').map(Number));

// Please Write your code here.

const dx = [1, 0];
const dy = [0, 1];

const hasSnake = (x, y) => grid[x][y] === 0;

const inRange = (x, y) => 0 <= x && x < n && 0 <= y && y < m;

const canGo = (x,y) => inRange(x,y) && !hasSnake(x,y);

let found = false;

function dfs(x,y){
    
    // 이미 찾았을 경우
    if(found){
        return;
    }

    // 찾았을 경우
    if(x === n - 1 && y === m - 1){
        found = true;
        return;
    }

    for(let i = 0; i < 2; i++){
        const next = [x + dx[i], y + dy[i]];
    
        if(canGo(...next)){
            grid[next[0]][next[1]] = 0;
            dfs(...next);
        }
    }

}

dfs(0,0);

console.log(found ? 1 : 0);