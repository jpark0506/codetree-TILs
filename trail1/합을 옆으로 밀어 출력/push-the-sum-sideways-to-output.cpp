#include <iostream>
using namespace std;

int main() {
    // Please write your code here.

    int N;

    cin >> N;

    int sum = 0;

    for(int i = 0; i< N; i++){
        int t;

        cin >> t;

        sum += t;
    }

    string str = to_string(sum);

    str = str.substr(1) + str[0];

    cout << str;

    return 0;
}