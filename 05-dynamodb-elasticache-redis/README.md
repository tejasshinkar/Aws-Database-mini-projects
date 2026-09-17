# Project 5 — DynamoDB + ElastiCache for Valkey: Lazy Loading and Cache Invalidation

## 1. Project Overview

This project demonstrates a cache-aside architecture using:

- **Amazon EC2** as the application host
- **Amazon DynamoDB** as the persistent source of truth
- **Amazon ElastiCache Serverless for Valkey** as the in-memory cache
- **Python** as the application language
- **IAM roles** for AWS authentication
- **Security groups** to restrict cache network access

The application stores and retrieves user records. Before reading from DynamoDB, it checks Valkey. If the requested record is already cached, the application returns it immediately. If the record is not cached, the application reads it from DynamoDB and stores it in Valkey with a five-minute TTL.

The project also demonstrates explicit cache invalidation after updates and deletions.

> **Cost warning:** ElastiCache Serverless for Valkey is not assumed to be free. Delete temporary AWS resources after completing the lab and collecting evidence.

---

## 2. Business Scenario

Imagine a user-profile service that receives frequent requests for the same user records.

Reading every request directly from DynamoDB can increase latency and create unnecessary database traffic. A cache can temporarily store frequently accessed records and reduce repeated database reads.

However, cached data can become stale when the original record changes.

This project addresses both problems:

1. Use **lazy loading** to populate the cache only when data is requested.
2. Use **TTL** to expire cached values automatically.
3. Use **explicit invalidation** after updates and deletions.

---

## 3. Architecture

The architecture follows the cache-aside pattern:

```text
                         ┌──────────────────────┐
                         │   Client Request     │
                         │      user-1          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Amazon EC2                    │
                    │ Amazon Linux + Python         │
                    │                              │
                    │ app.py                       │
                    │ cache_service.py              │
                    │ redis_client.py               │
                    │ dynamodb_client.py            │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
          ┌──────────────────┐          ┌────────────────────┐
          │ Valkey Cache     │          │ DynamoDB           │
          │                  │          │                    │
          │ user:user-1      │          │ project5-users     │
          │ TTL: 300 seconds │          │ PK: user_id        │
          └──────────────────┘          └────────────────────┘
                    ▲                              │
                    │                              │
                    └──────── Cache miss ──────────┘

Update/Delete flow:
DynamoDB mutation → Delete matching Valkey key → Next read reloads data
```

A PNG version of the architecture diagram is provided separately.

---

## 4. AWS Resources Used

| Resource | Configuration |
|---|---|
| EC2 | Amazon Linux 2023, t3.micro |
| Region | `ap-south-1` |
| VPC | Default VPC |
| EC2 security group | `project5-ec2-sg` |
| Valkey security group | `project5-redis-sg` |
| DynamoDB table | `project5-users` |
| DynamoDB key | `user_id` — String partition key |
| DynamoDB billing mode | `PAY_PER_REQUEST` |
| IAM role | `project5-ec2-dynamodb-role` |
| Cache engine | ElastiCache Serverless for Valkey |
| Cache port | `6379` |
| Cache encryption | TLS enabled |
| Cache TTL | `300` seconds |

---

## 5. IAM Design

The EC2 instance used an attached IAM role rather than hard-coded AWS access keys.

The role was scoped to the `project5-users` DynamoDB table and allowed these actions:

- `dynamodb:DescribeTable`
- `dynamodb:GetItem`
- `dynamodb:PutItem`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`
- `dynamodb:Query`

`dynamodb:Scan` was intentionally excluded.

An attempted table scan returned `AccessDenied`, which demonstrated that the role was following a least-privilege approach. The application used targeted `GetItem` requests instead of scanning the entire table.

---

## 6. Network and Security Design

The EC2 instance and Valkey cache were placed in the same default VPC.

The Valkey security group allowed:

```text
Protocol: TCP
Port: 6379
Source: project5-ec2-sg
```

Port `6379` was not opened to the public internet.

The cache used TLS, so the Python Redis client connected with `ssl=True`.

The SSH rule for the EC2 instance was temporarily opened broadly during the lab because the client public IP changed during connection attempts. This is not recommended for production. A production environment should use a restricted source IP, AWS Systems Manager Session Manager, or another controlled access method.

---

## 7. Project Structure

```text
project5-dynamodb-redis/
├── src/
│   ├── config.py
│   ├── dynamodb_client.py
│   ├── redis_client.py
│   ├── cache_service.py
│   └── app.py
├── tests/
│   ├── test_cache.py
│   ├── test_invalidation.py
│   ├── test_update_cache.py
│   └── test_delete_cache.py
├── docs/
│   ├── architecture/
│   │   └── project-5-dynamodb-valkey-architecture.png
│   └── screenshots/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 8. Python Environment Setup

Activate the virtual environment on EC2:

```bash
source ~/project5-dynamodb-redis/venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The required packages are:

```text
boto3
redis
```

The application uses the EC2 instance profile for DynamoDB authentication. No AWS access keys are required in the Python source code.

---

## 9. Configuration

Update `src/config.py` with the correct Valkey endpoint from the ElastiCache console.

Example:

```python
AWS_REGION = "ap-south-1"
DYNAMODB_TABLE = "project5-users"

VALKEY_HOST = "your-valkey-endpoint"
VALKEY_PORT = 6379

CACHE_TTL_SECONDS = 300
```

Do not publish private endpoints, credentials, or secrets unnecessarily in a public repository.

---

## 10. Application Flow

### 10.1 Cache hit

1. The application receives a `user_id`.
2. It builds the key `user:<user_id>`.
3. It calls Valkey `GET`.
4. If the key exists, the cached JSON is returned.
5. DynamoDB is not queried.

Example:

```text
GET user:user-1
→ Cache hit
→ Return cached user
```

### 10.2 Cache miss

1. The application receives a `user_id`.
2. It checks Valkey.
3. The key does not exist.
4. The application calls DynamoDB `GetItem`.
5. If the item exists, it is converted into normal Python data.
6. The data is serialized to JSON.
7. Valkey stores it with `SETEX` and a 300-second TTL.
8. The data is returned to the caller.

Example:

```text
GET user:user-1
→ Cache miss
→ Read DynamoDB
→ SETEX user:user-1 300 <json>
→ Return user
```

### 10.3 Update invalidation

```text
Update DynamoDB record
        ↓
Delete user:<id> from Valkey
        ↓
Next read gets fresh data from DynamoDB
        ↓
Fresh data is cached again
```

### 10.4 Delete invalidation

```text
Delete DynamoDB record
        ↓
Delete user:<id> from Valkey
        ↓
Next read returns None after a cache miss
```

---

## 11. Cache Key Convention

The project uses the following key format:

```python
key = f"user:{user_id}"
```

For the user ID `user-1`, the key is:

```text
user:user-1
```

The same key format must be used for:

- Reading cached data
- Writing cached data
- Invalidating cached data
- Deleting cached data

Inconsistent key names can cause stale entries to remain in the cache.

---

## 12. Main Redis/Valkey Operations

| Operation | Purpose |
|---|---|
| `GET` | Read a cached value |
| `SET` | Store a value without an expiration |
| `SETEX` | Store a value with a TTL |
| `TTL` | Check remaining lifetime |
| `DELETE` | Remove a cache key |
| `PING` | Test connectivity |

The project primarily uses:

- `GET` for cache reads
- `SETEX` for TTL-based writes
- `DELETE` for invalidation
- `PING` for connectivity testing

---

## 13. Commands Used During the Lab

Validate the EC2 IAM identity:

```bash
aws sts get-caller-identity
```

Validate DynamoDB access:

```bash
aws dynamodb describe-table   --table-name project5-users   --region ap-south-1
```

Install the network connectivity tool:

```bash
sudo dnf install nmap-ncat -y
```

Test Valkey connectivity:

```bash
nc -vz <valkey-endpoint> 6379
```

Activate the virtual environment:

```bash
source ~/project5-dynamodb-redis/venv/bin/activate
```

Install the Python Redis client:

```bash
pip install redis
```

Run the main application:

```bash
python src/app.py
```

Run the test scripts:

```bash
python tests/test_cache.py
python tests/test_invalidation.py
python tests/test_update_cache.py
python tests/test_delete_cache.py
```

---

## 14. Test Scenarios

The following scenarios were tested during the hands-on implementation:

### Test 1 — EC2 IAM authentication

`aws sts get-caller-identity` confirmed that the EC2 instance was using the assumed role `project5-ec2-dynamodb-role`.

### Test 2 — DynamoDB access

The `describe-table` command succeeded against `project5-users`.

### Test 3 — Valkey connectivity

The TCP connectivity test and Python `ping()` operation succeeded.

### Test 4 — Cache hit

A previously cached `user:user-1` record was returned directly from Valkey.

### Test 5 — Cache miss

After removing the cache key, the application read the record from DynamoDB and repopulated Valkey.

### Test 6 — Update invalidation

The user record was updated in DynamoDB. The old cache key was deleted. The next request retrieved the updated record and cached it again.

### Test 7 — Delete invalidation

The user was deleted from DynamoDB and the corresponding cache key was invalidated. The next application request returned `None`.

### Test 8 — Least-privilege behavior

A table scan failed with `AccessDenied` because `dynamodb:Scan` was not included in the IAM policy.

---

## 15. Troubleshooting Notes

### Problem: Virtual environment permission error

The project was initially created under OneDrive. The virtual environment creation failed because of local permission or synchronization behavior.

**Resolution:** The project was moved to:

```text
C:\AWS-Projects-dynamodb-elasticache-redis
```

### Problem: Serverless subnet validation error

The cache creation process reported that Serverless required between two and three subnet IDs.

**Resolution:** Two subnets in different Availability Zones were selected, including `ap-south-1a` and `ap-south-1b`.

### Problem: `nc` command was unavailable

The `nc` command was not initially installed on Amazon Linux.

**Resolution:**

```bash
sudo dnf install nmap-ncat -y
```

### Problem: Python Redis package missing

The Python cache connection could not work until the Redis client library was installed.

**Resolution:**

```bash
pip install redis
```

### Problem: Unexpected cache hit

The first application test returned a cache hit because an earlier test had already populated `user:user-1`.

**Resolution:** The cache key was deleted before repeating the test, allowing a genuine cache miss to be demonstrated.

### Problem: Database write during module import

The DynamoDB module initially inserted a user as soon as it was imported.

**Resolution:** The insertion code was removed from the import path. The module guard was used instead:

```python
if __name__ == "__main__":
    user = get_user("user-1")
    print(user)
```

This prevents unexpected database mutations when another file imports the module.

### Problem: Python 3.9 warning

Boto3 displayed a warning about future Python 3.9 support.

**Recommendation:** Recreate the environment with Python 3.10 or newer before using this design in production.

---

## 16. Production Considerations

This project is an educational implementation. A production version should additionally consider:

- Private subnets for application and cache resources
- AWS Systems Manager instead of publicly exposed SSH
- Strict security-group rules
- TLS certificate validation and secret management
- Application-level exception handling and retries
- Cache stampede protection
- Race conditions during simultaneous updates
- Failure handling between database writes and cache invalidation
- Cache hit-rate and latency monitoring
- Memory usage and eviction monitoring
- Structured application logging
- Metrics and alarms
- Automated deployment and testing
- Runtime upgrade to Python 3.10 or newer

TTL improves cache freshness but does not guarantee immediate consistency. Explicit invalidation remains important after updates and deletions.

---

## 17. Cleanup Checklist

After saving screenshots and completing the documentation:

- [ ] Delete the Valkey Serverless cache.
- [ ] Delete the DynamoDB table if it is no longer required.
- [ ] Terminate the EC2 instance if it is no longer required.
- [ ] Remove unused security groups after checking dependencies.
- [ ] Remove the IAM role if it is not used elsewhere.
- [ ] Review the AWS Billing dashboard.
- [ ] Confirm that no billable resources remain.

---

## 18. Interview Explanation

> I built a cache-aside system on Amazon EC2 using DynamoDB as the source of truth and ElastiCache Serverless for Valkey as the cache. The application checks Valkey first and returns a cached record on a hit. On a miss, it reads DynamoDB, serializes the record to JSON, and stores it in Valkey with a five-minute TTL. I also implemented explicit cache invalidation after updates and deletes to prevent stale data. EC2 accessed DynamoDB through an IAM role, and security groups restricted cache access to the EC2 application environment. I tested connectivity, cache hits, cache misses, lazy loading, update invalidation, delete invalidation, and least-privilege behavior.

---

## 19. Learning Outcomes

This project provided practical experience with:

- Cache-aside architecture
- Lazy loading
- Cache hits and misses
- Redis/Valkey commands
- TTL-based expiration
- Cache invalidation
- DynamoDB low-level APIs
- DynamoDB typed attribute deserialization
- IAM instance profiles
- Security-group-based access control
- TLS connections to Valkey
- Troubleshooting AWS networking and Python environments
- Designing a GitHub-ready cloud engineering project
