#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int N, B;

int main() {
    cin >> N >> B;

    // Please write your code here.

    vector<int> v;

    while(N != 0){
        v.push_back(N % B);
        N = (N - N%B) / B;
    }

    reverse(v.begin(), v.end());

    for(const auto& val : v){
        cout << val;
    }


    return 0;
}