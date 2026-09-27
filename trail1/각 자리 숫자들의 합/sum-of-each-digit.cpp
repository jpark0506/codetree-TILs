#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.
    string str;
    cin >> str;

    int ans = 0;

    for(const auto& c : str){
        int k = c - '0';
        ans += k;
    }

    cout << ans << endl;

    return 0;
}