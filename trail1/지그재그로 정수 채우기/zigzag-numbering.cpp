#include <iostream>

using namespace std;

int n, m;

int main() {
    cin >> n >> m;

    int arr[n][m];

    int cnt = 0;

    
    for(int j = 0; j < m; j++){
        for(int i = 0; i < n; i++){
            if(j % 2 == 0){
                arr[i][j] = cnt++;
            }else{
                arr[n-1-i][j] = cnt++;
            }
        }
    }

    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }

    // Please write your code here.

    return 0;
}
