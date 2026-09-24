#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.
    string str1, str2;

    getline(cin, str1);
    getline(cin, str2);

    for(auto c : str1){
        if(c != ' '){
            cout << c;
        }
    }

    for(auto c : str2){
        if(c != ' '){
            cout << c;
        }
    }

    return 0;
}