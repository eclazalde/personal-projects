Data structures:
vector that stores the users and messages.
created msgd.cc line 26 vector<Storage> users;
used on server.cc lines 127-136, 149, 158, 172, 181,195.
uses sem_t lock for the locking;
uses sem_t proc for the waiting threads;
The vector is the place where I save the users. The storage object is each user and their messages. Because we weren't required to thread safe individual users I don't have any sycronization in the Storage class. The locks on the users vector covers that data.

vector that stores the connections:
created msgd.cc line 27 queue<int> conns;
used on msgd.cc lines 101 (push) and 119,120 (pop)
uses sem_t que for the waiting threads
uses sem_t mutex for the locking