#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    // Please write your code here.
    

    int sum = 0;

    for(int i=0; i<2; i++){

        string str;

        cin >> str;

        string temp;
        for(int j =0; j < str.length(); j++){
            if(isdigit(str[j])){
                temp += str[j];
            }else{
                break;
            }
        }

        sum += stoi(temp);

    }

    cout << sum;


    return 0;
}