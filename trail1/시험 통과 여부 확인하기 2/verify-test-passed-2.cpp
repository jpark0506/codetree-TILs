#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> avg(n);


    for(int i = 0; i < n; i++){
        int sum = 0;
        for (int j =0; j<4; j++){
            int temp;
            cin >> temp;
            sum += temp;
        }
        avg[i] += sum / 4;
    }

    int cnt = 0;

    for(int i = 0; i < avg.size(); i++){
        if(avg[i] >= 60){
            cout << "pass" << endl;
            cnt += 1;
        }
        else{
            cout << "fail" << endl;
        } 
    }
    
    cout << cnt;

    return 0;
}