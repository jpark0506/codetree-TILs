#include <iostream>
using namespace std;

int main() {
    // Please write your code here.

    int n;
    cin >> n;
    
    int arr[n][n];

    int cnt = 1;
    bool T = true;

    for(int i = n-1; i >= 0; i--){
        if(T){
            for(int j = n-1; j>=0; j--){
                arr[i][j] = cnt++; 
            }
        }else{
            for(int j = 0; j <=n-1; j++){
                arr[i][j] = cnt++; 
            }
        }

        T = !T;
        
    }

    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            cout << arr[j][i] << " ";
        }
        cout << endl;
    }

    return 0;
}