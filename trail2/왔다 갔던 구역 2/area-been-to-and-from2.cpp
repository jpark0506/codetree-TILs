#include <iostream>

using namespace std;

int n;
int x[100];
char dir[100];

int road[2002] = {0};

int main() {
    cin >> n;

    int coord = 1000;

    for (int i = 0; i < n; i++) {
        cin >> x[i] >> dir[i];
    }

    for (int i = 0; i < n; i++){
        if(dir[i] == 'R'){
            int current = coord;
            int cnt = 0;
            while(cnt < x[i]){
                cnt++;
                road[++coord]++;
            };
        }
        if(dir[i] == 'L'){
            int current = coord;
            int cnt = 0;
            while(cnt < x[i]){
                cnt++;
                road[coord--]++;
            };
        }
    }

    int ans = 0;

    for(int i = 0; i < 2002; i++){
        if(road[i] >= 2){
            ans++;
        }
    }

    cout << ans;

    return 0;
}