#include <stdlib.h>
#include <unistd.h>
#include <iostream>

#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <unistd.h>
#include <queue>
#include "storage.h"
#include "server.h"

using namespace std;

void* worker(void*);

sem_t que;
sem_t mutex;
// structure to hold data passed to a thread
typedef struct thdata_ {
    sem_t lock;
    sem_t proc;
    vector<Storage> users;
    queue<int> conns;
} thdata;

int
main(int argc, char **argv)
{
    struct sockaddr_in server_addr,client_addr;
    socklen_t clientlen = sizeof(client_addr);
    int option, port, reuse;
    int server, client;

    // setup default arguments
    port = 3000;

    // process command line options using getopt()
    // see "man 3 getopt"
    while ((option = getopt(argc,argv,"p:")) != -1) {
        switch (option) {
            case 'p':
                port = atoi(optarg);
                break;
            default:
                cout << "server [-p port]" << endl;
                exit(EXIT_FAILURE);
        }
    }
    
      // setup socket address structure
    memset(&server_addr,0,sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = INADDR_ANY;
      // create socket
    server = socket(PF_INET,SOCK_STREAM,0);
    if (!server) {
        perror("socket");
        exit(-1);
    }
      // set socket to immediately reuse port when the application closes
    reuse = 1;
    if (setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("setsockopt");
        exit(-1);
    }
      // call bind to associate the socket with our local address and
      // port
    if (bind(server,(const struct sockaddr *)&server_addr,sizeof(server_addr)) < 0) {
        perror("bind");
        exit(-1);
    }
      // convert the socket to listen for incoming connections
    if (listen(server,SOMAXCONN) < 0) {
        perror("listen");
        exit(-1);
    }
    
    thdata* data = new thdata;
    std::vector<pthread_t*> threads;
    sem_init(&que, 0, 0);
    sem_init(&mutex, 0, 1);
    
    sem_init(&data->proc, 0, 1);
    sem_init(&data->lock, 0, 1);
    
    for (int i = 0; i < 10; i++) { // change to 10 after
        // Create 10 threads
        pthread_t* thread = new pthread_t;
        pthread_create(thread, NULL, &worker, (void *) data);
        threads.push_back(thread);
    }
      // accept clients
    while (true){ //(client = accept(server,(struct sockaddr *)&client_addr,&clientlen)) > 0) {
        client = accept(server,(struct sockaddr *)&client_addr,&clientlen);
        sem_wait(&mutex);
        data->conns.push(client);
        sem_post(&mutex);
        sem_post(&que);
    }
            // wait for threads to terminate.
    for (int i=0; i<threads.size(); i++) {
        pthread_join(*threads[i], NULL);
        delete threads[i];
    }
    close(server);
}

void* worker(void* ptr) {
    thdata* data;
    data = (thdata*) ptr;
    while(1) {
        sem_wait(&que);
        sem_wait(&mutex);
        int c = data->conns.front();
        data->conns.pop();
        sem_post(&mutex);
        Server *s = new Server();
        s->handle(c, data->users, data->lock, data->proc);
    }
    
    pthread_exit(0);
}