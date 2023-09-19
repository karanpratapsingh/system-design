Proxies
====

- A proxy server is an intermediary piece of hardware / software sitting between client and backend server.
  - Filter requests
  - Log requests
  - Transform requests (encryption, compression, etc)
  - [Cache](caching.md)
  - Batch requests
    - Collapsed forwarding: enable multiple client requests for the same URI to be processed as one request to the backend server
    - Collapse requests for data that is spatially close together in the storage to minimize the reads
