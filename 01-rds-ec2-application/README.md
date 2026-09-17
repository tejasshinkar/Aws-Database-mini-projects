# EC2 + RDS MySQL Web Application

A hands-on AWS mini-project demonstrating how to host a simple Flask web application on Amazon EC2, connect it to Amazon RDS for MySQL, submit data through a browser form, and verify that the data persists in the managed database.

## Problem Statement

Build a small web application that accepts user details through a browser and stores them in a relational database. The application should run on EC2, while the database is managed by Amazon RDS. The workflow must be tested end to end, including direct database verification.

## Architecture

```text
User Browser
     |
     | HTTP :5000
     v
Amazon EC2
  Flask Application
  PyMySQL Driver
     |
     | MySQL :3306
     | Allowed through EC2 security group
     v
Amazon RDS for MySQL
  Database: rdsapp
  Table: users
```

## AWS Resources

| Resource | Configuration |
|---|---|
| Compute | Amazon EC2, `t3.micro` |
| Application | Flask + Python |
| Database | Amazon RDS for MySQL |
| Database name | `rdsapp` |
| Table | `users` |
| Database port | `3306` |
| Application port | `5000` |
| Connectivity | RDS security group allows MySQL from the EC2 security group |

## Application Features

- Flask application hosted on EC2
- HTML registration form
- Insert user records into RDS MySQL
- Retrieve and display stored users on the frontend
- Basic input validation
- Email-format validation
- Length checks for name and email fields
- Database exception handling
- Transaction rollback when an insert fails
- Database connection cleanup using `finally`
- Direct SQL verification of persisted records

## Database Schema

```sql
CREATE DATABASE rdsapp;

USE rdsapp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Request Flow

1. A user opens the Flask application in a browser.
2. The user submits the registration form.
3. Flask receives the form data.
4. The application validates the name and email.
5. PyMySQL opens a connection to RDS.
6. A parameterized `INSERT` query stores the record.
7. The transaction is committed.
8. Flask queries the `users` table and displays the records.
9. A direct SQL query is used to verify persistence independently of the frontend.

## Validation and Error Handling

The application checks for:

- Empty name or email values
- Names longer than the database column allows
- Invalid email formats
- Database operation failures

If a database operation fails, the application rolls back the transaction, logs the technical error, closes the connection, and displays a user-friendly message.

## Security Notes

- RDS MySQL access is restricted to the EC2 security group rather than an open IP range.
- Database credentials are kept in environment variables through a `.env` file.
- The `.env` file must not be committed to GitHub.
- The application uses parameterized SQL values instead of string-concatenated queries.
- The development Flask server was used only for this learning project; a production deployment should use a WSGI server behind a reverse proxy.
- HTTPS and a domain name were outside the scope of this mini-project.

## Verification Evidence

The project was tested through the following flow:

- Submitted users through the browser form.
- Confirmed the success response from Flask.
- Queried RDS directly using `SELECT * FROM users;`.
- Confirmed that the submitted records appeared in the database.
- Confirmed that stored records were rendered back on the webpage.
- Tested invalid form input and confirmed that validation prevented an invalid submission.

Add the relevant screenshots to the `screenshots/` directory and reference them below.

### Suggested Evidence

- `01-ec2-running.png` — EC2 instance running
- `02-rds-created.png` — RDS database created
- `03-security-group.png` — RDS access restricted to the EC2 security group
- `04-registration-form.png` — Browser form
- `05-form-submission-success.png` — Successful submission
- `06-rds-persistence-verification.png` — Direct SQL query showing saved records
- `07-users-displayed-from-rds.png` — Records displayed on the frontend

## Project Structure

```text
rds-ec2-application/
├── app.py
├── app_basic.py
├── db_test.py
├── .env.example
├── requirements.txt
├── templates/
│   └── index.html
├── screenshots/
│   └── ...
└── README.md
```

## Local/EC2 Setup Overview

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The application expects database configuration through environment variables:

```text
DB_HOST=<rds-endpoint>
DB_PORT=3306
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_NAME=rdsapp
```

Do not commit real credentials.

## What This Project Demonstrates

This mini-project connects several AWS and application concepts into one working workflow:

- EC2 application hosting
- RDS managed relational databases
- VPC security-group-based access control
- Application-to-database connectivity
- SQL schema creation
- CRUD fundamentals: create and read
- Python virtual environments
- Environment-based configuration
- Input validation and error handling
- Database transaction handling
- End-to-end testing and persistence verification

## Future Improvements

- Deploy Flask with Gunicorn or another production WSGI server
- Put Nginx or an Application Load Balancer in front of the application
- Enable HTTPS with ACM and a suitable architecture
- Store secrets in AWS Secrets Manager or Systems Manager Parameter Store
- Add authentication and authorization
- Add automated tests and CI/CD
- Use private subnets for RDS and restrict application access further
- Add CloudWatch logging and monitoring

## Disclaimer

This is a learning-focused mini-project built in an AWS environment. It demonstrates production-oriented concepts but is not presented as a production deployment.
