#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.

    string str;

    cin >> str;

    string arr[2] = { "ee", "ab" };

    for(const auto& s : arr){
        bool flag = false;
        for(int i=0; i<str.length(); i++){
                if(str.substr(i, 2) == s){
                    flag = true;
                }
        }
        if(flag){
            cout << "Yes";
        }else{
            cout << "No";
        }

        cout << " ";
    }

    return 0;
}