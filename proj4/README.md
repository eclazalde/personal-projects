I used Dr. Zappalas echo code as a base. I parse the request in handleClient()
The responses are crafted in the requests.py and sent back to handleClient()
where they are sent. I also added a c_close and cleaup method to handle 
socket closing, marking and sweeping.

Non-blocking I/O
I used non-blocking I/O for the server and clients. For the server
I use non-blocking in the handle server method, lines 96-104 and return
if it would block. For the clients I use it for the recv() on lines 112-119
and return if there is nothing to revieve. I also use it on the send on
lines 143-148 and retry if the send blocks or would block.

Timeouts
I used a mark and sweep for the timeouts. When and fd gets polled I mark the
time after it has been handled on line 78. On lines 59-63 I get the time
between polls and if the timeout time has passed I call cleanup(). Cleanup()
checks if the last used time of the fd is greater than the timeout time and
closes the socket is more has passed.

Caching
In line 113 I get the data from recv() and on lines 121-126 I append it to
existing data for that fd if there is any. I then check that to see if there
is a valid message and handle it.