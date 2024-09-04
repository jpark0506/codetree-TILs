#include <iostream>
#define FEET 30.48
using namespace std;
int main() {
    double a;
    cin >> a;
    cout.fixed;
    cout.precision(4);
    cout << a*FEET << endl;
    return 0;
}