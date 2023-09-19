Caching
====

- Take advantage of the locality of reference principle: recently requested data is likely to be requested again.
- Exist at all levels in architecture, but often found at the level nearest to the front end.

## Application server cache
- Cache placed on a request layer node.
- When a request layer node is expanded to many nodes
  - Load balancer randomly distributes requests across the nodes.
  - The same request can go to different nodes.
  - Increase cache misses.
  - Solutions:
    - Global caches
    - Distributed caches

## Distributed cache
- Each request layer node owns part of the cached data.
- Entire cache is divided up using a consistent hashing function.
- Pro
  - Cache space can be increased easily by adding more nodes to the request pool.
- Con
  - A missing node leads to cache lost.

## Global cache
- A server or file store that is faster than original store, and accessible by all request layer nodes.
- Two common forms
  - Cache server handles cache miss.
    - Used by most applications.
  - Request nodes handle cache miss.
    - Have a large percentage of the hot data set in the cache.
    - An architecture where the files stored in the cache are static and shouldn’t be evicted.
    - The application logic understands the eviction strategy or hot spots better than the cache

## Content distributed network (CDN)
- For sites serving large amounts of static media.
- Process
  - A request first asks the CDN for a piece of static media.
  - CDN serves that content if it has it locally available.
  - If content isn’t available, CDN will query back-end servers for the file, cache it locally and serve it to the requesting user.
- If the system is not large enough for CDN, it can be built like this:
  - Serving static media off a separate subdomain using lightweight HTTP server (e.g. Nginx).
  - Cutover the DNS from this subdomain to a CDN later.

## Cache invalidation
- Keep cache coherent with the source of truth. Invalidate cache when source of truth has changed.
- Write-through cache
  - Data is written into the cache and permanent storage at the same time.
  - Pro
    - Fast retrieval, complete data consistency, robust to system disruptions.
  - Con
    - Higher latency for write operations.
- Write-around cache
  - Data is written to permanent storage, not cache.
  - Pro
    - Reduce the cache that is no used.
  - Con
    - Query for recently written data creates a cache miss and higher latency.
- Write-back cache
  - Data is only written to cache.
  - Write to the permanent storage is done later on.
  - Pro
    - Low latency, high throughput for write-intensive applications.
  - Con
    - Risk of data loss in case of system disruptions.

## Cache eviction policies
- FIFO: first in first out
- LIFO: last in first out
- LRU: least recently used
- MRU: most recently used
- LFU: least frequently used
- RR: random replacement
