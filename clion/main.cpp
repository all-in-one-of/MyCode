#include <iostream>
#include <string>
#include <cmath>

using namespace std;


int createEnemy(int enemyType, const string &name) {
    if (enemyType == 1) {
        cout << "111" << name << endl;
        return 90;
    }
    cout << "222" << name << endl;

    return 20;
}


enum WeekDay {
    Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
};

enum HeroType {
    Master, Sldier, Assassin, Tank
};


struct myPosition {
    float x;
    float y;
    float z;
};


struct Enemy1 {
    int hp;
    int attack;
    string name;
    myPosition pos;
};


void runCalculator() {

}


int main() {

    int s = 324;
    string a = "°¡";

    cout << a << endl;

    return 0;
}