#include <iostream>
#include <algorithm>
using namespace std;

int N;

class Seq {
public:
    int oindex;
    int value;
    int nindex;

    Seq(){
        this -> oindex = -1;
        this -> value = -1;
        this -> nindex = -1;
    }

    Seq(int oindex, int value){
        this -> oindex = oindex;
        this -> value = value;
        this -> nindex = -1;
    }

};

bool cmp(Seq a, Seq b){
    if(a.value == b.value){
        return a.oindex < b.oindex;
    }
    return a.value < b.value;
};

bool cmpIndex(Seq a, Seq b){
    return a.oindex < b.oindex;
}


int main() {
    Seq s[1000];
    cin >> N;
    for (int i = 0; i < N; i++) {
        int t;
        cin >> t;

        s[i] = Seq(i, t);
    }
    sort(s,s + N,cmp);

    for(int i=0; i<N; i++){
        s[i].nindex = i + 1;
    }

    sort(s, s+N, cmpIndex);

    for(int i=0; i<N; i++){
        cout << s[i].nindex << " ";
    }

    return 0;
}
