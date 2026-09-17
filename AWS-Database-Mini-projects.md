# AWS Database Mini Projects

A practical collection of five hands-on AWS database projects built to strengthen understanding of database architecture, high availability, scalability, performance, caching, security, and cloud troubleshooting.

The goal of this repository is to demonstrate practical understanding of AWS database services and architecture patterns through implementation-focused projects.

---

## Projects

| Project | Topic | Main AWS Services / Technologies |
|---|---|---|
| [01 - RDS EC2 Application](./01-rds-ec2-application/) | EC2-hosted application connected to an Amazon RDS database | EC2, RDS, IAM, Security Groups, Python/Flask |
| [02 - RDS High Availability and Read Replica](./02-rds-high-availability-read-replica/) | High availability and read scaling using RDS features | RDS, Multi-AZ, Read Replica, EC2 |
| [03 - Aurora High Availability and Failover](./03-aurora-high-availability-failover/) | Aurora replication, endpoints, and failover | Amazon Aurora, RDS |
| [04 - DynamoDB Design and Performance](./04-dynamodb-design-performance/) | NoSQL data modeling and performance experimentation | DynamoDB, Partition Keys, Sort Keys, GSI, LSI |
| [05 - DynamoDB + ElastiCache for Valkey](./05-dynamodb-elasticache-valkey/) | Lazy loading and cache invalidation using a caching layer | DynamoDB, ElastiCache for Valkey, EC2, IAM, Python |

---

## Skills Demonstrated

- Amazon RDS configuration and database connectivity
- RDS Multi-AZ and Read Replica concepts
- Amazon Aurora replication and failover concepts
- DynamoDB data modeling and key design
- DynamoDB performance testing and access patterns
- ElastiCache for Valkey integration
- Lazy loading and cache-aside architecture
- Cache invalidation strategies
- EC2 administration and application hosting
- IAM roles, permissions, and least-privilege access
- Security Groups and network troubleshooting
- Database high availability and scalability concepts
- Python automation and AWS SDK usage
- Testing, documentation, and AWS resource cleanup

---

## Repository Structure

```text
aws-database-mini-projects/
│
├── README.md
│
├── 01-rds-ec2-application/
│   ├── README.md
│   └── ...
│
├── 02-rds-high-availability-read-replica/
│   ├── README.md
│   └── ...
│
├── 03-aurora-high-availability-failover/
│   ├── README.md
│   └── ...
│
├── 04-dynamodb-design-performance/
│   ├── README.md
│   └── ...
│
└── 05-dynamodb-elasticache-valkey/
    ├── README.md
    └── ...
```

Each project contains its own documentation, implementation details, and test evidence where applicable.

---

## Approach

For each database project, the workflow generally included:

1. Understanding the AWS service or architecture.
2. Creating and configuring the required AWS resources.
3. Applying appropriate IAM and network-security controls.
4. Implementing or testing the solution.
5. Troubleshooting configuration and permission issues.
6. Capturing evidence through screenshots and test results.
7. Documenting the implementation and cleanup process.
8. Removing unused AWS resources to avoid unnecessary charges.

---

## Technologies Used

- **Cloud:** Amazon Web Services
- **Compute:** Amazon EC2
- **Relational Databases:** Amazon RDS, Amazon Aurora
- **NoSQL Database:** Amazon DynamoDB
- **Caching:** ElastiCache for Valkey
- **Networking:** VPC, Security Groups, Subnets
- **Security:** AWS IAM
- **Automation:** Python, Boto3
- **Version Control:** Git and GitHub

---

## Learning Outcomes

Through these projects, I worked on practical database scenarios involving:

- Connecting applications hosted on EC2 to managed databases
- Understanding RDS high availability and read scaling
- Exploring Aurora replication and failover behavior
- Designing DynamoDB tables and access patterns
- Understanding database and caching responsibilities
- Implementing cache hits, cache misses, and invalidation
- Applying IAM and network-security controls
- Troubleshooting connectivity and permission issues
- Documenting implementation steps and test results
- Practicing AWS cost awareness and resource cleanup

---

## Disclaimer

These projects were created for learning, experimentation, and portfolio development. Resource configurations may be simplified compared with production environments.

AWS resources should be deleted or stopped after testing to avoid unexpected costs.

---

## Author

**Tejas Shinkar**

AWS | Cloud | DevOps | Python | Linux | Infrastructure Automation
