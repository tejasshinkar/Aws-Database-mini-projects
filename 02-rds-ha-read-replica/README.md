# Project 2 — Amazon RDS High Availability and Read Scaling

## Project overview

This project is a **design-focused AWS database architecture exercise** covering two different ways of improving an Amazon RDS database environment:

1. **Multi-AZ deployment** for high availability and automatic failover.
2. **Read Replicas** for increasing read capacity and distributing read-heavy workloads.

No billable Multi-AZ or Read Replica deployment is required for this project. The goal is to understand the architecture, traffic flow, operational behavior, and trade-offs before implementing it in a production environment.

---

## Business scenario

Imagine an application that stores customer accounts, orders, payments, and product information in an Amazon RDS database.

The application has two important requirements:

- The database should remain available if the underlying Availability Zone or primary database instance fails.
- The application should handle a growing number of read requests without placing all read traffic on the primary database.

A single RDS instance can become a single point of failure and may also become a bottleneck when read traffic increases.

This project designs a database architecture that addresses both problems.

---

## Learning objectives

By completing this project, you should be able to explain:

- What Multi-AZ means in Amazon RDS.
- The difference between a primary instance and a standby instance.
- How synchronous replication supports high availability.
- What happens during an RDS failover.
- Why the application should use the RDS endpoint instead of an instance IP address.
- What a Read Replica is.
- How asynchronous replication works.
- Why Read Replicas are useful for read-heavy applications.
- The difference between a Multi-AZ standby and a Read Replica.
- How a Read Replica can be promoted.
- Why Multi-AZ and Read Replicas solve different problems.
- What cost and operational considerations must be evaluated before deployment.

---

## Proposed architecture

The application uses the RDS primary endpoint for normal database operations.

- **Write traffic** goes to the primary database.
- **Read traffic** that can tolerate replication lag may be directed to a Read Replica.
- A **Multi-AZ standby** exists for availability and failover, but it is not used as a normal read endpoint.
- If the primary instance fails, RDS can promote the standby and keep the database endpoint associated with the deployment.

See `architecture/architecture.png` for the visual design and `architecture/architecture.md` for the detailed explanation.

---

## Multi-AZ deployment

A Multi-AZ deployment maintains a primary database instance and a standby instance in a different Availability Zone.

### Main characteristics

- The primary handles normal application traffic.
- The standby is maintained for failover.
- Replication between primary and standby is synchronous.
- The standby is not intended for normal application reads.
- If the primary fails, RDS can perform an automatic failover.
- The application should connect through the RDS DNS endpoint rather than a hard-coded IP address.

### What Multi-AZ protects against

Multi-AZ is primarily designed to improve:

- Availability during infrastructure failure.
- Resilience against an Availability Zone problem.
- Recovery from certain database-instance failures.
- Operational continuity through managed failover.

Multi-AZ is **not primarily a read-scaling feature**.

---

## Read Replicas

A Read Replica is a separate database instance that receives changes from the source database through asynchronous replication.

### Main characteristics

- The source database continues to handle writes.
- The replica can serve read-only workloads.
- Replication is asynchronous.
- Replication lag is possible.
- Applications should send only suitable read operations to the replica.
- A replica can be promoted to become an independent writable database instance.

### Suitable workloads

Read Replicas can be useful for:

- Reporting dashboards.
- Analytics queries.
- Search or browsing pages.
- Read-heavy APIs.
- Background jobs that do not require the newest committed data.
- Offloading expensive read queries from the primary.

### Important limitation

A Read Replica is not automatically a replacement for Multi-AZ. If the source database fails, the replica may need to be promoted manually or through an application-specific recovery process, and it may not contain the very latest data because replication is asynchronous.

---

## Multi-AZ versus Read Replica

| Area | Multi-AZ standby | Read Replica |
|---|---|---|
| Primary purpose | High availability and failover | Read scaling and workload distribution |
| Replication | Synchronous | Asynchronous |
| Normal read traffic | Not intended for application reads | Designed for read workloads |
| Automatic failover | Supported by RDS | Not the same as Multi-AZ automatic failover |
| Replication lag | Designed to maintain synchronous standby state | Possible |
| Can be promoted | Failover promotes the standby | Can be promoted into an independent database |
| Main benefit | Reduced downtime | Increased read capacity |
| Main trade-off | Additional infrastructure cost | Extra cost and eventual-consistency considerations |

---

## Example request flow

### Write request

1. A user creates an order.
2. The application sends the write request to the RDS primary endpoint.
3. The primary database commits the transaction.
4. The Multi-AZ standby is synchronously maintained by RDS.

### Read request

1. A user opens an order-history page.
2. The application determines whether slightly stale data is acceptable.
3. If acceptable, the application sends the read request to a Read Replica.
4. If fresh data is required, the application reads from the primary.

---

## Failover behavior

A simplified failover sequence is:

1. RDS detects a failure affecting the primary.
2. RDS promotes the standby instance.
3. The database role changes so the standby becomes the new primary.
4. The RDS endpoint is redirected to the new primary.
5. The application reconnects using the same endpoint.

The application must still handle:

- Existing connection failures.
- Connection retries.
- Transaction retry logic where appropriate.
- Short periods of unavailability during failover.
- Connection-pool refresh behavior.

---

## Read Replica promotion

Promotion may be used when:

- A replica must become an independent database.
- A separate environment is needed for a workload.
- A recovery or migration strategy requires a new primary.
- A read replica needs to be converted into a writable database.

Promotion is not instantaneous and should be treated as an operational event requiring validation.

---

## Cost and Free Tier considerations

This project is intentionally documentation-focused because Multi-AZ deployments and Read Replicas can create additional charges.

Before implementing the architecture in AWS, verify:

- Instance-hour pricing.
- Storage pricing.
- Backup storage.
- Data transfer.
- Cross-AZ traffic considerations.
- Whether the selected engine and configuration qualify for any current Free Tier offer.
- Whether the environment has been deleted after testing.

The design can be understood without leaving billable database instances running.

---

## Validation checklist

- [ ] I can explain the purpose of Multi-AZ.
- [ ] I can explain why the standby is not used as a normal read endpoint.
- [ ] I can explain synchronous versus asynchronous replication.
- [ ] I can explain what happens during failover.
- [ ] I can explain why applications use the RDS endpoint.
- [ ] I can explain when to use a Read Replica.
- [ ] I can describe replication lag.
- [ ] I can explain Read Replica promotion.
- [ ] I can distinguish high availability from read scaling.
- [ ] I can identify the cost risks of deploying both features.

---

## Suggested interview explanation

> Multi-AZ and Read Replicas solve different problems. Multi-AZ improves availability by maintaining a standby in another Availability Zone and supporting managed failover. A Read Replica improves read scalability by asynchronously copying data to another instance that can serve read workloads. In a production design, I would use the primary endpoint for writes and consistency-sensitive reads, route suitable read-heavy operations to replicas, and use Multi-AZ to reduce downtime during infrastructure failures.

---

## Project outcome

The final outcome is a documented RDS architecture and a clear understanding of:

- High availability,
- Failover,
- Replication,
- Read scaling,
- Endpoint behavior,
- Operational trade-offs, and
- Cost-aware AWS design.
