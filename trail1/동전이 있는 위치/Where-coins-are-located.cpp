#include <iostream>
#include <vector>
using namespace std;

int main() {
    // Please write your code here.
    int N, M;
    cin >> N >> M;

    vector<vector<int>> arr(N, vector<int>(N, 0));

    for(int i = 0; i<M; i++){
        int k,h;
        cin >> k >> h;
        arr[k-1][h-1] = 1;
    }

    for(int i=0; i<N; i++){
        for(int j=0; j<N; j++){
            cout << arr[i][j] << " ";
        }
        cout << endl;
    }

    return 0;
}