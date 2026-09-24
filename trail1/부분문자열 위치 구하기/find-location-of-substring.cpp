#include <iostream>
#include <string>

using namespace std;

string input_str;
string target_str;

int main() {
    cin >> input_str;
    cin >> target_str;

    // Please write your code here.

    if(input_str.find(target_str) != string::npos){
        int index = input_str.find(target_str);
        cout << index;
    }else{
        cout << -1;
    }

    return 0;
}
