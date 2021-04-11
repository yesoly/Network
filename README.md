# Network
20-1 CAUCSE Network Application and Design  
Socket Programming Homework

### HW2
- **Socket Programming with Header Information** 
- Client program should show a menu with five options, and take user input for the selection.
> option 1) convert text to UPPER-case letters.
> option 2) ask the server what is the IP address and port number of the client (myself).
> option 3) ask the server what the current time on the server is.
> option 4) ask the server program how long it has been running for since it started (unit: seconds).
> option 5) exit client program

### HW3
- **Socket Programming with Multiple Clients
- Two ways: Multi-thread method / Non-blocking socket method
- Give each client a unique number such as (client1, client2, client3, ..) when they connect
- Whenever a new client connects, or an existing client disconnects, print out the client number and
the number of clients as
- Client program should show a menu with five options, and take user input for the selection (Same as hw1)

### HW4
- **Simple Server-Client Chat App**
- `$ python3 ChatTCPClient.py (nickname)`
- If anyone chats `I hate professor`, the server must detect that, and disconnect
that client.
- Chat room commands
> `\users`                    // show the <nickname, IP, port> list of all users
> `\wh <nickname> <message>`  // whisper to <nickname>
> `\exit`                     // disconnect from server, and quit
> `\version`                  // show server's software version (& client software version)
> `\rename <nickname>`        // change my nickname
> `\rtt`                      // show RTT (round trip time) from the client to the server and back

### HW5
- **File Transfer in Chatting App**
- Chat room commands
> `\fsend <filename>`              // send <filename> to everyone
> ~~`wsend <filename> <nickname>`  // send <filename> to <nickname> only~~
