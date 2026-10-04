const target = ['ee', 'eb'];
const ans = [0,0];

const fs = require('fs');

let input = fs.readFileSync(0).toString();

for(let i = 0; i<2; i++){
    const t = target[i];
    let start = 0;

    while(input.indexOf(t, start) != -1){
        const nextIndex = input.indexOf(t, start) + 1;
        start = nextIndex;
        ans[i]++;
    }
}

console.log(ans.join(" "));