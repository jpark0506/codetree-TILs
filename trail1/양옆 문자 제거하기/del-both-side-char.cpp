#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.

    string str;

    cin >> str;

    str.erase(1,1);

    str.erase(str.length() - 2, 1);

    cout << str;

    return 0;
}