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

    void run();
    
protected:
    virtual void create();
    virtual void close_socket();
    void serve();
    void handle(int);
    string get_request(int);
    bool send_response(int, string);
    
    string read_request(string);
    vector<string> split(string, char);
    string validate_request(string);
    string get_message(vector<string>);
    int name_index(string);

    int server_;
    int buflen_;
    char* buf_;
    vector<Storage> users;
};
