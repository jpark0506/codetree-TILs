#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.

    int ans = 0;

    for(int i=0; i<2; i++){
        string str;

        cin >> str;

        ans += str.length();
    }

    cout << ans;

    return 0;
}