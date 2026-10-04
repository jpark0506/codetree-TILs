const fs = require('fs');

let [str, target] = fs.readFileSync(0).toString().split('\n');

while(str.indexOf(target) !== -1){
    let index = str.indexOf(target);
    str = str.slice(0, index) + str.slice(index + target.length);
}

console.log(str);