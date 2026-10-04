const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split("\n");

const [n, m] = input[0].split(' ').map(Number);
let line = 1;
const movesA = [];
for (let i = 0; i < n; i++) {
    const [d, t] = input[line++].split(' ');
    movesA.push([d, Number(t)]);
}
const movesB = [];
for (let i = 0; i < m; i++) {
    const [d, t] = input[line++].split(' ');
    movesB.push([d, Number(t)]);
}

// Please Write your code here.

let coordA = 1000 * 1000 + 1;
let coordB = 1000 * 1000 + 1;

let rA = {
    index : 0,
    t : movesA[0][1],
    dir : movesA[0][0]
};
let rB = {
    index: 0,
    t : movesB[0][1],
    dir : movesB[0][0]
}

let noNextA = false;
let noNextB = false;

let t = 0;

while(true){

    if((noNextA && noNextB)){
        console.log(-1);
        break;
    }

    if(coordA === coordB && t!==0){
        console.log(t);
        break;
    }

    rA.t--;

    if(rA.dir === 'R'){
        coordA++;
    }
    if(rA.dir === 'L'){
        coordA--;
    }

    if(rA.t === 0){
        
        let indexT = ++rA.index;
        if(movesA.length > indexT){
            rA = {
                index: indexT,
                t: movesA[indexT][1],
                dir:movesA[indexT][0],
            }
        }else{
            noNextA = true;
        }
        
    }

    rB.t--;
    
    if(rB.dir === 'R'){
        coordB++;
    }
    if(rB.dir === 'L'){
        coordB--;
    }

    if(rB.t === 0){
        let indexTB = ++rB.index;
        if(movesB.length > indexTB){
            rB = {
                index: indexTB,
                t: movesB[indexTB][1],
                dir:movesB[indexTB][0],
            }
        }else{
            noNextB = true;
        }

    }

    t++;
}