#include <iostream>
#include <string>
using namespace std;

int main() {
    // Please write your code here.
    string arr[2];

    for(int i=0; i<2; i++){
        string t;
        cin >> t;
        arr[i] = t;
    }

    if(arr[0].length() > arr[1].length()){
        cout << arr[0] << " " << arr[0].length();
        return 0;
    }else if(arr[0].length() == arr[1].length()){
        cout << "same"; 
        return 0;
    }

    cout << arr[1] << " " << arr[1].length();

    return 0;
}