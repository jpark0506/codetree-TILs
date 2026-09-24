#include <iostream>
#include <string>
using namespace std;

int main() {

    string str;
    int q;

    cin >> str >> q;

    for (int i = 0; i < q; i++) {
        int command;
        cin >> command;

        if(command == 1){
            str = str.substr(1) + str[0];
        }

        if(command == 2){
            str = str[str.size() - 1] + str.substr(0, str.size()-1);
        }

        if(command == 3){
            string temp;
            for(int i = str.size() - 1; i >= 0; i--){
                temp += str[i];
            }
            str = temp;
        }

        cout << str << endl;
    }

    return 0;
}
