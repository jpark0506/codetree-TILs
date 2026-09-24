#include <iostream>
#include <string>
using namespace std;

string A, B;

int main() {
    cin >> A;
    cin >> B;

    // Please write your code here.

    while(A.find(B) != string::npos){
        int index = A.find(B);
        A.erase(index, B.length());
    }

    cout << A;

    return 0;
}
