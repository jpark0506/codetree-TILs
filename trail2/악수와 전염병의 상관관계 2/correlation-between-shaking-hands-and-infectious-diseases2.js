const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');
const [n, k, p, t] = input[0].split(' ').map(Number);
const shakes = [];
for (let i = 1; i <= t; i++) {
    const [time, person1, person2] = input[i].split(' ').map(Number);
    shakes.push({ time, person1, person2 });
}

const concount =  Array(n+1).fill(0)
const ans = Array(n+1).fill(0);

shakes.sort((a, b)=> a.time - b.time);

concount[p] = k;
ans[p] = 1;


for(const { person1, person2 } of shakes){
    const isCon = (p) => ans[p] === 1 && concount[p] > 0;

    const newCon = [];

    if(isCon(person1)){
        concount[person1]--;
        newCon.push(person2);
    }
    if(isCon(person2)){
        concount[person2]--;
        newCon.push(person1);
    }

    newCon.forEach((con)=>{
        if(ans[con] === 0){
            ans[con] = 1;
            concount[con] = k;
        }
    })
}

console.log(ans.slice(1).join('')); 