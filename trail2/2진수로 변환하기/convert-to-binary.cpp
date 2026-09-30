#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int n;

int main() {
    cin >> n;

    vector<int> v;

    if(n == 0){
        cout << 0;
        return 0;
    }


    while(n != 0){
        if(n % 2 == 0){
            v.push_back(0);
            n /= 2;
        }else if(n % 2 == 1){
            n = (n-1) / 2;
            v.push_back(1);
        }
    }

    reverse(v.begin(), v.end());

    for(const auto& val : v){
        cout << val;
    }


    return 0;
}