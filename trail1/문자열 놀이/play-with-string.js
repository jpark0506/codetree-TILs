const fs = require('fs');

let input = fs.readFileSync(0).toString().trim().split('\n');

let [S, Q] = input[0].split(" ");

const switchChar = (S, t1, t2) => {
    let tS = S.split('');
    let temp = tS[t1];
    tS[t1] = tS[t2];
    tS[t2] = temp;
    return tS.join('');
}

for(let cmd of input.slice(1)){
    let [type, t1, t2] = cmd.split(" ");
    type = Number(type);
    if(type === 1){
        S = switchChar(S, Number(t1)-1, Number(t2)-1);
        
    }else{
        for(let i = 0; i< S.length; i++){
            if(S[i] === t1){
                S = S.slice(0, i) + t2 + S.slice(i+1);
            }
        }
    }
    console.log(S);
}

