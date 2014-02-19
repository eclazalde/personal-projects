#pragma once

#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <semaphore.h>

using namespace std;

class Storage {
public:
    Storage();
    ~Storage();

    string store(string, string, string);
    string list_tostring();
    string get_tostring(int);
    string get_name();

protected:
    string name;
    vector<string> subject;
    vector<string> message;
};
