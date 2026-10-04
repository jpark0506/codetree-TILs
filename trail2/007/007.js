const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');
const [s_code, m_point, time] = input[0].split(' ');
// Please Write your code here.
class Zero{
    constructor(s_code, m_point, time){
        this.s_code = s_code
        this.m_point = m_point
        this.time = time
    }

    print(){
        console.log("secret code :", s_code);
        console.log("meeting point :", m_point);
        console.log("time :", time);
    }
}

const zero = new Zero(
    s_code,
    m_point,
    time
);

zero.print();