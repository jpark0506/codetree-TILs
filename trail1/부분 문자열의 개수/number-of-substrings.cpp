#include <iostream>
#include <string>

using namespace std;

int main() {
    // Please write your code here.
    string A,B;

    cin >> A >> B;

    int cnt = 0; 

    for(int i=0; i<A.length(); i++){
        if(A.substr(i, B.length()) == B){
            cnt++;
        }
    }

    cout << cnt;

    return 0;
}