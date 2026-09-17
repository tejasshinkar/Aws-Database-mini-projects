# Project 4: DynamoDB Design + Performance

## Overview

This project explores how to design and test a DynamoDB data model for a
messaging application.

The focus is not only on creating a DynamoDB table, but on understanding how
DynamoDB access patterns influence the table design, query performance,
capacity consumption, and data lifecycle.

The project uses Python and `boto3` to interact with Amazon DynamoDB.

## Scenario

We are modelling messages from a messaging application.

Each message contains information such as:

- `conversation_id`
- `message_id`
- `sender_id`
- `message_text`
- `message_type`
- `created_at`

The main access pattern is:

> Retrieve all messages belonging to a particular conversation in time order.

## DynamoDB Table Design

### Table name

`messaging-app-messages`

### Primary key

- **Partition key:** `conversation_id`
- **Sort key:** `created_at`

The partition key groups messages belonging to the same conversation.
The sort key allows messages within that conversation to be ordered by time.

This design supports efficient queries such as:

- Get all messages from a conversation
- Get messages from a conversation after a particular timestamp
- Get messages from a conversation within a time range

A unique `message_id` is also stored in each item to identify the message.

## Secondary Index

The project also demonstrates a Local Secondary Index (LSI):

- **Index name:** `conversation-time-index`
- **Partition key:** `conversation_id`
- **Sort key:** `created_at`
- **Projected attributes:** All

An LSI uses the same partition key as the base table but provides an alternate
sort-key access pattern.

> Note: An LSI must be created when the table is created. It cannot be added
> to an existing DynamoDB table later.

The project also discusses Global Secondary Indexes (GSIs), which can use a
different partition key and can be added after table creation.

## Activities Completed

The project covers the following DynamoDB concepts:

1. Creating and validating a DynamoDB table
2. Understanding partition keys and sort keys
3. Designing a table around application access patterns
4. Creating and inspecting a Local Secondary Index
5. Understanding the difference between an LSI and a GSI
6. Inserting and reading message records
7. Comparing `Query` and `Scan`
8. Running a data experiment with approximately 1,000 items
9. Understanding read-capacity-unit consumption
10. Performing conditional writes
11. Enabling and validating Time to Live (TTL)

## Query vs. Scan

### Query

`Query` retrieves items using a key condition.

For example:

> Retrieve messages where `conversation_id` equals `conversation-001`.

A query is generally more efficient because DynamoDB can locate the relevant
partition directly.

### Scan

`Scan` examines every item in the table or index.

A scan can be useful for small administrative tasks or experiments, but it is
usually less efficient for application request paths.

## Conditional Writes

Conditional writes allow an operation to proceed only when a specified
condition is true.

Example use cases:

- Insert an item only if it does not already exist
- Update a message only if the current value matches an expected value
- Prevent accidental overwrites

This helps protect data integrity in concurrent applications.

## Time to Live (TTL)

TTL allows DynamoDB to automatically remove expired items after a specified
expiration time.

In this project:

- **TTL attribute:** `expires_at`
- **Attribute type:** Unix epoch time in seconds

TTL is useful for data such as:

- Temporary messages
- Verification records
- Sessions
- Short-lived application events

TTL deletion is asynchronous. An item does not necessarily disappear
immediately when its expiration time is reached.

## Security and Cost Notes

- AWS credentials are not stored in this repository.
- The project uses the AWS CLI credential configuration or an IAM role.
- Avoid committing `.env` files, access keys, or secret keys.
- On-demand capacity is preferable for short experiments when available.
- Provisioned capacity and auto scaling can create costs if configured
  unnecessarily.
- Delete test tables and other resources after completing the experiment.

## Suggested Project Structure

```text
04-dynamodb-design-performance/
├── README.md
├── requirements.txt
├── src/
│   ├── check_dynamodb.py
│   ├── conditional_writes.py
│   ├── enable_ttl.py
│   └── query_gsi.py
├── notes/
├── screenshots/
└── .venv/
```

The exact contents of the `src` directory may change as the project evolves.

## Running the Project

Activate the virtual environment from the project directory:

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run an individual script from the project root:

```powershell
python src/check_dynamodb.py
```

## Key Learnings

- DynamoDB design should begin with access patterns, not tables.
- A good partition key distributes data and supports the required queries.
- A sort key is useful for ordering and range-based retrieval.
- `Query` is generally preferable to `Scan` for application access paths.
- LSIs share the base table's partition key, while GSIs can use a different one.
- Conditional writes help prevent incorrect updates and duplicate data.
- TTL is useful for automatically expiring temporary data.
- Capacity settings must be considered carefully during practical experiments.

## Cleanup Checklist

Before finishing the project:

- [ ] Remove unnecessary test items if required
- [ ] Disable or delete unused indexes and tables where applicable
- [ ] Check DynamoDB capacity settings
- [ ] Confirm that no unnecessary billable resources remain
- [ ] Save important screenshots and command outputs
- [ ] Push the cleaned project to GitHub
