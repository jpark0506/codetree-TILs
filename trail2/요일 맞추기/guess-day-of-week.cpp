#include <iostream>
#include <string>
using namespace std;

int m1, d1, m2, d2;
int month[13] = {
    0,
    31,29,31,30,31,30,31,31,30,31,30,31
};
string date[7] = {
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
};

int main() {

    cin >> m1 >> d1 >> m2 >> d2;

    int cmonth = m1;
    int cday = d1;

    int tmonth = m2;
    int tday = d2;

    int ansIndex = 0;

    bool flag = true;

    if(cmonth > tmonth){
        flag = false;
    }else{
        if(cmonth == tmonth){
            if(cday > tday){
                flag = false;
            }
        }
    }

    while(true){

        if(cmonth == tmonth && cday == tday){
            break;
        }
        
        if(cday <= month[cmonth]){
            if(flag){
                cday++;
            }else{
                cday--;
            }
        }else{
            cday = cday % month[cmonth];
            if(flag){
                cmonth++;
            }else{
                cmonth--;
            }
        }
        ansIndex = ansIndex % 7;
        if(flag){
            ansIndex++;
        }else{
            if(ansIndex == 0){
                ansIndex = 6;
            }else{
                ansIndex--;
            }
        }
    };

    cout << date[ansIndex];

    return 0;
}