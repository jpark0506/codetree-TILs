#include <iostream>
#include <set>
#include <unordered_set>
using namespace std;

int N;

int main() {
    cin >> N;

    set<int, greater<int>> s;
    unordered_set<int> us;

    for (int i = 0; i < N; i++) {
        int temp;
        cin >> temp;
        if(s.count(temp) != 0  || us.count(temp) != 0){
            s.erase(temp);
            us.insert(temp);
        }else{
            s.insert(temp);
        }
    }

    if(!s.empty()){
        auto ans = s.begin();
        cout << *ans;
        return 0;
    }

    cout << -1;
    

    // Please write your code here.

    return 0;
}
