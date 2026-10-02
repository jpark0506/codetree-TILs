#include <iostream>

using namespace std;

int n;
int x[1000];
char dir[1000];

int road[2000002] = {0};
char color[2000002] = {};

int main() {
    cin >> n;

    for (int i = 0; i < n; i++) {
        cin >> x[i] >> dir[i];
    }

    int coord = 1000000;

    for (int i = 0; i < n; i++){
        if(dir[i] == 'R'){
            int cnt = 0;
            while(cnt < x[i]){
                cnt++;
                road[coord]++;
                color[coord] = 'B';
                //cout << "RColor" << coord << " ";
                if(cnt != x[i])
                    coord++;
                
            };
        }
        if(dir[i] == 'L'){
            int cnt = 0;
            while(cnt < x[i]){
                cnt++;
                road[coord]++;
                color[coord] = 'W';
                //cout << "LColor" << coord << " ";
                if(cnt != x[i])
                    coord--;
            };
        }
    }

    int gray = 0;
    int black = 0;
    int white = 0;

    for(int i = 0; i < 2000002; i++){
        if(road[i] >= 4){
            gray++;
        }else{
            if(color[i] == 'B'){
                black++;
            }else if(color[i] == 'W'){
                white++;
            }
        }
    }

    cout << white << " " << black << " " << gray;

    return 0;
}