#include "server.h"

Server::Server() {
    // setup variables
    buflen_ = 1024;
    buf_ = new char[buflen_+1];
}

Server::~Server() {
    delete buf_;
}

void
Server::handle(int client, vector<Storage> &u, sem_t &lock, sem_t &proc) {
    // loop to handle all requests
    while (1) {
        // get a request
        string request = get_request(client);
        // break if client is done or an error occurred
        if (request.empty())
            break;
        
        string response = read_request(request, u, lock, proc);

        // send response
        bool success = send_response(client,response);
        // break if an error occurred
        if (not success)
            break;
    }
    close(client);
}

string
Server::get_request(int client) {
    string request = "";
    string message = "";
    int length;
    // read until we get a newline
    while (request.find("\n") == string::npos) {
        int nread = recv(client,buf_,1024,0);
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
        request.append(buf_,nread);
    }
    int loc = request.find('\n');
    string command = request.substr(0, loc);
    vector<string> tokens = split(command, ' ');
    if(tokens.size() == 4) {
        length = atoi(tokens[3].c_str());
        message = request.substr(loc, request.size()-1);
        length -= message.size();
        while(length > 0) {
            int nread = recv(client,buf_,1024,0);
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
        request = command + message;
    }
    // a better server would cut off anything after the newline and
    // save it in a cache
    return request;
}

bool
Server::send_response(int client, string response) {
    // prepare to send response
    const char* ptr = response.c_str();
    int nleft = response.length();
    int nwritten;
    // loop to be sure it is all sent
    while (nleft) {
        if ((nwritten = send(client, ptr, nleft, 0)) < 0) {
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
Server::read_request(string request, vector<Storage> &users, sem_t &lock, sem_t &proc) {
    vector<string> lines = split(request, '\n');
    vector<string> tokens = split(lines[0], ' ');
    if(tokens.size() < 1) {
        return "error No message recieved\n";
    }
    else if(tokens[0].compare("put") == 0) {
        if(tokens.size() == 4) {
            string message = get_message(lines);
            sem_wait(&proc);
            sem_wait(&lock);
            int index = name_index(tokens[1], users);
            string status;
            if(index == -1) {
                Storage temp;
                users.push_back(temp);
                status = users.back().store(tokens[1], tokens[2], message);
            }
            else {
                status = users[index].store(tokens[1], tokens[2], message);
            }
            sem_post(&lock);
            sem_post(&proc);
            return status;
        }
        else {
            return "error Put command has too many or to few arguments\n";
        }
    }
    else if(tokens[0].compare("list") == 0) {
        if(tokens.size() == 2) {
            sem_wait(&proc);
            sem_wait(&lock);
            int index = name_index(tokens[1], users);
            sem_post(&lock);
            sem_post(&proc);
            if(index == -1) {
                return "error Name not found.\n";
            }
            else {
                sem_wait(&proc);
                sem_wait(&lock);
                string message = users[index].list_tostring();
                sem_post(&lock);
                sem_post(&proc);
                return message;
            }
        }
        else {
            return "error List command has too many or to few arguments\n";
        }
    }
    else if(tokens[0].compare("get") == 0) {
        if(tokens.size() == 3) {
            sem_wait(&proc);
            sem_wait(&lock);
            int index = name_index(tokens[1], users);
            sem_post(&lock);
            sem_post(&proc);
            if(index == -1) {
                return "error Name not found.\n";
            }
            else {
                sem_wait(&proc);
                sem_wait(&lock);
                string message = users[index].get_tostring(atoi(tokens[2].c_str()));
                sem_post(&lock);
                sem_post(&proc);
                return message;
            }
        }
        else {
            return "error Get command has too many or to few arguments\n";
        }
    }
    else if(tokens[0].compare("reset") == 0) {
        if(tokens.size() == 1) {
            sem_wait(&proc);
            sem_wait(&lock);
            users.clear();
            sem_post(&lock);
            sem_post(&proc);
            return "OK\n";
        }
        else {
            return "error Reset command has too many or to few arguments\n";
        }
    }
    else {
        return "error Command not recognized. Must begin with put, list, get, reset.\n";
    }
}

vector<string>
Server::split(string s, char delim) {
    stringstream ss(s);
    string item;
    vector<string> elems;
    while (getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

string
Server::get_message(vector<string> lines) {
    string message = "";
    for(int i = 1 ; i < lines.size() ; i++) {
        message += lines[i] + "\n";
    }
    return message;
}

int
Server::name_index(string name, vector<Storage> &users) {
    int index = -1;
    int count = 0;
    bool found = false;
    while(!found && count < users.size()) {
        if(users[count].get_name().compare(name) == 0) {
            found = true;
            index = count;
        }
        else {
            count++;
        }
    }
    return index;
}
