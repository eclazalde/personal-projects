#include "storage.h"

Storage::Storage() {
    
}
Storage::~Storage() {
    
}

string
Storage::store(string name, string subject, string message) {
    this->name = name;
    this->subject.push_back(subject);
    this->message.push_back(message);
    if(this->subject.size() == this->message.size()) {
        return "OK\n";
    }
    else {
        return "error Internal error storing the subject and message.\n";
    }
}

string
Storage::list_tostring() {
    int size = this->subject.size();
    ostringstream convert;
    convert << size;
    string message = "list " + convert.str() + "\n";
    for(int i = 0 ; i < this->subject.size() ; i++) {
        ostringstream index;
        index << i + 1;
        message += index.str() + " " + subject[i] + "\n";
    }
    return message;
}

string
Storage::get_tostring(int index) {
    if(index > message.size() || index < 1) {
        return "error No message with that index.\n";
    }
    else {
        string m = message[index - 1].substr(0, message[index - 1].size()-1);
        int len =  m.length();
        ostringstream convert;
        convert << len;
        return "message " + subject[index - 1] + " " + convert.str() + "\n" + m;
    }
}

string
Storage::get_name() {
    return name;
}