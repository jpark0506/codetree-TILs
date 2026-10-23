const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const [n, m] = input[0].split(' ').map(Number);
const grid = input.slice(1, n + 1).map(line => line.split(' ').map(Number));

// Please Write your code here.

const dx = [0, 0, 1, -1];
const dy = [1, -1, 0, 0];

const createArr = () =>  Array.from({
    length : n,
}, () => Array.from({
    length : m
}, () => 0));

const step = createArr();
const visited = createArr();

const inRange = (x, y) => 0 <= x && x < n && 0 <= y && y < m;
const hasSnake = (x, y) => grid[x][y] === 0;
const hasVisited = (x,y) => visited[x][y] === 1;
const canGo = (x, y) => inRange(x, y) && !hasSnake(x,y) && !hasVisited(x,y);

const bfs = (x, y) => {
    let q = [];

    q.push([x,y]);
    visited[x][y] = 1;
    
    
    while(q.length !== 0){
        let top = q.shift();
        const [tx, ty] = top;

        for(let i = 0; i < 4; i++){
            const [nx, ny] = [tx + dx[i], ty + dy[i]];
            if(canGo(nx, ny)){
                visited[nx][ny] = 1;
                step[nx][ny] = step[nx][ny] !== 0 ? Math.min(step[tx][ty] + 1, step[nx][ny]) : step[tx][ty] + 1;
                q.push([nx, ny]);
            }

        }

    }

}
bfs(0,0);

console.log(step[n-1][m-1]);