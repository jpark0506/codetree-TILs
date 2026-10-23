const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const n = Number(input[0]);

// Please Write your code here.

const dp = [0, 1];

// 서브트리 개수에 따라 dp를 사용해서 더해줄 수 있다.

// dp[i] -> i개의 같지 않은 원소들이 있을 때 생성 가능한 이진트리의 개수

if(n < 2){
    console.log(dp[n]);
    return;
}

for(let i = 2; i < n + 1; i++){
    // dp[i] 공간을 만들어준다.
    dp.push(0);

    for(let j = 0; j < i; j++){
        let k = i - j - 1;

        console.log({
            j, k,
            dpj : dp[j],
            dpk : dp[k]
        })
        
        if(j === k){
            dp[i] += dp[j];
        }else{
            dp[i] += (dp[j] === 0 ? 1 : dp[j]) * (dp[k] === 0 ? 1 : dp[j]);
        }
        
        
        
    }
    console.log({
        dpi : dp[i]
    })
}

console.log(dp[n])