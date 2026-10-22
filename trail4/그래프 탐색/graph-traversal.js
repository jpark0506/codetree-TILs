const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const [n, m] = input[0].split(' ').map(Number);

const edges = [];

const graph = Array.from({ length : n + 1 }, () => []);

for (let i = 1; i <= m; i++) {
    edges.push(input[i].split(' ').map(Number));
}

for(const [s, e] of edges) {
    graph[s].push(e);
    graph[e].push(s);
}
// Please Write your code here.


let cnt = 0; 
// 방문했을 경우 번호가 존재한다.
let vs = new Set();

const hasVisited = (e) => vs.has(e);

const visited = (e) => vs.add(e);

const q = [...graph[1]];

visited(1);

function dfs(){
    
    if(q.length === 0){
        return;
    }

    let top = q.pop();

    for(const ne of graph[top]){
        if(!hasVisited(ne)){
            visited(ne);
            q.push(ne);
            dfs();
            cnt++;
        }
    }

}

dfs();

console.log(cnt);