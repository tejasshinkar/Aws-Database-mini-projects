# Project 3 — Amazon Aurora High Availability and Failover

## Project overview

This project is a documentation-focused study of Amazon Aurora architecture,
high availability, replication, endpoint behaviour, failover, promotion, and
backup/recovery concepts.

The original idea was to deploy an Aurora MySQL cluster with a writer and two
readers. However, Aurora resources can generate charges, and Aurora MySQL
should not be assumed to be covered by the AWS Free Tier. Therefore, this
project documents the architecture and operational workflow without requiring
a continuously running Aurora cluster.

## Business scenario

Imagine a production application that requires:

- A highly available relational database.
- A writer database for inserts, updates, and deletes.
- Multiple reader instances for read-heavy workloads.
- Automatic routing of write traffic to the active writer.
- Reader routing for suitable read-only operations.
- A recovery process if the writer instance fails.
- Backup and point-in-time recovery capabilities.

Amazon Aurora addresses these requirements through a managed database cluster,
cluster endpoints, replication, and managed recovery features.

## Learning objectives

By completing this project, you should be able to explain:

- What an Aurora DB cluster is.
- The difference between a cluster, an instance, and a storage layer.
- The role of the writer instance.
- The role of Aurora Replicas.
- The writer endpoint.
- The reader endpoint.
- How Aurora replication supports read scaling.
- What happens during a failover.
- How a new writer is selected.
- Why applications should use endpoints instead of instance-specific addresses.
- The difference between failover and promotion.
- Backup and point-in-time recovery concepts.
- Why Aurora pricing must be checked before hands-on deployment.

## Aurora architecture

An Aurora cluster typically contains:

1. A shared, distributed cluster storage volume.
2. A writer DB instance.
3. Zero or more Aurora Replicas.
4. A writer endpoint.
5. A reader endpoint.
6. A cluster management and failover mechanism.

The writer handles changes to the database. Aurora Replicas can serve read
traffic and may become the writer during a failover.

## Writer endpoint

The writer endpoint points to the current primary/writer instance.

Use it for:

- INSERT operations
- UPDATE operations
- DELETE operations
- Transactions
- Reads that require the writer's current state

When a failover occurs, Aurora moves the writer role to another eligible
instance and the writer endpoint is updated to point to the new writer.

Applications should therefore connect through the writer endpoint rather than
hard-code a particular instance address.

## Reader endpoint

The reader endpoint distributes read connections across Aurora Replicas
and, depending on the cluster state and configuration, can route reads to
available reader instances.

Use it for:

- Read-heavy APIs
- Product browsing
- Reporting queries
- Dashboards
- Queries that can tolerate replica behaviour and routing changes

The reader endpoint should not be used for writes.

## Aurora Replicas and read scaling

Aurora Replicas are read-only instances that use the Aurora storage architecture
and can serve read workloads.

Adding replicas can:

- Increase read capacity.
- Reduce pressure on the writer.
- Improve workload isolation.
- Provide additional failover candidates.

However, replicas still have instance costs, and the application must consider
connection management, query routing, and consistency requirements.

## Failover workflow

A simplified failover sequence is:

1. Aurora detects that the writer is unavailable or a failover is initiated.
2. Aurora selects an eligible replica or instance as the failover target.
3. The selected instance becomes the new writer.
4. The writer endpoint is updated.
5. The application reconnects and retries safe operations where appropriate.

During failover, active connections may be interrupted. Applications should
use connection pooling, retry logic, and sensible timeout settings.

## Manual failover

A manual failover can be initiated for testing or operational purposes.

The purpose of a controlled failover exercise is to validate:

- Application reconnection.
- Endpoint behaviour.
- Connection-pool recovery.
- Monitoring and alerting.
- Retry logic.
- Operational runbooks.

A failover test should be planned carefully because it can temporarily interrupt
database connectivity.

## Failover versus promotion

### Failover

Failover changes which instance is the active writer within the Aurora cluster.
It is intended to restore writer availability.

### Promotion

Promotion is the process of changing a replica or another database instance
into a writer role. In Aurora, promotion tiers and instance eligibility can
influence which replica is selected during failover.

The terms are related but should not be treated as identical in every context.

## Backup and point-in-time recovery

Aurora provides automated backup capabilities that support recovery to a
specific time within the configured backup-retention period.

Important concepts include:

- Automated backups.
- Backup retention.
- Continuous backup data.
- Point-in-time recovery.
- Restoring to a new cluster.
- Testing recovery procedures.
- Recovery point objective (RPO).
- Recovery time objective (RTO).

A backup strategy should be tested rather than assumed to work. Recovery
validation should include application connectivity, schema availability,
data checks, and permissions.

## Endpoints and application design

A production application should avoid embedding a specific DB instance endpoint.

Recommended approach:

- Use the writer endpoint for writes and writer-consistent reads.
- Use the reader endpoint for suitable read-only traffic.
- Handle connection failures.
- Reconnect after failover.
- Avoid retrying non-idempotent operations blindly.
- Monitor replica health and application error rates.

## Cost considerations

Aurora resources can incur charges for:

- DB instance usage.
- Aurora storage.
- I/O or other engine-specific usage components.
- Backup storage beyond applicable allowances.
- Data transfer.
- Multiple reader instances.

Aurora MySQL should not be assumed to be free. Always verify the current AWS
pricing, Free Tier eligibility, and regional availability before deploying.

For this reason, this project remains documentation-focused.

## Suggested interview explanation

> Aurora uses a cluster architecture with a writer and optional Aurora Replicas.
> The writer endpoint always identifies the current writer, while the reader
> endpoint is used for read-oriented traffic. Replicas provide read scaling and
> additional failover candidates. If the writer fails, Aurora can promote an
> eligible replica and update the writer endpoint. Applications must reconnect
> through the endpoint and should be designed to tolerate brief connection
> interruptions.

## Validation checklist

- [ ] I can explain the Aurora cluster architecture.
- [ ] I can distinguish a writer from an Aurora Replica.
- [ ] I can explain the writer endpoint.
- [ ] I can explain the reader endpoint.
- [ ] I understand how replicas support read scaling.
- [ ] I can describe a failover sequence.
- [ ] I understand manual failover.
- [ ] I can distinguish failover from promotion.
- [ ] I understand backup and point-in-time recovery.
- [ ] I understand why Aurora costs must be checked before deployment.

## Project outcome

The project provides a practical conceptual foundation for designing an Aurora
cluster that supports high availability, read scaling, endpoint-based routing,
and recoverability without leaving potentially billable Aurora resources
running.
