#include "client.h"

Client::Client() {
    // setup variables
    buflen_ = 1024;
    buf_ = new char[buflen_+1];
}

Client::~Client() {
}

void Client::run() {
    // connect to the server and run echo program
    create();
    //echo();
    messaging();
}

void
Client::create() {
}

void
Client::close_socket() {
}

void
Client::messaging() {
    bool go = true;
    while (go) {
        string message = "";
        string line;
        cout << "% ";
        if(getline(cin, line)) {
            vector<string> tokens = split(line, ' ');
            string valid = validate_command(tokens);
            if(valid.compare("quit") == 0) {
                go = false;
                message = "bad";
            }
            else if(valid.compare("send") == 0) {
                string body = "";
                cout << "- Type your message. End with a blank line -" << endl;
                while (getline(cin, line)) {
                    if(line.compare("") == 0) {
                        break;
                    }
                    else {
                        body += line + "\n";
                    }
                }
                int len =  body.length() - 1;
                ostringstream convert;
                convert << len;
                string m = body.substr(0, body.size()-1);
                message = "put " + tokens[1] + " " + tokens[2] + " " + convert.str() + "\n" + m;
                //cout << message << endl;
            }
            else if(valid.compare("list") == 0) {//f
                message = "list " + tokens[1] + "\n";
                //cout<< message <<endl;
            }
            else if(valid.compare("read") == 0) {
                message = "get " + tokens[1] + " " + tokens[2] + "\n";
                //cout<< message <<endl;
            }
            else if(valid.compare("reset") == 0) {
                message = "reset\n";
                //cout<< message <<endl;
            }
            else {
                message = "bad";
                cout << "Please use the correct format: send [user] subject, list [user], read [user] [index]" << endl;
            }
            
            if(message.compare("bad") != 0) {
                bool success = send_request(message);
                if (not success)
                    break;
                // get a response
                string response = get_response();
                // break if an error occurred
                if (response.empty())
                    break;
                string display = format_response(response);
                cout<< display <<endl;
            }
        }
    }
    close_socket();
}

bool
Client::send_request(string request) {
    // prepare to send request
    const char* ptr = request.c_str();
    int nleft = request.length();
    int nwritten;
    // loop to be sure it is all sent
    while (nleft) {
        if ((nwritten = send(server_, ptr, nleft, 0)) < 0) {
            if (errno == EINTR) {
                // the socket call was interrupted -- try again
                continue;
            } else {
                // an error occurred, so break out
                perror("write");
                return false;
            }
        } else if (nwritten == 0) {
            // the socket is closed
            return false;
        }
        nleft -= nwritten;
        ptr += nwritten;
    }
    return true;
}

string
Client::get_response() {
    string response = "";
    string message = "";
    int length;
    // read until we get a newline
    while (response.find("\n") == string::npos) {
        int nread = recv(server_,buf_,1024,0);
        if (nread < 0) {
            if (errno == EINTR)
                // the socket call was interrupted -- try again
                continue;
            else
                // an error occurred, so break out
                return "";
        } else if (nread == 0) {
            // the socket is closed
            return "";
        }
        // be sure to use append in case we have binary data
        response.append(buf_,nread);
    }
    int loc = response.find('\n');
    string command = response.substr(0, loc);
    vector<string> tokens = split(command, ' ');
    if(tokens.size() == 3) {
        length = atoi(tokens[2].c_str());
        message = response.substr(loc, response.size()-1);
        length -= message.size();
        while(length > 0) {
            int nread = recv(server_,buf_,1024,0);
            if (nread < 0) {
                if (errno == EINTR)
                    // the socket call was interrupted -- try again
                    continue;
                else
                    // an error occurred, so break out
                    return "";
            } else if (nread == 0) {
                // the socket is closed
                return "";
            }
            // be sure to use append in case we have binary data
            message.append(buf_,nread);
            length -= nread;
            usleep(5);
        }
        response = command + message;
    }
    // a better server would cut off anything after the newline and
    // save it in a cache
    return response;
}

string
Client::format_response(string response) {
    vector<string> lines = split(response, '\n');
    vector<string> tokens = split(lines[0], ' ');
    if(tokens.size() < 1) {
        return "Error: No message recieved\n";
    }
    else if(tokens[0].compare("OK") == 0) {
        return "OK\n";
    }
    else if(tokens[0].compare("list") == 0) {
        string message = "";
        for(int i = 1 ; i < lines.size() ; i++) {
            message += lines[i] + "\n";
        }
        return message;
    }
    else if(tokens[0].compare("message") == 0) {
        string message = "";
        for(int i = 1 ; i < lines.size() ; i++) {
            message += "\n" + lines[i];
        }
        return tokens[1] + message;
    }
    else if(tokens[0].compare("error") == 0) {
        string err_message = "";
        for(int i = 1 ; i < tokens.size() ; i++) {
            err_message += " " + tokens[i];
        }
        return "Error:" + err_message;
    }
    else {
        return "Error: Can't understand what the server sent.";
    }
}

string
Client::validate_command(vector<string> tokens) {
    if(tokens.size() < 1) {
        return "invalid1";
    }
    else if(tokens[0].compare("send") == 0) {
        if(tokens.size() == 3) {
            return "send";
        }
        else {
            return "invalid2";
        }
    }
    else if(tokens[0].compare("list") == 0) {
        if(tokens.size() == 2) {
            return "list";
        }
        else {
            return "invalid3";
        }
    }
    else if(tokens[0].compare("read") == 0) {
        if(tokens.size() == 3) {
            return "read";
        }
        else {
            return "invalid4";
        }
    }
    else if(tokens[0].compare("reset") == 0) {
        if(tokens.size() == 1) {
            return "reset";
        }
        else {
            return "invalid5";
        }
    }
    else if(tokens[0].compare("quit") == 0) {
        if(tokens.size() == 1) {
            return "quit";
        }
        else {
            return "invalid6";
        }
    }
    else {
        return "invalid7";
    }
}

vector<string>
Client::split(string s, char delim) {
    stringstream ss(s);
    string item;
    vector<string> elems;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}
