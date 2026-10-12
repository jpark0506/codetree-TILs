const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);
const arr = input.slice(1, 1 + n).map(Number);

const l  = arr.length;

// Please Write your code here.

const checkHasCarry = (a, b, c) => {
    // a, b, c는 문자열

    const [ra, rb, rc] = [a, b, c].map(e => {
        let arr = Array.from(String(e));
        return arr.map(Number).reverse();
    })

    const max = Math.max(ra.length, rb.length, rc.length);

    for(let i = 0; i < max; i++){
        let rra = ra[i] ?? 0;
        let rrb = rb[i] ?? 0;
        let rrc = rc[i] ?? 0;

        if(rra + rrb + rrc >= 10){
            return true;
        }
    }

    return false;
}

let max = -1;

for(let i = 0; i < l - 2; i++){
    for(let j = i+1; j < l - 1; j++){
        for(let k = j+1; k < l; k++){
            const args = [arr[i], arr[j], arr[k]];
            if(!checkHasCarry(...args)){
                const sum = args.reduce((acc, cur) => acc + cur, 0);
                if(sum > max){
                    max = sum;
                }
            }
        }
    }
}

console.log(max);