#include <iostream>
using namespace std;

int main() {
    // Please write your code here.
    int N;

    cin >> N;

    int arr[N][N];

    for(int i=0; i<N; i++){
        arr[i][0] = 1;
        arr[0][i] = 1;
    }

    for(int i=1; i<N; i++){
        for(int j=1; j<N; j++){
            arr[i][j] = arr[i-1][j-1] + arr[i-1][j] + arr[i][j-1];
        }
    }

    for(int i=0; i<N; i++){
        for(int j=0; j<N; j++){
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}