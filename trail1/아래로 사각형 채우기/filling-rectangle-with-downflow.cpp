#include <iostream>
using namespace std;

int main() {
    // Please write your code here.
    int N;

    cin >> N;

    int arr[N][N];

    int cnt = 1;

    for(int i=0; i<N; i++){
        for(int j = 0; j < N; j++){
            arr[j][i] = cnt++;
        }
    }
    
    for(int i=0; i<N; i++){
        for(int j = 0; j < N; j++){
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}