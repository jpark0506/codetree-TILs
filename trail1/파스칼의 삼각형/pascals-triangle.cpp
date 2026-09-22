#include <iostream>
using namespace std;

int main() {
    // Please write your code here.
    int arr[16][16] = {0,};

    arr[0][0] =1;
    arr[1][0] = 1;
    arr[1][1] = 1;

    int N;
    cin >> N;

    for (int i=2; i<N; i++){
        for(int j = 0; j < N; j++){
            arr[i][j] = arr[i-1][j-1] + arr[i-1][j];
        }
    }

    for(int i=0; i<N; i++){
        for(int j=0; j<N; j++){
            if(arr[i][j] == 0){
                break;
            }
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}