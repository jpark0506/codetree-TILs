const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

let cnt = 0;

const n = Number(input[0]);
const grid = input.slice(1, n + 1).map(line => line.split(' ').map((e) => {
    const num = Number(e);

    if(num === 1){
        cnt++;
    }

    return num;
}));

// Please Write your code here.

const dx = [0,0, 1, -1];
const dy = [1,-1, 0, 0];

const inRange = (x, y) => 0 <= x && x < n && 0 <= y && y < n;

const isWall = (x, y) => grid[x][y] === 0;

const canGo = (x,y) => inRange(x,y) && !isWall(x,y);

let total = 0;
const pcount = [];

const findStartPos = () => {
    for(let i = 0; i < n ; i++){
        for(let j =0 ; j < n; j++){
            if(grid[i][j] === 1){
                return [i,j];
            }
        }
    }
    return false;
}

const createCounter = () => {
    let cnt = 0; 
    return {
        add: () => { cnt = cnt + 1; },
        value: () => cnt,
        reset: () => { cnt = 0 }
    }
}

const counter = createCounter();

function dfs(x, y){

    for(let i = 0; i < 4; i++){
        const next = [x + dx[i], y + dy[i]];
        if(canGo(...next)){
            grid[next[0]][next[1]] = 0;
            counter.add();
            dfs(...next);
        }
    }
}

function solve(){

    while(true){
        
        const h = findStartPos();

        if(!h){
            break;
        }

        const [sx, sy] = h;

        counter.add();
        grid[sx][sy] = 0;

        dfs(sx, sy);

        pcount.push(counter.value());

        counter.reset();
    }

}

solve();

pcount.sort((a, b) => Number(a) - Number(b));

console.log(pcount.length);

pcount.forEach(p => {
    console.log(p);
})
