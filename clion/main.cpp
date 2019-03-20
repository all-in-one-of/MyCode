#include <iostream>
#include <string>
#include <cmath>
#include "Enemy.h"
#include "Enemy_walk.h"

using namespace std;


int main() {

    Enemy enemy1;
    Enemy_walk enemyWalk;
    cout << enemy1.HP << endl;

    enemyWalk.TakeDamage();
    cout << enemyWalk.HP << endl;

    return 0;
}