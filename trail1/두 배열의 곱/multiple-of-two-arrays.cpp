#include <iostream>
using namespace std;


int main() {
    // Please write your code here.

    int arr[3][3];
    int arr2[3][3];

    for(int i = 0; i<3; i++){
        for(int j = 0; j<3; j++){
            int temp;
            cin >> temp;

            arr[i][j] = temp;
        }
    }
    for(int i = 0; i<3; i++){
        for(int j = 0; j<3; j++){
            int temp;
            cin >> temp;

            arr2[i][j] = temp;
        }
    }

    for(int i = 0; i<3; i++){
        for(int j = 0; j<3; j++){
            cout << arr[i][j] * arr2[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}