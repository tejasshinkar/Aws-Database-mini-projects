# AWS Cloud & DevOps Mini Projects

A practical collection of hands-on AWS projects built while developing skills in **Cloud Engineering, DevOps, infrastructure, automation, security, and troubleshooting**.

The goal of this repository is to demonstrate practical understanding of AWS services through implementation-focused mini-projects rather than only theoretical learning.

---

## Projects

| Project | Topic | Main AWS Services / Technologies |
|---|---|---|
| [Project 1 — Server Data Archival](./project-1-server-data-archival/) | Automated archival of old server files to object storage | Amazon S3, EC2, IAM, Python, Boto3 |
| [Project 2 — Highly Available Web Application](./project-2-high-availability-web-app/) | Load-balanced and self-healing web application | EC2, Application Load Balancer, Auto Scaling, Launch Templates, CloudWatch, Multi-AZ |
| [Project 3 — VPC Networking](./project-3-vpc-networking/) | Designing and testing AWS network infrastructure | VPC, Subnets, Route Tables, Internet Gateway, Security Groups, Network ACLs |
| [Project 4 — Serverless REST API](./project-4-serverless-rest-api/) | Building and testing a serverless API workflow | AWS Lambda, API Gateway, IAM, Python |
| [Project 5 — DynamoDB + Valkey Caching](./project-5-dynamodb-valkey/) | Implementing lazy loading and cache invalidation | DynamoDB, ElastiCache for Valkey, EC2, IAM, Python, Redis |

> **Note:** Update the folder names in this table if your local project directories use different names.

---

## Skills Demonstrated

- AWS resource provisioning and configuration
- IAM roles, policies, and least-privilege access
- EC2 instance administration
- S3 object storage and lifecycle concepts
- VPC networking and security controls
- Load balancing and Auto Scaling
- Serverless application concepts
- DynamoDB data access
- Redis/Valkey caching patterns
- Cache-aside / lazy-loading architecture
- Cache invalidation
- Python automation with Boto3
- Troubleshooting AWS permissions and connectivity
- Testing and documenting cloud infrastructure
- Cost awareness and resource cleanup

---

## Repository Structure

```text
aws-cloud-devops-mini-projects/
│
├── README.md
│
├── project-1-server-data-archival/
│   ├── README.md
│   ├── src/
│   └── docs/
│
├── project-2-high-availability-web-app/
│   ├── README.md
│   └── docs/
│
├── project-3-vpc-networking/
│   ├── README.md
│   └── docs/
│
├── project-4-serverless-rest-api/
│   ├── README.md
│   └── docs/
│
└── project-5-dynamodb-valkey/
    ├── README.md
    ├── src/
    ├── tests/
    └── docs/
```

Each project contains its own documentation, implementation files, test evidence, and architecture diagrams where applicable.

---

## Approach

For each project, the workflow generally included:

1. Understanding the AWS service or architecture.
2. Creating and configuring the required AWS resources.
3. Applying appropriate IAM and network-security controls.
4. Implementing or testing the solution.
5. Troubleshooting configuration and permission issues.
6. Capturing evidence through screenshots and test results.
7. Documenting the implementation and cleanup process.
8. Removing unused AWS resources to avoid unnecessary charges.


## Technologies Used

- **Cloud:** Amazon Web Services
- **Compute:** Amazon EC2
- **Storage:** Amazon S3, EBS
- **Networking:** Amazon VPC, Security Groups, Route Tables
- **Databases:** Amazon DynamoDB
- **Caching:** ElastiCache for Valkey
- **Serverless:** AWS Lambda, API Gateway
- **Scalability:** Application Load Balancer, Auto Scaling
- **Monitoring:** Amazon CloudWatch
- **Automation:** Python, Boto3
- **Version Control:** Git and GitHub

---

## Learning Outcomes

Through these projects, I worked on practical cloud scenarios involving:

- Secure AWS access using IAM roles
- Infrastructure configuration and validation
- Network connectivity and security-group troubleshooting
- High availability and scalability
- Object archival and idempotent automation
- Serverless request handling
- Database access patterns
- Cache hits, cache misses, and invalidation
- Operational documentation and cleanup discipline

---

## Disclaimer

These projects were created for learning, experimentation, and portfolio development. Resource configurations may be simplified compared with production environments.

AWS resources should be deleted or stopped after testing to avoid unexpected costs.

---

## Author

**Tejas Shinkar**

AWS | Cloud | DevOps | Python | Linux | Infrastructure Automation
