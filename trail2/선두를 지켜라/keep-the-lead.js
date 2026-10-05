const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split("\n");

const [n, m] = input[0].split(" ").map(Number);
const aData = input.slice(1, n + 1).map(line => line.split(" ").map(Number));
const bData = input.slice(n + 1, n + 1 + m).map(line => line.split(" ").map(Number));

const maxTA = aData.reduce((acc, cur) => acc + cur[1], 0);

const max = maxTA;

let changed = 0;
// 선두
let top = '';

// 현재 가지고 있는 속도 정보, 남아있는 시간, Data 내 인덱스
let ca = [...aData[0], 0];
let cb = [...bData[0], 0];

// 현재 위치를 나타낸다.
let pa = 0;
let pb = 0;

for (let i = 1; i < max; i++) {
    let [v, t, ci] = [0, 1, 2];
    // 1. A 이동
    // 2. B 이동
    // 3. A의 위치와, B의 위치를 비교한다. 만약 역전했을 경우 선두 변경++
    ca[t]--;
    cb[t]--;

    pa += ca[v];
    pb += cb[v];

    if (pa < pb) {
        if (top !== 'B') {
            if (top !== '') {
                changed++;
            }
            top = 'B';
        }
    }

    if (pa > pb) {
        if (top !== 'A') {
            if (top !== '') {
                changed++;
            }
            top = 'A';
        }
    }

    if (aData.length > ca[ci]) {
        if (ca[t] == 0) {
            let nI = ca[ci] + 1;
            ca = [...aData[nI], nI]; // 다음 데이터 주입
        }
    }

    if (bData.length > cb[ci]) {
        if (cb[t] == 0) {
            let nI = cb[ci] + 1;
            cb = [...bData[nI], nI]; // 다음 데이터 주입
        }
    }
}

console.log(changed);