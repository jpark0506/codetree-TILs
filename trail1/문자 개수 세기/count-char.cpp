#include <iostream>
#include <string>
#include <set>
using namespace std;

int main() {
    // Please write your code here.
    string str;

    getline(cin, str);

    char input;
    cin >> input;

    int cnt = 0;

    for(int i=0; i<str.length(); i++){

        if(input == str[i]){
            cnt++;
        }
    }
    
    cout << cnt;
    return 0;
}