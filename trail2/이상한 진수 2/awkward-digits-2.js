const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const a = input[0];

// Please Write your code here.

const solution = () => {

    let sum = 0;

    for(let i = a.length-1; i>=0; i--){
        sum += 2 ** ((a.length-1) - i) * Number(a[i]);
    }


    let max = 0;

    for(let i = a.length - 1; i >= 0; i--){

        const n = Number(a[i]) === 0 ? 1 : 0;

        if(n === 1){
            const r = sum + 2 ** ((a.length-1) - i);
            if(max < r){
                max = r;
            }
        }else{
            const r = sum - 2 ** ((a.length-1) - i);
            if(max < r){
                max = r;
            }
        }        
    }
    return max;
}

console.log(solution());