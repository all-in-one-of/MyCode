//
// Created by HYC on 2019/3/16.
//

#include "Enemy.h"
#include <iostream>
#include <string>
#include <cmath>

using namespace std;

void Enemy::Attack() {
    cout << "¹¥»÷" << endl;
}

void Enemy::TakeDamage() {
    cout << "ÊÜÉË" << endl;

}

Enemy::Enemy() {
    HP = 100;
    Damage = 1;
}

