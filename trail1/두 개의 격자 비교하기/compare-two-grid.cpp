#include <iostream>
using namespace std;

int main() {
    // Please write your code here.

    int N, M;
    cin >> N >> M;

    int arr1[N][M];
    int arr2[N][M];

    int ans[N][M];

    for(int i=0; i<2; i++){
        for(int j = 0; j< N; j++){
            for(int k = 0; k < M; k++){
                int temp;
                cin >> temp;
                if(i == 0){
                    arr1[j][k] = temp;
                }else{
                    arr2[j][k] = temp;
                    if(arr1[j][k] == temp){
                        ans[j][k] = 0;
                    }
                    else{
                        ans[j][k] = 1;
                    }
                }
            }
        }
    }

    for(int i=0; i<N; i++){
        for(int j=0; j<M; j++){
            cout << ans[i][j] << " ";
        }
        cout << endl;
    }



    return 0;
}