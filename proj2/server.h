#pragma once

#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#include "storage.h"
#include <iostream>
#include <vector>
#include <sstream>

#include <string>

using namespace std;

class Server {
public:
    Server();
    ~Server();

    void handle(int, vector<Storage>&, sem_t&, sem_t&);
    
protected:
    string get_request(int);
    bool send_response(int, string);
    
    string read_request(string, vector<Storage>&, sem_t&, sem_t&);
    vector<string> split(string, char);
    string get_message(vector<string>);
    int name_index(string, vector<Storage>&);

    int buflen_;
    char* buf_;
};
