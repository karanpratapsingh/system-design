# URL Shortening Service

## Summary
![overview](../img/short-url-overview.png)
![summary](../img/short-url-detail.png)

## Requirements
- Functional Requirements
  - Given a URL, generate a shorter and unique alias (short link).
  - When users access a short link, redirect to the original link.
  - Users should optionally be able to pick a custom short link for their URL.
  - Links will expire after a standard default timespan. Users should also be able to specify the expiration time.

- Non-Functional Requirements
  - The system should be highly available. This is required because, if our service is down, all the URL redirections will start failing.
  - URL redirection should happen in real-time with minimal latency.
  - Shortened links should not be guessable (not predictable).

- Extended Requirements
  - Analytics; e.g., how many times a redirection happened?
  - Be accessible through REST APIs by other services.

## Capacity Estimation and Constraints
- Assumption
  - Read-heavy. More redirection requests compared to new URL shortenings.
  - Assume **100:1** ratio between read and write.

- Traffic estimates
  - **500M** new URL shortenings per month, 100 * 500M => 50B redirections per month.
  - New URL shortenings per second
    - 500 million / (30 days * 24 hours * 3600 seconds) = **~200 URLs/s**
  - URLs redirections per second
    - 50 billion / (30 days * 24 hours * 3600 sec) = **~19K/s**

- Storage estimates
  - Assume storing every URL shortening request for 5 years, each object takes **500 bytes**
  - Total objects: 500 million * 5 years * 12 months = **30 billion**
  - Total storage: 30 billion * 500 bytes = **15 TB**

- Bandwidth estimates
  - Write: 200 URL/s * 500 bytes/URL = **100 KB/s**
  - Read: 19K URL/s * 500 bytes/URL = **~9 MB/s**

- Cache memory estimates
  - Follow the 80-20 rule, assuming 20% of URLs generate 80% of traffic, cache 20% hot URLs
  - Requests per day: 19K * 3600 seconds * 24 hours = **~1.7 billion/day**
  - Cache 20%: 0.2 * 1.7 billion * 500 bytes = **~170GB**

- Summary
  - Assuming 500 million new URLs per month and 100:1 read:write ratio
  
  Category | Calculation | Estimate
  ---- | ---- | ----
  New URLs | 500 million / (30 days * 24 hours * 3600 seconds) | 200 /s
  URL redirections | 500 million * 100 / (30 days * 24 hours * 3600 seconds) | 19 K/s
  Incoming data | 500 bytes/URL * 200 URL/s | 100 KB/s
  Outgoing data | 500 bytes/URL * 19K URL/s | 9 MB/s
  Storage for 5 years | 500 bytes/URL * 500 million * 60 months | 15 TB
  Memory for cache | 19K URL * 3600 seconds * 24 hours * 500 bytes * 20% | 170 GB

## System APIs
### `createUrl`
- Parameters
  Name | Type | Note
  ---- | ---- | ----
  `api_dev_key` | `string` | The API developer key of a registered account. This will be used to, among other things, throttle users based on their allocated quota.
  `original_url` | `string` | Original URL to be shortened.
  `custom_alias` | `string` | Optional custom key for the URL.
  `user_name` | `string` | Optional user name to be used in encoding.
  `expire_date` | `string` | Optional expiration date for the shortened URL.
- Return
  - `string`
  - A successful insertion returns the shortened URL; otherwise, it returns an error code.

### `deleteUrl`
- Parameters
  Name | Type | Note
  ---- | ---- | ----
  `api_dev_key` | `string` | The API developer key of a registered account. This will be used to, among other things, throttle users based on their allocated quota.
  `url_key` | `string` | Short URL.
- Return
  - `string`
  - A successful deletion returns ‘URL Removed’.

## Database design
- Observations
  - Need to store billions of records.
  - Each object is small (less than 1K).
  - No relationships between records—other than storing which user created a URL.
  - Read-heavy.
  - A [NoSQL](../basics/sql-vs-nosql.md) choice would also be easier to scale.
  - Comment: SQL with sharding should also work

- Schema
  - URL
    Column | Type
    ---- | ----
    `hash` | varchar(16)
    `original_url` | varchar(512)
    `creation_date` | datetime
    `expiration_date` | datetime
    `user_id` | int
  - User
    Column | Type
    ---- | ----
    `name` | varchar(20)
    `email` | varchar(32)
    `creation_date` | datetime
    `last_login` | datetime

## Basic System Design and Algorithm
### Encoding actual URL
- Compute unique hash
  - `base64`: A-Z, a-z, 0-9, `-`, `.`
  - 6 letters: 64 ^ 6 = ~68.7 billion
  - 8 letters: 64 ^ 8 = ~281 trillion
  - Use 6 letters
  - `MD5` generates 128 bit hash value
  - Each `base64` character encodes 6 bits
  - `base64` encoding generates 22 characters
  - Select 8 characters
- Issues with this approach
  - Same URL from multiple users
  - URL-encoded
- Workaround
  - Append an increasing sequence number to each input URL, and generate a hash for it
  - Append user id to input URL

### Generating keys offline
- Standalone Key Generation Service (KGS)
  - Generate random 6 letter strings and store them in a database (key DB)
  - When a short URL is needed, take one from the key DB

- Key DB size
  - 6 characters/key * 68.7B unique keys = 412 GB

- Concurrency issue
  - If there are multiple servers reading keys concurrently, two or more servers try to read the same key from the database.

- Workaround
  - Servers can use KGS to read/mark keys in the database.
  - KGS can use two tables to store keys: one for keys that are not used yet, and one for all the used keys.
  - KGS can always keep some keys in memory so that it can quickly provide them whenever a server needs them.
  - KGS needs to make sure not to give the same key to multiple servers.
  - Comment: keys are sharded. Each KGS server only serves one application server.

- Key lookup
  - When a key is found, issue an "HTTP 302 Redirect" status and passing the stored URL.
  - When a key is not found, issue an "HTTP 404 Not Found", or redirect to homepage.

### UUID
Replace KGS with UUID.

## Data Partitioning and Replication
- Range Based Partitioning
  - Store URLs in separate partitions based on the first letter of the URL or the hash key.
  - Combine certain less frequently occurring letters into one database partition.
- Problem with this approach
  - Unbalanced servers.

- Hash-Based Partitioning
  - Take a hash of the short URL we are storing, and calculate which partition to use based upon the hash.
  - Use [consistent hashing](../basics/consistent-hashing.md)

## Cache
- Eviction policy
  - LRU: discard the least recently used URL first
- Cache update
  - Cache miss: hit backend database and pass new entry to all cache replicas

## Load Balancer (LB)
- LB locations
  - Between Clients and Application servers
  - Between Application Servers and database servers
  - Between Application Servers and Cache servers

## DB Sweeping
A separate Cleanup service can run periodically to remove expired links from our storage and cache.

## Telemetry
Statistics about the system: how many times a short URL has been used

## Security and Permissions
- Store permission level (public/private) with each URL in the database
- Send an error (HTTP 401) for unauthorized access
