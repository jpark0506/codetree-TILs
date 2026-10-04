const fs = require("fs");

let [str, target] = fs.readFileSync(0).toString().split("\n");

console.log(str.indexOf(target));