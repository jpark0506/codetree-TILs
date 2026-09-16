#include <iostream>

using namespace std;

int n;
int price[1000];

int main() {
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> price[i];
    }
    int max = 0;
    for(int c = 1; c < n; c++){
        for(int i = 0; i < n; i++){
            if(max < price[i+c] - price[i]){
                max = price[i+c] - price[i];
            }
        }
    }

    cout << max;
    
    // Please write your code here.

    return 0;
}
