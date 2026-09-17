# RDS HA and Read Scaling Architecture

```mermaid
flowchart TD
    A[Application / EC2] --> B[RDS Primary]
    B -. Synchronous replication .-> C[RDS Standby in another AZ]
    B -. Asynchronous replication .-> D[RDS Read Replica]
    C --> E[Automatic failover managed by RDS]
    D --> F[Read-only workloads]
    D --> G[Manual replica promotion]
```

- The primary handles normal reads and writes.
- The standby supports high availability and is not a normal read endpoint.
- Multi-AZ standby replication is synchronous and managed by RDS.
- A Read Replica receives changes asynchronously and can serve read traffic.
- A Read Replica can be promoted into an independent database.
