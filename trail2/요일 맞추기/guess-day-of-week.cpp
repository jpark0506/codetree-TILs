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

    int ansIndex = 0;

    while(true){

        if(cmonth == m2 && cday == d2){
            break;
        }
        
        if(cday <= month[cmonth]){
            cday++;
        }else{
            cday = cday % month[cmonth];
            if(cmonth == 12){
                cmonth = 1;
            }else{
                cmonth ++;
            }
        }
        ansIndex = ansIndex++ % 7;
    };

    cout << date[ansIndex];

    return 0;
}