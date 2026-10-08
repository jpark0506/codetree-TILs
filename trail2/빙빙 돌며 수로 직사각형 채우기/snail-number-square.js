const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');
const [n, m] = input[0].split(' ').map(Number);
// Please Write your code here.

const dx = [0, 1, 0, -1]; // n
const dy = [1, 0, -1, 0]; // m

let ans = Array.from({
    length : n
}, () => Array.from({
    length : m
}, () => 0));

const cR = (x, y) => { 
    return 0 <= x && x < n && 0 <= y && y < m; 
};

let cx = 0; 
let cy = 0;
let cnt  = 1;
let dir = 0; 

while(cnt <= n * m){

    ans[cx][cy] = cnt;

    let nx = cx + dx[dir];
    let ny = cy + dy[dir];


    if(!cR(nx, ny) || ans[nx][ny] !== 0){
        dir = (dir + 1)%4;

        nx = cx + dx[dir];
        ny = cy + dy[dir];

    }

    [cx, cy] = [nx, ny];

    cnt++;
}

for(let i =0 ; i<n; i++){
        console.log(ans[i].join(' '))
}