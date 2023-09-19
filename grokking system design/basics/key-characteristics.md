# Key Characteristics of Distributed Systems

## Scalability
- The capability of a system to grow and manage increased demand.
- A system that can continuously evolve to support growing amount of work is scalable.
- Horizontal scaling: by adding more servers into the pool of resources.
- Vertical scaling: by adding more resource (CPU, RAM, storage, etc) to an existing server. This approach comes with downtime and an upper limit.

## Reliability
- Reliability is the probability that a system will fail in a given period.
- A distributed system is reliable if it keeps delivering its service even when one or multiple components fail.
- Reliability is achieved through redundancy of components and data (remove every single point of failure).

## Availability
- Availability is the time a system remains operational to perform its required function in a specific period.
- Measured by the percentage of time that a system remains operational under normal conditions.
- A reliable system is available.
- An available system is not necessarily reliable.
  - A system with a security hole is available when there is no security attack.

## Efficiency
- Latency: response time, the delay to obtain the first piece of data.
- Bandwidth: throughput, amount of data delivered in a given time.

## Serviceability / Manageability
- Easiness to operate and maintain the system.
- Simplicity and spend with which a system can be repaired or maintained.
