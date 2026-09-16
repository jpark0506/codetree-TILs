#include <iostream>
using namespace std;

int main() {
    // Please write your code here.

    int arr[4][4];

    for(int i =0 ; i<4; i++){
        for(int j =0 ; j<4; j++){
            int temp;
            cin >> temp;
            arr[i][j] = temp;
            
        }
    }

    int sum = 0;

    for(int i=0; i<4; i++){
        for(int j=0; j <= i; j++){
            sum += arr[i][j];
        }
    }

    cout << sum;

    return 0;
}