const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const [n, m] = input[0].split(' ').map(Number);
const a = input.slice(1, 1 + n).map(line => line.split(' ').map(Number));

let outerW = new Set();
const innerW = new Set();
const ice = new Set();
const meltableIce = new Set();

const key = (x, y) => `${x},${y}`;

const dx = [0, 0, 1, -1];
const dy = [1, -1, 0, 0];

const visited = new Set();
const inRange = (x, y) => 0 <= x && x < n && 0 <= y && y < m;
const isIce = (x, y) => a[x]?.[y] === 1;
const hasVisited = (x, y) => visited.has(key(x, y));
const canGo = (x, y) => inRange(x, y) && !isIce(x, y) && !hasVisited(x, y);

for (let i = 0; i < n; i++) {
    for (let j = 0; j < m; j++) {
        if (a[i][j] === 1)
            ice.add(key(i, j));
        else
            innerW.add(key(i, j));
    }
}

// x, y는 시작 좌표
function bfs(x, y, callback) {
    const q = [[x, y]];

    visited.add(key(x, y));
    callback(x, y);

    while (q.length !== 0) {
        let [tx, ty] = q.shift();

        for (let i = 0; i < 4; i++) {
            const [nx, ny] = [tx + dx[i], ty + dy[i]];

            if(isIce(nx,ny)){
                meltableIce.add(key(nx,ny));
            }

            if (canGo(nx, ny)) {
                visited.add(key(nx, ny));
                q.push([nx, ny]);
                callback(nx, ny);
            }
        }
    }
    visited.clear();
}

bfs(0, 0, (x, y) => {
    innerW.delete(key(x, y));
    outerW.add(key(x, y));
});

// x, y는 얼음 좌표들만 들어간다.
function melt(x, y) {
    let isMeletable = false;

    const tempOuterW = new Set();
    const tempMeltableIce = new Set();
    for (let i = 0; i < 4; i++) {
        const ncoord = [x + dx[i], y + dy[i]]
        const nc = key(...ncoord);
        if (outerW.has(nc)) {
            isMeletable = true;
            tempOuterW.add(key(x, y));
            if (innerW.has(nc)) {
                tempOuterW.add(nc);
                innerW.delete(nc);
                // 이미 녹아버린 얼음
                tempMeltableIce.delete(nc);
            }
            if(a[ncoord[0]][ncoord[1]] === 1){
                tempMeltableIce.add(nc);
            }
        }
    }
    return [x, y, isMeletable, tempOuterW, tempMeltableIce];
}

const mergeSet = (set, mSet) => new Set([...set, ...mSet]);

let lastIceCnt = ice.size;
let time = 0;

while (ice.size !== 0) {
    lastIceCnt = ice.size;

    const arr = [];
    for (const pos of [...meltableIce]) {
        const [x, y] = pos.split(',').map(Number);
        arr.push(melt(x, y));
    }
    meltableIce.clear();
    for (let i = 0; i < arr.length; i++) {
        const [x, y, isMeletable, tempOuterW, tempMeltableIce] = arr[i];
        meltableIce.add(...tempMeltableIce);
        if (isMeletable) {
            outerW = mergeSet(outerW, tempOuterW);
            ice.delete(key(x, y));
            a[x][y] = 0;
        }
    }

    
    time += 1;
}

console.log(time, lastIceCnt);