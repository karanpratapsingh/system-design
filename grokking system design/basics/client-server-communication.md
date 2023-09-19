Client-Server Communication
====

## Standard HTTP Web Request
1. Client opens a connection and requests data from server.
2. Server calculates the response.
3. Server sends the response back to the client on the opened request.

## Ajax Polling
The client repeatedly polls (or requests) a server for data, and waits for the server to respond with data. If no data is available, an empty response is returned.

1. Client opens a connection and requests data from the server using regular HTTP.
2. The requested webpage sends requests to the server at regular intervals (e.g., 0.5 seconds).
3. The server calculates the response and sends it back, like regular HTTP traffic.
4. Client repeats the above three steps periodically to get updates from the server.

Problems
- Client has to keep asking the server for any new data.
- A lot of responses are empty, creating HTTP overhead.

## HTTP Long-Polling
The client requests information from the server exactly as in normal polling, but with the expectation that the server may not respond immediately.

1. The client makes an initial request using regular HTTP and then waits for a response.
2. The server delays its response until an update is available, or until a timeout has occurred.
3. When an update is available, the server sends a full response to the client.
4. The client typically sends a new long-poll request, either immediately upon receiving a response or after a pause to allow an acceptable latency period.

Each Long-Poll request has a timeout. The client has to reconnect periodically after the connection is closed, due to timeouts.

## WebSockets
- A persistent full duplex communication channels over a single TCP connection. Both server and client can send data at any time.
- A connection is established through WebSocket handshake.
- Low communication overhead.
- Real-time data transfer.

## Server-Sent Event (SSE)
1. Client requests data from a server using regular HTTP.
2. The requested webpage opens a connection to the server.
3. Server sends the data to the client whenever there’s new information available.

- Use case:
  - When real-time traffic from server to client is needed.
  - When server generates data in a loop and sends multiple events to client.
