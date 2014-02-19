#pragma once

#include <errno.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>

#include <vector>
#include <sstream>

#include <fstream>
#include <iostream>
#include <string>

using namespace std;

class Client {
public:
    Client();
    ~Client();

    void run();

protected:
    virtual void create();
    virtual void close_socket();
    void messaging();
    bool send_request(string);
    string get_response();
    
    vector<string> split(string s, char delim);
    string validate_command(vector<string>);
    string format_response(string);
    
    int server_;
    int buflen_;
    char* buf_;
};
