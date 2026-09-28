#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int n, k;
string t;
string str[100];

bool compare(const string& a, const string& b){

    for(int i = 0; i< b.length(); i++){
        if(b[i] != a[i]){
            return false;
        }
    }

    return true;
};

int main() {
    cin >> n >> k >> t;

    for (int i = 0; i < n; i++) {
        cin >> str[i];
    }

    sort(str, str + n);

    int cnt = 1;

    for(int i=0; i<n; i++){
        if(compare(str[i],t)){
            if(cnt == k){
                cout << str[i];
                return 0;
            }
            cnt++;
        }
    }


    return 0;
}