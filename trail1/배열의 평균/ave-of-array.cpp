#include <iostream>
using namespace std;

int main() {
    // Please write your code here.

    int arr[2][4];

    int avg_all = 0;

    for(int i=0; i<2; i++){
        for(int j=0; j<4; j++){
            int temp;
            cin >> temp;
            arr[i][j] = temp;
        }
    }

    cout << fixed;
    cout.precision(2);

    // 가로 평균
    for(int i=0; i<2; i++){
        int avg = 0;
        for(int j=0; j<4; j++){
            avg += arr[i][j];
        }
        
        cout << (double)(avg / 4) << " ";
    }
    cout << endl;

    // 세로 평균
    for(int i=0; i<4; i++){
        int avg = 0;
        for(int j=0; j<2; j++){
            avg += arr[j][i];
            avg_all += arr[j][i];
        }
        cout << (double)(avg / 2) << " ";
    }
    
    cout << endl;

    cout << (double)(avg_all / 8); 

    return 0;
}