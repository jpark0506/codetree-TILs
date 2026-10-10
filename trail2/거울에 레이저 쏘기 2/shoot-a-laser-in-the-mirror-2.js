const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);
const arr = input.slice(1, n + 1);
const startNum = Number(input[n + 1]);

const map = [[]];

for(let i =0; i< n + 2; i++){
    map[0].push(0);
}

for(let i = 0; i < n; i++){
    let a = [0];
    for(let j = 0; j < n; j++){
        a.push(arr[i][j]);
    }
    a.push(0);
    
    map.push(a);
}
map.push([]);
for(let i =0; i < n + 2; i++){
    
    map[n + 1].push(0);
}
// Please Write your code here.

const dx = [0, 1, 0, -1];
const dy = [1, 0, -1, 0];

const findIndex = (cx, cy) => {
    for(let i = 0; i < 4; i++){
        if(dx[i] === cx && dy[i] === cy){
            return i;
        }
    }
}

const rotateDir = (cx, cy, isClockwise) => {
    const index = findIndex(cx, cy);
    if(isClockwise){
        return (index + 1) % 4;
    }else{
        return (index - 1) % 4;
    }
}

const nextDir = (cx, cy, e) => {
    try{

    if(e === '\\'){
        let index = findIndex(cx, cy);
        // 가로 -> 시계
        // 세로 -> 반시계
        if(index % 2 === 0){
            return rotateDir(cx, cy, true);
        }else{
            return rotateDir(cx, cy, false);
        }

    }

    if(e === '/'){
        let index = findIndex(cx, cy);
        // 가로 -> 반시계
        // 세로 -> 시계
        if(index % 2 === 0){
            return rotateDir(cx, cy, false);
        }else{
            return rotateDir(cx, cy, true);
        }
    }

    return -1;
}catch(e){
    console.log(cx, cy);
}
}

const findKpos = (n, startNum) => {
    const myun = parseInt(startNum / n);

    const startpos = startNum % n;

    if(myun === 0){
        return [0, startpos, 1];
    }
    if(myun === 1){
        return [startpos, n + 1, 2];
    }
    if(myun === 2){
        return [n + 1, n + 1 - startpos, 3];
    }
    if(myun === 3){
        return [n + 1 - startpos, 0, 0];
    }

}

let cnt = 0;

let [sx, sy, dir] = findKpos(n, startNum);

// console.log({
//     sx, sy, dir
// })

while(true){

    const [nx, ny] = [sx + dx[dir], sy + dy[dir]];

    const ndir = nextDir(dx[dir], dy[dir], map[nx][ny]);

    //console.log({nx, ny, ndir, e : map})

    if(ndir === -1){
        break;
    }

    [sx, sy, dir] = [nx, ny, ndir];

    cnt++;

}

console.log(cnt);


