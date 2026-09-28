#include <iostream>
#include <functional>
#include <algorithm>

using namespace std;

int n;
int nums[100];

int main() {
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    
    sort(nums, nums + n, greater<int>());


    // Please write your code here.

    return 0;
}
