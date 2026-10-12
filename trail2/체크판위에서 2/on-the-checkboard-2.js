const fs = require("fs");
const input = fs.readFileSync(0).toString().trim().split('\n');

const [R, C] = input[0].split(' ').map(Number);
const grid = input.slice(1).map(line => line.trim().split(' '));

// Please Write your code here.

const toggleColor = (color) => color === 'W' ? 'B' : 'W';

const fc = toggleColor(grid[0][0]);

const scanTarget = (r, c, targetColor) => {

    const coordR = [];
    const coordC = [];

    const isLastCoord = (r, c) => (r === (R - 1)) && (c === (C - 1));

    for(let i = r+1; i < R; i++){
        for(let j = c+1; j < C; j++){
                if(grid[i][j] === targetColor && !isLastCoord(i,j)){
                    coordR.push(i);
                    coordC.push(j);
                }
        }
    }
    return {
        coordR,
        coordC,
    }
}


const solution = () => {
    let ans = 0;

    let start = [0, 0, fc];

    const { coordR : fcoordR, coordC : fcoordC } = scanTarget(...start);

    if(fcoordR.length === 0){
        return fcoordR;
    }

    let toggledColor = toggleColor(fc);

    for(let i = 0 ; i < fcoordR.length; i++){

        if(toggledColor === grid[R-1][C-1])
            return 0;
        
        let next = [fcoordR[i], fcoordC[i], toggledColor];
        
        const { coordR, coordC } = scanTarget(...next);

        if(coordR.length === 0){
            continue;
        }

        for(let j = 0; j < coordR.length; j++){
            if(coordR[j] < R - 1 && coordC[j] < C - 1){
                ans++;
            }
        }
        
    }

    return ans;
}

console.log(solution());






